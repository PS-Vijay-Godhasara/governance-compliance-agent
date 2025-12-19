# Business Scenarios & Use Cases

## Financial Services Scenarios

### Scenario 1: Customer Onboarding
**Business Context**: Bank needs to onboard new customers while ensuring KYC/AML compliance

**Workflow**:
```python
async def onboard_customer(customer_application):
    # Step 1: Policy validation
    policy_result = await orchestrator.validate("kyc_policy", customer_application)
    
    if not policy_result['data']['is_valid']:
        return {
            "status": "rejected",
            "reason": "Policy violations",
            "violations": policy_result['data']['violations']
        }
    
    # Step 2: KYC validation
    kyc_result = await orchestrator.perform_kyc_validation(customer_application)
    
    if kyc_result['kyc_status'] == "rejected":
        return {"status": "kyc_failed", "issues": kyc_result['issues']}
    
    # Step 3: Risk assessment
    risk_result = await orchestrator.assess_risk(customer_application)
    
    if risk_result['risk_level'] == "high":
        return {"status": "manual_review", "risk_factors": risk_result['risk_factors']}
    
    # Step 4: Approve onboarding
    return {"status": "approved", "customer_id": await create_customer_account()}
```

### Scenario 2: Transaction Monitoring
**Business Context**: Real-time transaction monitoring for suspicious activity

**Workflow**:
```python
async def monitor_transaction(transaction):
    # Assess transaction risk
    risk_assessment = await orchestrator.assess_risk(transaction, {
        "customer_history": await get_customer_history(transaction['customer_id']),
        "account_patterns": await analyze_account_patterns(transaction['customer_id'])
    })
    
    # Take action based on risk level
    if risk_assessment['risk_level'] == "high":
        # Hold transaction for review
        await hold_transaction(transaction['id'])
        await create_sar_case(transaction, risk_assessment)
        
    elif risk_assessment['risk_level'] == "medium":
        # Process with enhanced monitoring
        await process_transaction(transaction['id'])
        await flag_for_monitoring(transaction['customer_id'], 30)  # 30 days
        
    else:
        # Process normally
        await process_transaction(transaction['id'])
    
    return risk_assessment
```

## Healthcare Scenarios

### Scenario 3: Patient Data Validation
**Business Context**: Hospital needs to ensure patient data meets HIPAA requirements

**Workflow**:
```python
async def validate_patient_data(patient_record):
    # Define HIPAA policy
    hipaa_policy = """
    Patient data policy:
    - Patient name, DOB, and medical record number are required
    - SSN must be encrypted or masked
    - Diagnosis codes must be valid ICD-10 codes
    - Provider information must be complete
    - Audit trail must be maintained for all access
    """
    
    # Register policy
    policy_id = await orchestrator.register_policy("hipaa_compliance", hipaa_policy)
    
    # Validate patient data
    validation_result = await orchestrator.validate(policy_id, patient_record)
    
    if not validation_result['data']['is_valid']:
        # Generate compliance report
        compliance_report = {
            "patient_id": patient_record.get('id', 'unknown'),
            "violations": validation_result['data']['violations'],
            "explanations": validation_result['data'].get('explanations', []),
            "remediation_required": True,
            "compliance_officer_notified": True
        }
        
        await notify_compliance_officer(compliance_report)
        return compliance_report
    
    return {"status": "compliant", "patient_id": patient_record['id']}
```

## E-commerce Scenarios

### Scenario 4: Age Verification for Restricted Products
**Business Context**: Online retailer selling age-restricted products

**Workflow**:
```python
async def verify_age_restricted_purchase(customer_id, product_id, customer_data):
    # Get product age requirements
    product = await get_product(product_id)
    min_age = product.get('min_age', 18)
    
    # Create age verification policy
    age_policy = f"""
    Age verification policy:
    - Customer must be {min_age} years or older
    - Valid government-issued ID required
    - ID must not be expired
    - Age verification must be completed within last 30 days
    """
    
    policy_id = await orchestrator.register_policy(f"age_verification_{min_age}", age_policy)
    
    # Validate customer data
    validation_result = await orchestrator.validate(policy_id, customer_data)
    
    if validation_result['data']['is_valid']:
        return {"status": "approved", "can_purchase": True}
    else:
        return {
            "status": "age_verification_failed",
            "can_purchase": False,
            "required_actions": [
                "Upload valid government ID",
                "Complete age verification process"
            ]
        }
```

