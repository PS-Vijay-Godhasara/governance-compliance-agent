# Documentation Index

## Agent Documentation

### Individual Agents
- [Policy Agent](agents/policy-agent.md) - Natural language policy parsing
- [RAG Agent](agents/rag-agent.md) - Knowledge retrieval and context management  
- [Validation Agent](agents/validation-agent.md) - Data validation, KYC, and risk assessment
- [Schema Agent](agents/schema-agent.md) - Database schema evolution management
- [Explanation Agent](agents/explanation-agent.md) - Human-readable explanations

## User Guides

### End User Documentation
- [End User Guide](user-flows/end-user-guide.md) - Complete guide for business users
- [Workflow Diagrams](user-flows/workflow-diagrams.md) - Visual process flows and user journeys

## Integration Documentation

### Technical Integration
- [MCP Integration Guide](mcp-integration.md) - Model Context Protocol server integration
- [API Reference](../USAGE_GUIDE.md) - Complete API documentation
- [Architecture Overview](../AGENT_ARCHITECTURE.md) - System architecture details

## Quick Reference

### Common Tasks
1. **Create Policy**: Use Policy Agent to parse natural language
2. **Validate Data**: Use Validation Agent with policy rules
3. **Search Knowledge**: Use RAG Agent for context retrieval
4. **Assess Risk**: Use Validation Agent for risk scoring
5. **Detect Schema Changes**: Use Schema Agent for drift detection
6. **Get Explanations**: Use Explanation Agent for human-readable output

### Agent Communication Flow
```
User Request → Orchestrator → Specific Agent → Response → User
```

### MCP Tool Categories
- **Policy Tools**: parse_policy, validate_policy, get_policy
- **Knowledge Tools**: store_knowledge, retrieve_context, semantic_search
- **Validation Tools**: validate_data, kyc_validation, risk_assessment, compliance_check

## Getting Started

1. **Installation**: Follow [main README](../README.md) setup instructions
2. **Basic Usage**: See [Usage Guide](../USAGE_GUIDE.md) for examples
3. **Agent Details**: Review individual agent documentation
4. **Integration**: Use MCP server for external system integration

## Support

- **Examples**: See [examples/](../examples/) directory
- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for questions