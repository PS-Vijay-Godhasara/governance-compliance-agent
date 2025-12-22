"""Sample Prompts for Governance and Validation Agent"""

# Sample prompts specifically for governance and validation agent functionality
# Use these with: python examples/interactive_llm.py --interactive

DATA_VALIDATION_PROMPTS = [
    "How do I validate customer data for compliance?",
    "What validation rules should I apply for email addresses?",
    "How do I ensure data quality in customer onboarding?",
    "What are the mandatory fields for customer validation?",
    "How do I validate phone numbers for international customers?",
    "What data types are supported in validation rules?",
    "How do I set up validation constraints for age verification?",
    "What happens when validation fails?",
]

GOVERNANCE_POLICY_PROMPTS = [
    "How do I create governance policies for data validation?",
    "What are the key components of a governance policy?",
    "How do I enforce data governance rules automatically?",
    "What governance frameworks should I follow?",
    "How do I ensure policy compliance across different regions?",
    "What are governance best practices for financial data?",
    "How do I audit governance policy effectiveness?",
    "How do I update governance policies without breaking existing workflows?",
]

COMPLIANCE_VALIDATION_PROMPTS = [
    "How do I validate data for GDPR compliance?",
    "What validation checks are needed for KYC compliance?",
    "How do I ensure AML compliance in transaction validation?",
    "What data validation is required for SOX compliance?",
    "How do I validate customer consent for data processing?",
    "What compliance violations should trigger alerts?",
    "How do I validate data retention policies?",
    "What validation is needed for cross-border data transfers?",
]

RISK_GOVERNANCE_PROMPTS = [
    "How do I assess data quality risks in governance?",
    "What risk factors should trigger additional validation?",
    "How do I validate high-risk customer transactions?",
    "What governance controls reduce operational risk?",
    "How do I validate risk scoring models?",
    "What data validation prevents compliance risks?",
    "How do I govern third-party data validation?",
    "What validation ensures data lineage governance?",
]

VALIDATION_RULES_PROMPTS = [
    "How do I create custom validation rules?",
    "What validation patterns work best for financial data?",
    "How do I validate data against multiple policies?",
    "What are the validation rule priorities?",
    "How do I handle validation rule conflicts?",
    "What validation rules prevent data breaches?",
    "How do I validate data transformations?",
    "What validation ensures data consistency?",
]

GOVERNANCE_AUTOMATION_PROMPTS = [
    "How do I automate governance policy enforcement?",
    "What validation processes can be automated?",
    "How do I set up automated compliance monitoring?",
    "What governance workflows need human oversight?",
    "How do I automate data quality validation?",
    "What validation alerts should be automated?",
    "How do I automate policy violation responses?",
    "What governance metrics should be automated?",
]

DATA_QUALITY_PROMPTS = [
    "How do I validate data completeness?",
    "What validation checks ensure data accuracy?",
    "How do I validate data consistency across systems?",
    "What validation prevents duplicate records?",
    "How do I validate data freshness and timeliness?",
    "What validation ensures data integrity?",
    "How do I validate data format standardization?",
    "What validation catches data anomalies?",
]

POLICY_CREATION_PROMPTS = [
    "Create a governance policy for customer data validation",
    "Generate validation rules for financial transaction data",
    "Create a policy for PII data governance",
    "Generate validation rules for regulatory reporting data",
    "Create a governance policy for data retention",
    "Generate validation rules for cross-border data transfers",
    "Create a policy for third-party data validation",
    "Generate validation rules for sensitive data handling",
]

VALIDATION_TROUBLESHOOTING_PROMPTS = [
    "Why is my data validation failing?",
    "How do I debug governance policy violations?",
    "What causes validation performance issues?",
    "How do I resolve validation rule conflicts?",
    "Why are validation scores inconsistent?",
    "How do I fix data quality validation errors?",
    "What validation logs should I check?",
    "How do I optimize validation rule performance?",
]

SAMPLE_CONVERSATIONS = [
    {
        "user": "How do I validate customer data for GDPR compliance?",
        "expected_topics": ["data validation", "GDPR requirements", "consent validation", "data minimization"]
    },
    {
        "user": "Create a governance policy for financial transaction validation",
        "expected_topics": ["policy creation", "financial data governance", "validation rules", "compliance"]
    },
    {
        "user": "Why is my data validation failing?",
        "expected_topics": ["validation troubleshooting", "rule conflicts", "data quality issues", "debugging"]
    },
    {
        "user": "What validation rules prevent compliance violations?",
        "expected_topics": ["compliance validation", "risk prevention", "governance controls", "regulatory requirements"]
    },
    {
        "user": "How do I automate governance policy enforcement?",
        "expected_topics": ["automation", "policy enforcement", "workflow orchestration", "monitoring"]
    }
]

def print_sample_prompts():
    """Print categorized sample prompts for governance and validation"""
    categories = [
        ("Data Validation", DATA_VALIDATION_PROMPTS),
        ("Governance Policies", GOVERNANCE_POLICY_PROMPTS),
        ("Compliance Validation", COMPLIANCE_VALIDATION_PROMPTS),
        ("Risk Governance", RISK_GOVERNANCE_PROMPTS),
        ("Validation Rules", VALIDATION_RULES_PROMPTS),
        ("Governance Automation", GOVERNANCE_AUTOMATION_PROMPTS),
        ("Data Quality", DATA_QUALITY_PROMPTS),
        ("Policy Creation", POLICY_CREATION_PROMPTS),
        ("Validation Troubleshooting", VALIDATION_TROUBLESHOOTING_PROMPTS),
    ]
    
    print("Sample Prompts for Governance and Validation Agent")
    print("=" * 50)
    
    for category, prompts in categories:
        print(f"\n{category}:")
        print("-" * len(category))
        for i, prompt in enumerate(prompts[:5], 1):  # Show first 5 of each category
            print(f"{i}. {prompt}")
        if len(prompts) > 5:
            print(f"   ... and {len(prompts) - 5} more")
    
    print(f"\nTotal sample prompts: {sum(len(prompts) for _, prompts in categories)}")
    print("\nTo use these prompts:")
    print("1. Run: python examples/interactive_llm.py --interactive")
    print("2. Copy and paste any prompt above")
    print("3. Or ask your own governance and validation questions!")

def get_random_prompt(category=None):
    """Get a random prompt from specified category or all categories"""
    import random
    
    all_prompts = {
        "data_validation": DATA_VALIDATION_PROMPTS,
        "governance": GOVERNANCE_POLICY_PROMPTS,
        "compliance": COMPLIANCE_VALIDATION_PROMPTS,
        "risk": RISK_GOVERNANCE_PROMPTS,
        "rules": VALIDATION_RULES_PROMPTS,
        "automation": GOVERNANCE_AUTOMATION_PROMPTS,
        "quality": DATA_QUALITY_PROMPTS,
        "creation": POLICY_CREATION_PROMPTS,
        "troubleshooting": VALIDATION_TROUBLESHOOTING_PROMPTS,
    }
    
    if category and category in all_prompts:
        return random.choice(all_prompts[category])
    else:
        # Random from all categories
        all_prompt_lists = list(all_prompts.values())
        random_category = random.choice(all_prompt_lists)
        return random.choice(random_category)

if __name__ == "__main__":
    print_sample_prompts()
    
    print(f"\nRandom prompt: {get_random_prompt()}")
    print(f"Random data validation prompt: {get_random_prompt('data_validation')}")
    print(f"Random governance prompt: {get_random_prompt('governance')}")