## Enterprise Data Scenarios

### Scenario 5: Data Quality Monitoring
**Business Context**: Enterprise monitoring data quality across multiple systems

**Workflow**:
```python
async def monitor_data_quality(dataset_name, data_batch):
    # Get data quality policy for dataset
    policy = await get_data_quality_policy(dataset_name)
    
    # Validate data batch
    results = []
    for record in data_batch:
        validation_result = await orchestrator.validate(policy['policy_id'], record)
        
        if not validation_result['data']['is_valid']:
            # Get detailed explanations
            explanations = validation_result['data'].get('explanations', [])
            
            # Create data quality issue
            issue = {
                "record_id": record.get('id'),
                "dataset": dataset_name,
                "violations": validation_result['data']['violations'],
                "explanations": explanations,
                "severity": calculate_severity(validation_result['data']['violations']),
                "timestamp": datetime.now().isoformat()
            }
            
            results.append(issue)
    
    # Generate data quality report
    quality_score = calculate_quality_score(data_batch, results)
    
    if quality_score < 0.95:  # Below 95% quality threshold
        await alert_data_team({
            "dataset": dataset_name,
            "quality_score": quality_score,
            "issues_count": len(results),
            "critical_issues": [r for r in results if r['severity'] == 'high']
        })
    
    return {
        "quality_score": quality_score,
        "total_records": len(data_batch),
        "issues_found": len(results),
        "issues": results
    }
```

### Scenario 6: Schema Migration Management
**Business Context**: Database schema changes across microservices

**Workflow**:
```python
async def manage_schema_migration(service_name, old_schema, new_schema):
    # Detect schema drift
    drift_result = await orchestrator.detect_schema_drift(old_schema, new_schema)
    
    if drift_result['compatibility'] == "breaking":
        # Generate migration plan
        migration_plan = await generate_migration_plan(drift_result['changes'])
        
        # Assess impact on dependent services
        impact_assessment = await assess_service_impact(service_name, drift_result['changes'])
        
        # Create migration workflow
        migration_workflow = {
            "service": service_name,
            "changes": drift_result['changes'],
            "migration_steps": migration_plan['steps'],
            "rollback_plan": migration_plan['rollback_steps'],
            "affected_services": impact_assessment['affected_services'],
            "estimated_downtime": migration_plan['estimated_duration'],
            "approval_required": True if drift_result['risk_level'] == "high" else False
        }
        
        if migration_workflow['approval_required']:
            await request_migration_approval(migration_workflow)
        else:
            await schedule_migration(migration_workflow)
        
        return migration_workflow
    
    else:
        # Non-breaking change - auto-deploy
        await deploy_schema_change(service_name, new_schema)
        return {"status": "auto_deployed", "risk_level": drift_result['risk_level']}
```

## Regulatory Compliance Scenarios

### Scenario 7: GDPR Compliance Check
**Business Context**: Ensuring customer data processing complies with GDPR

**Workflow**:
```python
async def check_gdpr_compliance(data_processing_request):
    gdpr_policy = """
    GDPR compliance policy:
    - Explicit consent must be obtained for data processing
    - Purpose of processing must be clearly defined
    - Data subject rights must be respected
    - Data retention period must be specified
    - Legal basis for processing must be documented
    - Data processor agreements must be in place for third parties
    """
    
    policy_id = await orchestrator.register_policy("gdpr_compliance", gdpr_policy)
    
    # Validate processing request
    compliance_result = await orchestrator.validate(policy_id, data_processing_request)
    
    if not compliance_result['data']['is_valid']:
        # Generate compliance report
        report = {
            "request_id": data_processing_request['id'],
            "compliance_status": "non_compliant",
            "violations": compliance_result['data']['violations'],
            "legal_risk": "high",
            "required_actions": [],
            "dpo_notification_required": True
        }
        
        # Extract required actions from explanations
        for explanation in compliance_result['data'].get('explanations', []):
            if 'remediation' in explanation:
                report['required_actions'].extend(explanation['remediation'])
        
        # Notify Data Protection Officer
        await notify_dpo(report)
        
        return report
    
    return {"status": "gdpr_compliant", "processing_approved": True}
```

## Integration Scenarios

### Scenario 8: Multi-System Validation Pipeline
**Business Context**: Validating data across multiple enterprise systems

