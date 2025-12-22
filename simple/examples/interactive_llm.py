"""Interactive LLM Communication Example"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from orchestrator import SimpleOrchestrator

class InteractiveLLMAgent:
    def __init__(self):
        self.orchestrator = SimpleOrchestrator(use_llm=True)
        self.conversation_history = []
    
    def chat_with_agent(self):
        """Interactive chat with governance agent"""
        print("Interactive Governance Agent with LLM")
        print("=" * 40)
        print("Ask questions about policies, validation, or compliance!")
        print("Type 'quit' to exit, 'help' for commands")
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            elif user_input.lower() == 'help':
                self.show_help()
                continue
            elif user_input.lower().startswith('validate'):
                self.handle_validation_request(user_input)
                continue
            elif user_input.lower().startswith('policy'):
                self.handle_policy_request(user_input)
                continue
            elif user_input.lower().startswith('explain'):
                self.handle_explanation_request(user_input)
                continue
            
            # General LLM conversation
            response = self.get_llm_response(user_input)
            print(f"Agent: {response}")
            
            self.conversation_history.append({
                "user": user_input,
                "agent": response
            })
    
    def get_llm_response(self, user_input):
        """Get LLM response for governance and validation queries"""
        if not self.orchestrator.engine.llm_service:
            return "LLM service not available. Please start Ollama with a model like 'llama3.2:3b'"
        
        # Create governance-focused prompt
        prompt = f"""You are a governance and validation expert assistant specializing in:
        
- Data validation and quality assurance
- Governance policy creation and enforcement
- Compliance validation (GDPR, KYC, AML, SOX)
- Risk governance and controls
- Automated validation workflows
- Data governance frameworks

User question: {user_input}

Provide expert guidance on governance and validation topics.
Keep responses practical and actionable for data governance professionals."""
        
        try:
            response = self.orchestrator.engine.llm_service._call_llm(prompt)
            return response if response != "LLM unavailable" else "I'm having trouble connecting to the LLM service."
        except Exception as e:
            return f"Error getting LLM response: {str(e)}"
    
    def handle_validation_request(self, user_input):
        """Handle validation requests"""
        print("Agent: I can help you validate data! Here are some examples:")
        
        # Show validation example
        sample_data = {
            "email": "user@example.com",
            "age": 25,
            "phone": "+1-555-0123"
        }
        
        result = self.orchestrator.validate("customer_onboarding", sample_data)
        print(f"Sample validation result: {result['summary']}")
        
        # Get LLM explanation
        if result['violations']:
            explanation = self.get_validation_explanation(result['violations'])
            print(f"Explanation: {explanation}")
    
    def handle_policy_request(self, user_input):
        """Handle policy-related requests"""
        policies = self.orchestrator.list_policies()
        print(f"Agent: Available policies: {', '.join(policies)}")
        
        # Get policy explanation
        if "customer" in user_input.lower():
            policy = self.orchestrator.get_policy("customer_onboarding")
            print(f"Customer onboarding policy has {len(policy.get('rules', []))} rules")
            
            # LLM explanation of policy
            if self.orchestrator.engine.llm_service:
                explanation = self.orchestrator.engine.llm_service._call_llm(
                    f"Explain this customer onboarding policy in simple terms: {policy}"
                )
                print(f"Policy explanation: {explanation}")
    
    def handle_explanation_request(self, user_input):
        """Handle explanation requests"""
        # Sample violation for demonstration
        sample_violations = ["Email format is invalid", "Age below minimum requirement"]
        
        if self.orchestrator.engine.llm_service:
            explanation = self.orchestrator.engine.llm_service.explain_violations(
                sample_violations, 
                {"email": "invalid", "age": 16}, 
                "Customer Onboarding"
            )
            print(f"Agent: {explanation.get('summary', 'Here are the issues explained:')}")
            for exp in explanation.get('explanations', []):
                print(f"- {exp.get('explanation', 'Issue explanation')}")
        else:
            print("Agent: LLM service needed for detailed explanations.")
    
    def get_validation_explanation(self, violations):
        """Get natural language explanation for violations"""
        if not self.orchestrator.engine.llm_service:
            return "Basic validation failed. Please check the data format."
        
        prompt = f"""Explain these validation violations in simple, helpful terms:
        
Violations: {violations}

Provide:
1. What went wrong
2. Why it matters
3. How to fix it

Keep it friendly and actionable."""
        
        return self.orchestrator.engine.llm_service._call_llm(prompt)
    
    def show_help(self):
        """Show available commands for governance and validation"""
        print("\nAvailable commands:")
        print("- 'validate' - Learn about data validation and quality")
        print("- 'policy' - Get information about governance policies")
        print("- 'explain' - Get explanations for validation violations")
        print("- 'help' - Show this help")
        print("- 'quit' - Exit the chat")
        print("\nOr ask questions about:")
        print("• Data validation and quality assurance")
        print("• Governance policy creation and enforcement")
        print("• Compliance validation (GDPR, KYC, AML)")
        print("• Risk governance and controls")
        print("• Automated validation workflows")

def demo_natural_language_suggestions():
    """Demo natural language suggestions"""
    print("\nNatural Language Suggestions Demo")
    print("=" * 35)
    
    orchestrator = SimpleOrchestrator(use_llm=True)
    
    # Test with invalid data
    invalid_data = {
        "email": "not-an-email",
        "age": 15,
        "phone": "123"
    }
    
    result = orchestrator.validate("customer_onboarding", invalid_data)
    
    print("Validation Result:")
    print(f"Valid: {result['is_valid']}")
    print(f"Summary: {result['summary']}")
    
    if result['explanations']:
        print("\nNatural Language Explanations:")
        for explanation in result['explanations']:
            print(f"- {explanation}")
    
    # Create policy from natural language
    print("\nCreating Policy from Natural Language:")
    policy_text = "Premium customers must have account balance over $50,000 and be members for at least 12 months"
    
    new_policy = orchestrator.create_policy(policy_text, "premium_customer_policy")
    if "error" not in new_policy:
        print(f"Created policy: {new_policy.get('description', 'Policy created successfully')}")
    else:
        print("Policy creation requires LLM service")

def sample_prompts():
    """Show sample prompts for interaction"""
    print("\nSample Prompts for Interactive Agent")
    print("=" * 37)
    
    prompts = [
        "What is GDPR and how does it affect customer data validation?",
        "Explain KYC requirements for financial services",
        "How do I validate email addresses in customer onboarding?",
        "What are the risk factors for high-value transactions?",
        "Create a policy for premium customer verification",
        "Why is my customer validation failing?",
        "What documents are needed for KYC compliance?",
        "How do I assess transaction risk automatically?",
        "Explain the difference between validation and verification",
        "What are best practices for data governance?"
    ]
    
    print("Try these sample prompts:")
    for i, prompt in enumerate(prompts, 1):
        print(f"{i:2d}. {prompt}")
    
    print("\nStart interactive mode with: python interactive_llm.py")

if __name__ == "__main__":
    # Check if user wants interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        agent = InteractiveLLMAgent()
        agent.chat_with_agent()
    else:
        # Run demos
        demo_natural_language_suggestions()
        sample_prompts()
        
        print("\nTo start interactive chat, run:")
        print("python interactive_llm.py --interactive")