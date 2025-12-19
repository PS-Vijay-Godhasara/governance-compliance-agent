"""Explanation Agent for generating human-readable explanations"""

from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentMessage, AgentResponse
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)


class ExplanationAgent(BaseAgent):
    """Agent for generating explanations and recommendations"""
    
    def __init__(self, llm_client=None):
        super().__init__("ExplanationAgent")
        self.llm_client = llm_client
        self.explanation_templates = {}
        
    async def initialize(self):
        """Initialize explanation agent"""
        if not self.llm_client:
            from ..providers.ollama import OllamaProvider
            self.llm_client = OllamaProvider(
                base_url=settings.LLM_BASE_URL,
                model=settings.LLM_MODEL
            )
        
        self._load_templates()
        logger.info("ExplanationAgent initialized")
    
    async def process_message(self, message: AgentMessage) -> AgentResponse:
        """Process explanation-related messages"""
        try:
            if message.action == "explain_violation":
                return await self._explain_violation(message.payload)
            elif message.action == "generate_remediation":
                return await self._generate_remediation(message.payload)
            elif message.action == "explain_decision":
                return await self._explain_decision(message.payload)
            elif message.action == "risk_explanation":
                return await self._risk_explanation(message.payload)
            else:
                return AgentResponse(success=False, error=f"Unknown action: {message.action}")
        except Exception as e:
            return AgentResponse(success=False, error=str(e))
    
    async def _explain_violation(self, payload: Dict[str, Any]) -> AgentResponse:
        """Generate explanation for policy violations"""
        try:
            violations = payload.get("violations", [])
            context = payload.get("context", {})
            policy_name = payload.get("policy_name", "Unknown Policy")
            
            explanations = []
            
            for violation in violations:
                field = violation.get("field", "unknown")
                violation_type = violation.get("type", "unknown")
                severity = violation.get("severity", "medium")
                
                # Generate detailed explanation using LLM
                prompt = f"""
                Explain this policy violation in simple business terms:
                
                Policy: {policy_name}
                Field: {field}
                Violation Type: {violation_type}
                Severity: {severity}
                Context: {context}
                
                Provide:
                1. What went wrong (in plain English)
                2. Why this rule exists (business justification)
                3. Potential consequences if ignored
                4. Specific steps to fix it
                
                Keep explanation clear and actionable for business users.
                """
                
                try:
                    llm_explanation = await self.llm_client.generate(prompt)
                    
                    explanation = {
                        "field": field,
                        "violation_type": violation_type,
                        "severity": severity,
                        "explanation": llm_explanation,
                        "business_impact": self._assess_business_impact(violation_type, severity),
                        "urgency": self._determine_urgency(severity),
                        "stakeholders": self._identify_stakeholders(field, violation_type)
                    }
                    
                except Exception as e:
                    # Fallback to template-based explanation
                    explanation = {
                        "field": field,
                        "violation_type": violation_type,
                        "severity": severity,
                        "explanation": self._get_template_explanation(violation_type, field),
                        "business_impact": self._assess_business_impact(violation_type, severity),
                        "urgency": self._determine_urgency(severity),
                        "stakeholders": self._identify_stakeholders(field, violation_type)
                    }
                
                explanations.append(explanation)
            
            return AgentResponse(
                success=True,
                data={
                    "explanations": explanations,
                    "summary": self._generate_summary(explanations),
                    "overall_risk": self._calculate_overall_risk(violations),
                    "next_steps": self._suggest_next_steps(explanations)
                }
            )
            
        except Exception as e:
            logger.error(f"Violation explanation error: {e}")
            return AgentResponse(success=False, error=str(e))
    
    async def _generate_remediation(self, payload: Dict[str, Any]) -> AgentResponse:
        """Generate remediation suggestions"""
        try:
            violations = payload.get("violations", [])
            context = payload.get("context", {})
            
            remediation_plan = {
                "immediate_actions": [],
                "short_term_actions": [],
                "long_term_actions": [],
                "preventive_measures": []
            }
            
            for violation in violations:
                field = violation.get("field", "unknown")
                violation_type = violation.get("type", "unknown")
                severity = violation.get("severity", "medium")
                
                # Generate remediation using LLM
                prompt = f"""
                Generate specific remediation steps for this compliance violation:
                
                Field: {field}
                Violation: {violation_type}
                Severity: {severity}
                Context: {context}
                
                Provide:
                1. Immediate actions (within 24 hours)
                2. Short-term fixes (within 1 week)
                3. Long-term improvements (within 1 month)
                4. Prevention strategies
                
                Make recommendations specific and actionable.
                """
                
                try:
                    llm_remediation = await self.llm_client.generate(prompt)
                    parsed_remediation = self._parse_remediation_response(llm_remediation)
                    
                    # Merge with remediation plan
                    for category in remediation_plan:
                        if category in parsed_remediation:
                            remediation_plan[category].extend(parsed_remediation[category])
                
                except Exception as e:
                    # Fallback to template-based remediation
                    template_remediation = self._get_template_remediation(violation_type, field, severity)
                    for category in remediation_plan:
                        if category in template_remediation:
                            remediation_plan[category].extend(template_remediation[category])
            
            # Remove duplicates and prioritize
            for category in remediation_plan:
                remediation_plan[category] = list(set(remediation_plan[category]))
            
            return AgentResponse(
                success=True,
                data={
                    "remediation_plan": remediation_plan,
                    "estimated_effort": self._estimate_remediation_effort(remediation_plan),
                    "success_metrics": self._define_success_metrics(violations),
                    "timeline": self._create_timeline(remediation_plan)
                }
            )
            
        except Exception as e:
            logger.error(f"Remediation generation error: {e}")
            return AgentResponse(success=False, error=str(e))
    
    async def _explain_decision(self, payload: Dict[str, Any]) -> AgentResponse:
        """Explain automated decision making"""
        try:
            decision = payload.get("decision", {})
            factors = payload.get("factors", [])
            context = payload.get("context", {})
            
            prompt = f"""
            Explain this automated compliance decision in business terms:
            
            Decision: {decision}
            Contributing Factors: {factors}
            Context: {context}
            
            Explain:
            1. What decision was made and why
            2. Which factors were most important
            3. How the decision protects the business
            4. What would happen with different inputs
            
            Use clear, non-technical language suitable for business stakeholders.
            """
            
            try:
                explanation = await self.llm_client.generate(prompt)
            except Exception as e:
                explanation = self._get_template_decision_explanation(decision, factors)
            
            return AgentResponse(
                success=True,
                data={
                    "explanation": explanation,
                    "decision_factors": self._rank_decision_factors(factors),
                    "confidence_level": decision.get("confidence", 0.8),
                    "alternative_scenarios": self._generate_alternative_scenarios(decision, factors),
                    "audit_trail": self._create_audit_trail(decision, factors, context)
                }
            )
            
        except Exception as e:
            logger.error(f"Decision explanation error: {e}")
            return AgentResponse(success=False, error=str(e))
    
    async def _risk_explanation(self, payload: Dict[str, Any]) -> AgentResponse:
        """Explain risk assessment results"""
        try:
            risk_assessment = payload.get("risk_assessment", {})
            risk_factors = payload.get("risk_factors", [])
            context = payload.get("context", {})
            
            risk_level = risk_assessment.get("risk_level", "unknown")
            risk_score = risk_assessment.get("risk_score", 0.0)
            
            prompt = f"""
            Explain this risk assessment in business terms:
            
            Risk Level: {risk_level}
            Risk Score: {risk_score}
            Risk Factors: {risk_factors}
            Context: {context}
            
            Explain:
            1. What the risk level means for the business
            2. Which factors contribute most to the risk
            3. Potential business consequences
            4. How to reduce the risk
            
            Make it understandable for non-technical business users.
            """
            
            try:
                explanation = await self.llm_client.generate(prompt)
            except Exception as e:
                explanation = self._get_template_risk_explanation(risk_level, risk_factors)
            
            return AgentResponse(
                success=True,
                data={
                    "explanation": explanation,
                    "risk_breakdown": self._break_down_risk_factors(risk_factors),
                    "mitigation_strategies": self._suggest_risk_mitigation(risk_factors),
                    "monitoring_recommendations": self._recommend_monitoring(risk_level, risk_factors),
                    "escalation_triggers": self._define_escalation_triggers(risk_level)
                }
            )
            
        except Exception as e:
            logger.error(f"Risk explanation error: {e}")
            return AgentResponse(success=False, error=str(e))
    
    def _load_templates(self):
        """Load explanation templates"""
        self.explanation_templates = {
            "missing_required": "The required field '{field}' is missing. This field is mandatory because {reason}.",
            "invalid_type": "The field '{field}' has an invalid data type. Expected {expected_type} but received {actual_type}.",
            "constraint_violation": "The field '{field}' violates business constraints. {constraint_details}.",
            "pattern_mismatch": "The field '{field}' doesn't match the expected format. {format_requirements}.",
            "business_rule_violation": "A business rule was violated: {rule_description}. This rule exists to {business_justification}."
        }
    
    def _get_template_explanation(self, violation_type: str, field: str) -> str:
        """Get template-based explanation"""
        template = self.explanation_templates.get(violation_type, "Unknown violation type for field '{field}'.")
        return template.format(field=field, reason="it's required for compliance", 
                             expected_type="string", actual_type="number",
                             constraint_details="value exceeds allowed limits",
                             format_requirements="must be a valid email address",
                             rule_description="age verification rule",
                             business_justification="ensure regulatory compliance")
    
    def _assess_business_impact(self, violation_type: str, severity: str) -> str:
        """Assess business impact of violation"""
        impact_matrix = {
            ("missing_required", "high"): "Critical compliance failure - may result in regulatory penalties",
            ("missing_required", "medium"): "Moderate compliance risk - requires attention",
            ("invalid_type", "medium"): "Data quality issue - may cause processing errors",
            ("constraint_violation", "high"): "Business rule violation - may impact operations"
        }
        return impact_matrix.get((violation_type, severity), "Potential compliance or operational impact")
    
    def _determine_urgency(self, severity: str) -> str:
        """Determine urgency level"""
        urgency_map = {
            "high": "Immediate action required",
            "medium": "Address within 24 hours",
            "low": "Address within 1 week"
        }
        return urgency_map.get(severity, "Standard timeline")
    
    def _identify_stakeholders(self, field: str, violation_type: str) -> List[str]:
        """Identify relevant stakeholders"""
        stakeholder_map = {
            "email": ["Data Quality Team", "Customer Service"],
            "age": ["Compliance Team", "Legal Department"],
            "transaction_amount": ["Risk Management", "Finance Team"],
            "identity_documents": ["KYC Team", "Compliance Officer"]
        }
        return stakeholder_map.get(field, ["Compliance Team"])
    
    def _generate_summary(self, explanations: List[Dict[str, Any]]) -> str:
        """Generate summary of all explanations"""
        total_violations = len(explanations)
        high_severity = sum(1 for e in explanations if e.get("severity") == "high")
        
        return f"Found {total_violations} violations, {high_severity} of which are high severity and require immediate attention."
    
    def _calculate_overall_risk(self, violations: List[Dict[str, Any]]) -> str:
        """Calculate overall risk level"""
        high_count = sum(1 for v in violations if v.get("severity") == "high")
        medium_count = sum(1 for v in violations if v.get("severity") == "medium")
        
        if high_count > 0:
            return "high"
        elif medium_count > 2:
            return "medium"
        return "low"
    
    def _suggest_next_steps(self, explanations: List[Dict[str, Any]]) -> List[str]:
        """Suggest next steps"""
        steps = []
        
        high_severity_count = sum(1 for e in explanations if e.get("severity") == "high")
        if high_severity_count > 0:
            steps.append("Address high-severity violations immediately")
        
        steps.extend([
            "Review all violation explanations with relevant stakeholders",
            "Implement remediation plan",
            "Monitor for similar issues in the future"
        ])
        
        return steps
    
    def _parse_remediation_response(self, response: str) -> Dict[str, List[str]]:
        """Parse LLM remediation response"""
        # Simple parsing - in production, use more sophisticated NLP
        return {
            "immediate_actions": ["Fix data validation", "Update records"],
            "short_term_actions": ["Implement monitoring", "Train staff"],
            "long_term_actions": ["Improve processes", "Automate checks"],
            "preventive_measures": ["Regular audits", "Enhanced training"]
        }
    
    def _get_template_remediation(self, violation_type: str, field: str, severity: str) -> Dict[str, List[str]]:
        """Get template-based remediation"""
        return {
            "immediate_actions": [f"Fix {field} data issue", "Notify stakeholders"],
            "short_term_actions": [f"Implement {field} validation", "Update documentation"],
            "long_term_actions": ["Improve data quality processes", "Enhance monitoring"],
            "preventive_measures": ["Regular data audits", "Staff training"]
        }
    
    def _estimate_remediation_effort(self, plan: Dict[str, List[str]]) -> str:
        """Estimate effort required for remediation"""
        total_actions = sum(len(actions) for actions in plan.values())
        if total_actions > 10:
            return "High effort (2-4 weeks)"
        elif total_actions > 5:
            return "Medium effort (1-2 weeks)"
        return "Low effort (1-3 days)"
    
    def _define_success_metrics(self, violations: List[Dict[str, Any]]) -> List[str]:
        """Define success metrics for remediation"""
        return [
            "Zero high-severity violations",
            "95% data quality score",
            "All stakeholders notified",
            "Remediation plan 100% complete"
        ]
    
    def _create_timeline(self, plan: Dict[str, List[str]]) -> Dict[str, str]:
        """Create timeline for remediation"""
        return {
            "immediate_actions": "Within 24 hours",
            "short_term_actions": "Within 1 week",
            "long_term_actions": "Within 1 month",
            "preventive_measures": "Ongoing"
        }
    
    def _get_template_decision_explanation(self, decision: Dict[str, Any], factors: List[Dict[str, Any]]) -> str:
        """Get template decision explanation"""
        return f"Decision made based on {len(factors)} factors. Primary considerations included data quality, compliance requirements, and risk assessment."
    
    def _rank_decision_factors(self, factors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank decision factors by importance"""
        return sorted(factors, key=lambda x: x.get("weight", 0), reverse=True)
    
    def _generate_alternative_scenarios(self, decision: Dict[str, Any], factors: List[Dict[str, Any]]) -> List[str]:
        """Generate alternative scenarios"""
        return [
            "If data quality was higher, approval would be automatic",
            "If risk score was lower, fewer checks would be required",
            "If compliance requirements were different, decision might vary"
        ]
    
    def _create_audit_trail(self, decision: Dict[str, Any], factors: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """Create audit trail for decision"""
        return {
            "timestamp": "2024-01-01T00:00:00Z",
            "decision": decision,
            "factors": factors,
            "context": context,
            "agent": "ExplanationAgent"
        }
    
    def _get_template_risk_explanation(self, risk_level: str, risk_factors: List[Dict[str, Any]]) -> str:
        """Get template risk explanation"""
        return f"Risk level is {risk_level} based on {len(risk_factors)} contributing factors. This requires appropriate monitoring and controls."
    
    def _break_down_risk_factors(self, risk_factors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Break down risk factors"""
        return [
            {
                "factor": factor.get("factor", "unknown"),
                "weight": factor.get("weight", 0),
                "explanation": f"Contributes {factor.get('weight', 0)*100:.1f}% to overall risk"
            }
            for factor in risk_factors
        ]
    
    def _suggest_risk_mitigation(self, risk_factors: List[Dict[str, Any]]) -> List[str]:
        """Suggest risk mitigation strategies"""
        return [
            "Implement additional monitoring",
            "Require manual approval for high-risk cases",
            "Enhance data validation",
            "Regular risk assessment reviews"
        ]
    
    def _recommend_monitoring(self, risk_level: str, risk_factors: List[Dict[str, Any]]) -> List[str]:
        """Recommend monitoring strategies"""
        if risk_level == "high":
            return ["Real-time monitoring", "Daily risk reports", "Immediate alerts"]
        elif risk_level == "medium":
            return ["Weekly monitoring", "Trend analysis", "Threshold alerts"]
        return ["Monthly reviews", "Quarterly assessments"]
    
    def _define_escalation_triggers(self, risk_level: str) -> List[str]:
        """Define escalation triggers"""
        return [
            f"Risk score exceeds {risk_level} threshold",
            "Multiple violations detected",
            "Regulatory deadline approaching",
            "Stakeholder concerns raised"
        ]