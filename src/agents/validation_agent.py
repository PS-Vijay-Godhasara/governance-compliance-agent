"""Validation Agent for data validation and compliance checking"""

import re
from datetime import datetime, timedelta
from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentMessage, AgentResponse
import logging

logger = logging.getLogger(__name__)


class ValidationAgent(BaseAgent):
    """Agent for data validation and compliance checking"""
    
    def __init__(self):
        super().__init__("ValidationAgent")
        self.validation_rules = {}
        self.risk_thresholds = {
            "high": 0.8,
            "medium": 0.5,
            "low": 0.2
        }
        
    async def initialize(self):
        """Initialize validation agent"""
        # Load default validation patterns
        self.validation_patterns = {
            "email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            "phone": r'^\+?1?-?\.?\s?\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})$',
            "ssn": r'^\d{3}-?\d{2}-?\d{4}$',
            "credit_card": r'^\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}$'
        }
        logger.info("ValidationAgent initialized")
    
    async def process_message(self, message: AgentMessage) -> AgentResponse:
        """Process validation-related messages"""
        try:
            if message.action == "validate_data":
                return await self._validate_data(message.payload)
            elif message.action == "kyc_validation":
                return await self._kyc_validation(message.payload)
            elif message.action == "risk_assessment":
                return await self._risk_assessment(message.payload)
            elif message.action == "compliance_check":
                return await self._compliance_check(message.payload)
            else:
                return AgentResponse(success=False, error=f"Unknown action: {message.action}")
        except Exception as e:
            return AgentResponse(success=False, error=str(e))
    
    async def _validate_data(self, payload: Dict[str, Any]) -> AgentResponse:
        """Validate data against policy rules"""
        try:
            data = payload.get("data", {})
            rules = payload.get("rules", {})
            context = payload.get("context", {})
            
            violations = []
            warnings = []
            score = 1.0
            
            # Validate each rule
            for rule in rules.get("rules", []):
                field_name = rule.get("field")
                field_type = rule.get("type")
                required = rule.get("required", False)
                constraints = rule.get("constraints", {})
                
                # Check if required field is present
                if required and field_name not in data:
                    violations.append({
                        "field": field_name,
                        "type": "missing_required",
                        "message": f"Required field '{field_name}' is missing",
                        "severity": "high"
                    })
                    score -= 0.2
                    continue
                
                if field_name not in data:
                    continue
                
                field_value = data[field_name]
                
                # Type validation
                if not self._validate_type(field_value, field_type):
                    violations.append({
                        "field": field_name,
                        "type": "invalid_type",
                        "message": f"Field '{field_name}' should be of type {field_type}",
                        "severity": "medium"
                    })
                    score -= 0.1
                
                # Constraint validation
                constraint_result = self._validate_constraints(field_value, constraints)
                if not constraint_result["valid"]:
                    violations.append({
                        "field": field_name,
                        "type": "constraint_violation",
                        "message": constraint_result["message"],
                        "severity": "medium"
                    })
                    score -= 0.1
                
                # Pattern validation
                if field_type in self.validation_patterns:
                    if not re.match(self.validation_patterns[field_type], str(field_value)):
                        violations.append({
                            "field": field_name,
                            "type": "pattern_mismatch",
                            "message": f"Field '{field_name}' does not match expected {field_type} format",
                            "severity": "medium"
                        })
                        score -= 0.1
            
            # Business rule validation
            for business_rule in rules.get("business_rules", []):
                rule_result = await self._validate_business_rule(data, business_rule, context)
                if not rule_result["valid"]:
                    violations.append({
                        "field": "business_rule",
                        "type": "business_rule_violation",
                        "message": rule_result["message"],
                        "severity": business_rule.get("priority", "medium")
                    })
                    score -= 0.15
            
            score = max(0.0, score)
            is_valid = len(violations) == 0
            
            return AgentResponse(
                success=True,
                data={
                    "is_valid": is_valid,
                    "score": score,
                    "violations": violations,
                    "warnings": warnings,
                    "total_checks": len(rules.get("rules", [])) + len(rules.get("business_rules", []))
                }
            )
            
        except Exception as e:
            logger.error(f"Data validation error: {e}")
            return AgentResponse(success=False, error=str(e))
    
    async def _kyc_validation(self, payload: Dict[str, Any]) -> AgentResponse:
        """Perform KYC (Know Your Customer) validation"""
        try:
            customer_data = payload.get("customer_data", {})
            kyc_requirements = payload.get("requirements", {})
            
            kyc_score = 1.0
            issues = []
            
            # Identity verification
            if "identity_documents" not in customer_data:
                issues.append({
                    "type": "missing_identity",
                    "message": "Identity documents required for KYC",
                    "severity": "high"
                })
                kyc_score -= 0.3
            
            # Address verification
            if "address_proof" not in customer_data:
                issues.append({
                    "type": "missing_address",
                    "message": "Address proof required for KYC",
                    "severity": "medium"
                })
                kyc_score -= 0.2
            
            # Age verification
            if "date_of_birth" in customer_data:
                age = self._calculate_age(customer_data["date_of_birth"])
                if age < 18:
                    issues.append({
                        "type": "underage",
                        "message": "Customer must be 18 or older",
                        "severity": "high"
                    })
                    kyc_score -= 0.5
            
            # Document expiry check
            if "identity_documents" in customer_data:
                for doc in customer_data["identity_documents"]:
                    if "expiry_date" in doc:
                        if self._is_document_expired(doc["expiry_date"]):
                            issues.append({
                                "type": "expired_document",
                                "message": f"Document {doc.get('type', 'unknown')} has expired",
                                "severity": "high"
                            })
                            kyc_score -= 0.2
            
            kyc_score = max(0.0, kyc_score)
            kyc_status = "approved" if kyc_score >= 0.7 else "rejected" if kyc_score < 0.3 else "review_required"
            
            return AgentResponse(
                success=True,
                data={
                    "kyc_status": kyc_status,
                    "kyc_score": kyc_score,
                    "issues": issues,
                    "recommendation": self._get_kyc_recommendation(kyc_status, issues)
                }
            )
            
        except Exception as e:
            logger.error(f"KYC validation error: {e}")
            return AgentResponse(success=False, error=str(e))
    
    async def _risk_assessment(self, payload: Dict[str, Any]) -> AgentResponse:
        """Perform risk assessment"""
        try:
            data = payload.get("data", {})
            context = payload.get("context", {})
            
            risk_factors = []
            risk_score = 0.0
            
            # Transaction amount risk
            if "transaction_amount" in data:
                amount = float(data["transaction_amount"])
                if amount > 10000:
                    risk_factors.append({"factor": "high_value_transaction", "weight": 0.3})
                    risk_score += 0.3
                elif amount > 5000:
                    risk_factors.append({"factor": "medium_value_transaction", "weight": 0.1})
                    risk_score += 0.1
            
            # Geographic risk
            if "country" in data:
                high_risk_countries = ["XX", "YY"]  # Example high-risk countries
                if data["country"] in high_risk_countries:
                    risk_factors.append({"factor": "high_risk_geography", "weight": 0.4})
                    risk_score += 0.4
            
            # Customer history risk
            if "customer_history" in context:
                history = context["customer_history"]
                if history.get("previous_violations", 0) > 0:
                    risk_factors.append({"factor": "previous_violations", "weight": 0.2})
                    risk_score += 0.2
            
            # Determine risk level
            if risk_score >= self.risk_thresholds["high"]:
                risk_level = "high"
            elif risk_score >= self.risk_thresholds["medium"]:
                risk_level = "medium"
            else:
                risk_level = "low"
            
            return AgentResponse(
                success=True,
                data={
                    "risk_level": risk_level,
                    "risk_score": min(1.0, risk_score),
                    "risk_factors": risk_factors,
                    "recommendation": self._get_risk_recommendation(risk_level)
                }
            )
            
        except Exception as e:
            logger.error(f"Risk assessment error: {e}")
            return AgentResponse(success=False, error=str(e))
    
    async def _compliance_check(self, payload: Dict[str, Any]) -> AgentResponse:
        """Check compliance against regulations"""
        try:
            data = payload.get("data", {})
            regulations = payload.get("regulations", [])
            jurisdiction = payload.get("jurisdiction", "GLOBAL")
            
            compliance_results = []
            overall_compliant = True
            
            for regulation in regulations:
                reg_name = regulation.get("name", "Unknown")
                requirements = regulation.get("requirements", [])
                
                reg_compliant = True
                violations = []
                
                for requirement in requirements:
                    if not self._check_requirement(data, requirement):
                        reg_compliant = False
                        overall_compliant = False
                        violations.append({
                            "requirement": requirement.get("name", "Unknown"),
                            "description": requirement.get("description", ""),
                            "severity": requirement.get("severity", "medium")
                        })
                
                compliance_results.append({
                    "regulation": reg_name,
                    "compliant": reg_compliant,
                    "violations": violations
                })
            
            return AgentResponse(
                success=True,
                data={
                    "overall_compliant": overall_compliant,
                    "jurisdiction": jurisdiction,
                    "compliance_results": compliance_results,
                    "total_regulations_checked": len(regulations)
                }
            )
            
        except Exception as e:
            logger.error(f"Compliance check error: {e}")
            return AgentResponse(success=False, error=str(e))
    
    def _validate_type(self, value: Any, expected_type: str) -> bool:
        """Validate field type"""
        type_mapping = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "email": str,
            "phone": str,
            "date": str
        }
        
        expected_python_type = type_mapping.get(expected_type, str)
        return isinstance(value, expected_python_type)
    
    def _validate_constraints(self, value: Any, constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Validate field constraints"""
        if "min" in constraints and isinstance(value, (int, float)):
            if value < constraints["min"]:
                return {"valid": False, "message": f"Value {value} is below minimum {constraints['min']}"}
        
        if "max" in constraints and isinstance(value, (int, float)):
            if value > constraints["max"]:
                return {"valid": False, "message": f"Value {value} is above maximum {constraints['max']}"}
        
        if "min_length" in constraints and isinstance(value, str):
            if len(value) < constraints["min_length"]:
                return {"valid": False, "message": f"String length {len(value)} is below minimum {constraints['min_length']}"}
        
        return {"valid": True, "message": "Valid"}
    
    async def _validate_business_rule(self, data: Dict[str, Any], rule: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate business rule"""
        condition = rule.get("condition", "")
        
        # Simple condition evaluation (in production, use a proper rule engine)
        if "age > 18" in condition:
            age = data.get("age", 0)
            if age <= 18:
                return {"valid": False, "message": "Age must be greater than 18"}
        
        if "amount > 10000" in condition:
            amount = data.get("transaction_amount", 0)
            if amount > 10000:
                return {"valid": False, "message": "High value transactions require additional approval"}
        
        return {"valid": True, "message": "Business rule satisfied"}
    
    def _calculate_age(self, date_of_birth: str) -> int:
        """Calculate age from date of birth"""
        try:
            birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d")
            today = datetime.now()
            return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        except:
            return 0
    
    def _is_document_expired(self, expiry_date: str) -> bool:
        """Check if document is expired"""
        try:
            expiry = datetime.strptime(expiry_date, "%Y-%m-%d")
            return expiry < datetime.now()
        except:
            return True
    
    def _get_kyc_recommendation(self, status: str, issues: List[Dict]) -> str:
        """Get KYC recommendation"""
        if status == "approved":
            return "Customer approved for onboarding"
        elif status == "rejected":
            return "Customer rejected - critical issues found"
        else:
            return "Manual review required - resolve identified issues"
    
    def _get_risk_recommendation(self, risk_level: str) -> str:
        """Get risk recommendation"""
        recommendations = {
            "low": "Standard processing approved",
            "medium": "Enhanced monitoring recommended",
            "high": "Manual review and approval required"
        }
        return recommendations.get(risk_level, "Unknown risk level")
    
    def _check_requirement(self, data: Dict[str, Any], requirement: Dict[str, Any]) -> bool:
        """Check if data meets requirement"""
        req_type = requirement.get("type", "")
        
        if req_type == "field_required":
            field_name = requirement.get("field", "")
            return field_name in data and data[field_name] is not None
        
        if req_type == "data_retention":
            # Check if data retention policies are met
            return True  # Simplified
        
        return True