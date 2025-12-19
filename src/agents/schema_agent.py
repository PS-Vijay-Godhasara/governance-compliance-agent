"""Schema Agent for database/API schema evolution management"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from .base_agent import BaseAgent, AgentMessage, AgentResponse
import logging

logger = logging.getLogger(__name__)


class SchemaAgent(BaseAgent):
    """Agent for handling schema drift and evolution"""
    
    def __init__(self):
        super().__init__("SchemaAgent")
        self.schema_versions = {}
        self.migration_strategies = {}
        
    async def initialize(self):
        """Initialize schema agent"""
        logger.info("SchemaAgent initialized")
    
    async def process_message(self, message: AgentMessage) -> AgentResponse:
        """Process schema-related messages"""
        try:
            if message.action == "detect_drift":
                return await self._detect_drift(message.payload)
            elif message.action == "generate_migration":
                return await self._generate_migration(message.payload)
            elif message.action == "validate_compatibility":
                return await self._validate_compatibility(message.payload)
            elif message.action == "register_schema":
                return await self._register_schema(message.payload)
            else:
                return AgentResponse(success=False, error=f"Unknown action: {message.action}")
        except Exception as e:
            return AgentResponse(success=False, error=str(e))
    
    async def _detect_drift(self, payload: Dict[str, Any]) -> AgentResponse:
        """Detect schema changes between versions"""
        try:
            old_schema = payload.get("old_schema", {})
            new_schema = payload.get("new_schema", {})
            
            changes = []
            
            # Detect field changes
            old_props = old_schema.get("properties", {})
            new_props = new_schema.get("properties", {})
            
            # New fields
            for field in new_props:
                if field not in old_props:
                    changes.append({
                        "type": "field_added",
                        "field": field,
                        "description": f"New field '{field}' added",
                        "impact": self._assess_impact("field_added", field, new_props[field]),
                        "migration_strategy": self._suggest_migration("field_added", field, new_props[field])
                    })
            
            # Removed fields
            for field in old_props:
                if field not in new_props:
                    changes.append({
                        "type": "field_removed",
                        "field": field,
                        "description": f"Field '{field}' removed",
                        "impact": "high",
                        "migration_strategy": "Backup data before removal, update dependent systems"
                    })
            
            # Modified fields
            for field in old_props:
                if field in new_props:
                    old_field = old_props[field]
                    new_field = new_props[field]
                    
                    # Type changes
                    if old_field.get("type") != new_field.get("type"):
                        changes.append({
                            "type": "type_changed",
                            "field": field,
                            "description": f"Field '{field}' type changed from {old_field.get('type')} to {new_field.get('type')}",
                            "impact": "medium",
                            "migration_strategy": f"Convert existing {old_field.get('type')} values to {new_field.get('type')}"
                        })
                    
                    # Required status changes
                    old_required = old_field.get("required", False)
                    new_required = new_field.get("required", False)
                    if old_required != new_required:
                        changes.append({
                            "type": "required_changed",
                            "field": field,
                            "description": f"Field '{field}' required status changed from {old_required} to {new_required}",
                            "impact": "medium" if new_required else "low",
                            "migration_strategy": "Add default values for newly required fields" if new_required else "No action needed"
                        })
            
            # Schema-level changes
            if old_schema.get("required", []) != new_schema.get("required", []):
                changes.append({
                    "type": "required_fields_changed",
                    "field": "schema",
                    "description": "Required fields list changed",
                    "impact": "medium",
                    "migration_strategy": "Update validation logic and add defaults for new required fields"
                })
            
            return AgentResponse(
                success=True,
                data={
                    "changes": changes,
                    "total_changes": len(changes),
                    "risk_level": self._calculate_risk_level(changes),
                    "compatibility": "breaking" if any(c["impact"] == "high" for c in changes) else "non-breaking"
                }
            )
            
        except Exception as e:
            logger.error(f"Schema drift detection error: {e}")
            return AgentResponse(success=False, error=str(e))
    
    async def _generate_migration(self, payload: Dict[str, Any]) -> AgentResponse:
        """Generate migration plan for schema changes"""
        try:
            changes = payload.get("changes", [])
            target_system = payload.get("target_system", "database")
            
            migration_steps = []
            rollback_steps = []
            
            for change in changes:
                change_type = change.get("type")
                field = change.get("field")
                
                if change_type == "field_added":
                    migration_steps.append({
                        "step": f"ADD_COLUMN_{field}",
                        "sql": f"ALTER TABLE main_table ADD COLUMN {field} {self._get_sql_type(change)}",
                        "description": f"Add new column {field}",
                        "order": 1
                    })
                    rollback_steps.append({
                        "step": f"DROP_COLUMN_{field}",
                        "sql": f"ALTER TABLE main_table DROP COLUMN {field}",
                        "description": f"Remove column {field}",
                        "order": 1
                    })
                
                elif change_type == "field_removed":
                    migration_steps.append({
                        "step": f"BACKUP_DATA_{field}",
                        "sql": f"CREATE TABLE backup_{field} AS SELECT id, {field} FROM main_table",
                        "description": f"Backup data for field {field}",
                        "order": 1
                    })
                    migration_steps.append({
                        "step": f"DROP_COLUMN_{field}",
                        "sql": f"ALTER TABLE main_table DROP COLUMN {field}",
                        "description": f"Remove column {field}",
                        "order": 2
                    })
                
                elif change_type == "type_changed":
                    migration_steps.append({
                        "step": f"CONVERT_TYPE_{field}",
                        "sql": f"ALTER TABLE main_table ALTER COLUMN {field} TYPE {self._get_sql_type(change)}",
                        "description": f"Convert {field} to new type",
                        "order": 1
                    })
            
            # Sort by execution order
            migration_steps.sort(key=lambda x: x["order"])
            rollback_steps.sort(key=lambda x: x["order"], reverse=True)
            
            return AgentResponse(
                success=True,
                data={
                    "migration_plan": {
                        "steps": migration_steps,
                        "rollback_steps": rollback_steps,
                        "estimated_duration": self._estimate_duration(migration_steps),
                        "risk_assessment": self._assess_migration_risk(changes),
                        "prerequisites": self._get_prerequisites(changes),
                        "validation_queries": self._generate_validation_queries(changes)
                    }
                }
            )
            
        except Exception as e:
            logger.error(f"Migration generation error: {e}")
            return AgentResponse(success=False, error=str(e))
    
    async def _validate_compatibility(self, payload: Dict[str, Any]) -> AgentResponse:
        """Validate backward compatibility"""
        try:
            old_schema = payload.get("old_schema", {})
            new_schema = payload.get("new_schema", {})
            
            compatibility_issues = []
            
            # Check for breaking changes
            old_required = set(old_schema.get("required", []))
            new_required = set(new_schema.get("required", []))
            
            # New required fields are breaking
            new_required_fields = new_required - old_required
            for field in new_required_fields:
                compatibility_issues.append({
                    "type": "breaking_change",
                    "field": field,
                    "issue": f"Field '{field}' is now required",
                    "impact": "Existing data may fail validation"
                })
            
            # Removed fields are breaking
            old_props = set(old_schema.get("properties", {}).keys())
            new_props = set(new_schema.get("properties", {}).keys())
            removed_fields = old_props - new_props
            
            for field in removed_fields:
                compatibility_issues.append({
                    "type": "breaking_change",
                    "field": field,
                    "issue": f"Field '{field}' was removed",
                    "impact": "Applications using this field will break"
                })
            
            # Type changes can be breaking
            for field in old_props & new_props:
                old_type = old_schema["properties"][field].get("type")
                new_type = new_schema["properties"][field].get("type")
                
                if old_type != new_type and not self._is_compatible_type_change(old_type, new_type):
                    compatibility_issues.append({
                        "type": "breaking_change",
                        "field": field,
                        "issue": f"Field '{field}' type changed from {old_type} to {new_type}",
                        "impact": "Data conversion may fail or lose precision"
                    })
            
            is_compatible = len([issue for issue in compatibility_issues if issue["type"] == "breaking_change"]) == 0
            
            return AgentResponse(
                success=True,
                data={
                    "is_compatible": is_compatible,
                    "compatibility_level": "full" if is_compatible else "partial",
                    "issues": compatibility_issues,
                    "recommendations": self._get_compatibility_recommendations(compatibility_issues)
                }
            )
            
        except Exception as e:
            logger.error(f"Compatibility validation error: {e}")
            return AgentResponse(success=False, error=str(e))
    
    async def _register_schema(self, payload: Dict[str, Any]) -> AgentResponse:
        """Register a new schema version"""
        try:
            schema_id = payload.get("schema_id", f"schema_{len(self.schema_versions)}")
            schema_data = payload.get("schema", {})
            version = payload.get("version", "1.0.0")
            
            self.schema_versions[schema_id] = {
                "version": version,
                "schema": schema_data,
                "registered_at": datetime.now().isoformat(),
                "metadata": payload.get("metadata", {})
            }
            
            return AgentResponse(
                success=True,
                data={
                    "schema_id": schema_id,
                    "version": version,
                    "registered": True
                }
            )
            
        except Exception as e:
            logger.error(f"Schema registration error: {e}")
            return AgentResponse(success=False, error=str(e))
    
    def _assess_impact(self, change_type: str, field: str, field_def: Dict[str, Any]) -> str:
        """Assess impact of schema change"""
        if change_type == "field_added":
            return "low" if not field_def.get("required", False) else "medium"
        elif change_type == "field_removed":
            return "high"
        elif change_type == "type_changed":
            return "medium"
        return "low"
    
    def _suggest_migration(self, change_type: str, field: str, field_def: Dict[str, Any]) -> str:
        """Suggest migration strategy"""
        if change_type == "field_added":
            if field_def.get("required", False):
                return f"Add default value for required field '{field}'"
            return f"Add optional field '{field}' - no migration needed"
        return "Standard migration required"
    
    def _calculate_risk_level(self, changes: List[Dict[str, Any]]) -> str:
        """Calculate overall risk level"""
        high_impact = sum(1 for c in changes if c.get("impact") == "high")
        medium_impact = sum(1 for c in changes if c.get("impact") == "medium")
        
        if high_impact > 0:
            return "high"
        elif medium_impact > 2:
            return "medium"
        return "low"
    
    def _get_sql_type(self, change: Dict[str, Any]) -> str:
        """Get SQL type for field"""
        # Simplified type mapping
        type_mapping = {
            "string": "VARCHAR(255)",
            "integer": "INTEGER",
            "number": "DECIMAL(10,2)",
            "boolean": "BOOLEAN",
            "date": "DATE",
            "datetime": "TIMESTAMP"
        }
        return type_mapping.get(change.get("field_type", "string"), "VARCHAR(255)")
    
    def _estimate_duration(self, steps: List[Dict[str, Any]]) -> str:
        """Estimate migration duration"""
        base_time = len(steps) * 5  # 5 minutes per step
        return f"{base_time} minutes"
    
    def _assess_migration_risk(self, changes: List[Dict[str, Any]]) -> str:
        """Assess migration risk"""
        return self._calculate_risk_level(changes)
    
    def _get_prerequisites(self, changes: List[Dict[str, Any]]) -> List[str]:
        """Get migration prerequisites"""
        return [
            "Database backup completed",
            "Application maintenance window scheduled",
            "Rollback plan tested"
        ]
    
    def _generate_validation_queries(self, changes: List[Dict[str, Any]]) -> List[str]:
        """Generate validation queries"""
        return [
            "SELECT COUNT(*) FROM main_table",
            "SELECT * FROM main_table LIMIT 10"
        ]
    
    def _is_compatible_type_change(self, old_type: str, new_type: str) -> bool:
        """Check if type change is compatible"""
        compatible_changes = {
            ("integer", "number"),
            ("string", "text")
        }
        return (old_type, new_type) in compatible_changes
    
    def _get_compatibility_recommendations(self, issues: List[Dict[str, Any]]) -> List[str]:
        """Get compatibility recommendations"""
        recommendations = []
        
        if any(issue["type"] == "breaking_change" for issue in issues):
            recommendations.append("Consider versioning your API to maintain backward compatibility")
            recommendations.append("Implement gradual migration strategy")
            recommendations.append("Provide migration tools for existing clients")
        
        return recommendations