**Workflow**:
```python
async def enterprise_validation_pipeline(data_payload, source_system):
    validation_results = {}
    
    # Step 1: Source system validation
    source_policy = await get_system_policy(source_system)
    source_result = await orchestrator.validate(source_policy['id'], data_payload)
    validation_results['source_validation'] = source_result
    
    # Step 2: Cross-system compatibility check
    target_systems = await get_target_systems(source_system)
    
    for target_system in target_systems:
        # Check schema compatibility
        source_schema = await get_system_schema(source_system)
        target_schema = await get_system_schema(target_system)
        
        compatibility = await orchestrator.detect_schema_drift(source_schema, target_schema)
        
        if compatibility['compatibility'] == "breaking":
            # Transform data for compatibility
            transformed_data = await transform_data(data_payload, compatibility['changes'])
            target_result = await validate_for_target_system(target_system, transformed_data)
        else:
            target_result = await validate_for_target_system(target_system, data_payload)
        
        validation_results[f'{target_system}_validation'] = target_result
    
    # Step 3: Generate overall compliance report
    overall_status = all(result['data']['is_valid'] for result in validation_results.values())
    
    return {
        "overall_compliant": overall_status,
        "system_results": validation_results,
        "data_flow_approved": overall_status,
        "transformation_required": any('transformed' in str(r) for r in validation_results.values())
    }
```

## Performance Monitoring Scenarios

### Scenario 9: Real-time Compliance Dashboard
**Business Context**: Real-time monitoring of compliance metrics

**Workflow**:
```python
async def update_compliance_dashboard():
    dashboard_metrics = {}
    
    # Get recent validation results
    recent_validations = await get_recent_validations(hours=24)
    
    # Calculate compliance metrics
    total_validations = len(recent_validations)
    successful_validations = sum(1 for v in recent_validations if v['is_valid'])
    compliance_rate = successful_validations / total_validations if total_validations > 0 else 0
    
    # Analyze violation patterns
    violations_by_type = {}
    for validation in recent_validations:
        for violation in validation.get('violations', []):
            violation_type = violation['type']
            violations_by_type[violation_type] = violations_by_type.get(violation_type, 0) + 1
    
    # Risk assessment trends
    risk_assessments = await get_recent_risk_assessments(hours=24)
    high_risk_count = sum(1 for r in risk_assessments if r['risk_level'] == 'high')
    
    # KYC processing metrics
    kyc_results = await get_recent_kyc_results(hours=24)
    kyc_approval_rate = sum(1 for k in kyc_results if k['status'] == 'approved') / len(kyc_results)
    
    dashboard_metrics = {
        "compliance_rate": compliance_rate,
        "total_validations_24h": total_validations,
        "violation_patterns": violations_by_type,
        "high_risk_transactions_24h": high_risk_count,
        "kyc_approval_rate_24h": kyc_approval_rate,
        "system_health": await check_system_health(),
        "last_updated": datetime.now().isoformat()
    }
    
    # Alert on concerning trends
    if compliance_rate < 0.90:
        await send_alert("Low compliance rate detected", dashboard_metrics)
    
    if high_risk_count > 50:  # Threshold for high-risk transactions
        await send_alert("High number of risky transactions", dashboard_metrics)
    
    return dashboard_metrics
```

## Error Recovery Scenarios

### Scenario 10: System Failure Recovery
**Business Context**: Handling system failures gracefully

**Workflow**:
```python
async def handle_validation_failure(data, policy_id, error):
    # Log the failure
    await log_system_failure({
        "error": str(error),
        "policy_id": policy_id,
        "data_hash": hash_data(data),
        "timestamp": datetime.now().isoformat()
    })
    
    # Attempt fallback validation
    try:
        # Use cached policy rules if available
        cached_policy = await get_cached_policy(policy_id)
        if cached_policy:
            fallback_result = await basic_validation(data, cached_policy['rules'])
            
            return {
                "status": "fallback_validation",
                "result": fallback_result,
                "warning": "Used cached policy due to system error",
                "manual_review_required": True
            }
    
    except Exception as fallback_error:
        # Complete fallback - queue for manual review
        await queue_for_manual_review({
            "data": data,
            "policy_id": policy_id,
            "original_error": str(error),
            "fallback_error": str(fallback_error),
            "priority": "high"
        })
        
        return {
            "status": "system_failure",
            "manual_review_queued": True,
            "error_reference": await generate_error_reference()
        }
```

These scenarios demonstrate how the agent-based governance system handles real-world business requirements across different industries and use cases.