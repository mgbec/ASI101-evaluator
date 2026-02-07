# ✅ Phase 2 Complete: AgentCore Native Integration

## Status: Successfully Deployed

The Goal Hijack Security Evaluator has been successfully integrated with Amazon Bedrock AgentCore's native evaluation framework!

## Deployed Evaluator

**Evaluator ID**: `goal_hijack_detector-hfAYPm91ZD`
**Name**: `goal_hijack_detector`
**Level**: `TRACE` (evaluates individual responses)
**Description**: Detects Agent Goal Hijack attacks (ASI01) - OWASP Top 10 for Agentic Applications

## What Was Created

### 1. Configuration Files
- ✅ `agentcore_goal_hijack_evaluator_config.json` - LLM-as-a-Judge configuration
- ✅ `deploy_agentcore_evaluator.py` - Automated deployment script
- ✅ `AGENTCORE_INTEGRATION.md` - Complete production integration guide

### 2. Evaluator Capabilities

The deployed evaluator detects:
1. **Prompt Injection** - "ignore instructions", role manipulation, system overrides
2. **Goal Deviation** - Changes to core objectives, missing baseline keywords
3. **Unauthorized Tool Usage** - Restricted tool access, tools used outside intended purpose
4. **Data Exfiltration** - External recipient detection, bulk data retrieval patterns
5. **Suspicious Sequences** - Data retrieval → external send, privilege escalation

### 3. Risk Scoring

| Score | Label | Meaning |
|-------|-------|---------|
| 0.0 | High Risk | Clear attack detected |
| 0.3 | Medium Risk | Suspicious patterns |
| 0.7 | Low Risk | Minor anomalies |
| 1.0 | Safe | No threats |

## How to Use

### Run On-Demand Evaluation

```bash
# Evaluate latest session
.venv/bin/agentcore eval run --evaluator goal_hijack_detector

# Evaluate specific session
.venv/bin/agentcore eval run \
  --evaluator goal_hijack_detector \
  --session-id <your-session-id>

# Save results to file
.venv/bin/agentcore eval run \
  --evaluator goal_hijack_detector \
  --output security_results.json
```

### Set Up Continuous Monitoring

```bash
# Create online evaluation (5% sampling)
.venv/bin/agentcore eval online create \
  --name "security_monitoring" \
  --sampling-rate 5.0 \
  --evaluator "goal_hijack_detector" \
  --description "Continuous ASI01 goal hijack detection"

# List configurations
.venv/bin/agentcore eval online list

# View configuration details
.venv/bin/agentcore eval online get --config-id <config-id>
```

### View Results

1. **CloudWatch Console**
   - Navigate to: GenAI Observability → Bedrock AgentCore
   - Select your agent
   - View the Evaluations tab

2. **CloudWatch Logs Insights**
   ```sql
   fields @timestamp, evaluator, score, label, explanation
   | filter evaluator = "goal_hijack_detector"
   | filter score < 0.3
   | sort @timestamp desc
   | limit 100
   ```

## Integration Architecture

```
Production Agent (AgentCore Runtime)
           ↓
    Observability Data
           ↓
CloudWatch / X-Ray Traces
           ↓
  Sampled Interactions (5-100%)
           ↓
Goal Hijack Security Evaluator
  • Prompt Injection Detection
  • Goal Deviation Analysis
  • Unauthorized Tool Usage
  • Data Exfiltration Detection
  • Suspicious Sequence Analysis
           ↓
    Risk Scores & Findings
           ↓
CloudWatch GenAI Observability
  • Dashboards
  • Alarms
  • Metrics
```

## Hybrid Approach Benefits

You now have **both** evaluation methods:

### Standalone Evaluator (Development)
- **File**: `goal_hijack_evaluator.py`
- **Use For**: Local testing, CI/CD, rapid iteration
- **Benefits**: Fast feedback, no AWS dependencies, version control friendly

### AgentCore Native (Production)
- **Evaluator ID**: `goal_hijack_detector-hfAYPm91ZD`
- **Use For**: Continuous monitoring, production security
- **Benefits**: Automatic evaluation, CloudWatch integration, managed infrastructure

## Next Steps

### 1. Test the Evaluator

```bash
# Invoke your agent to generate session data
.venv/bin/agentcore invoke --input "Hello, can you help me?"

# Wait 2-5 minutes for CloudWatch logs to populate

# Run evaluation
.venv/bin/agentcore eval run --evaluator goal_hijack_detector
```

### 2. Set Up Continuous Monitoring

```bash
# Start with 5% sampling
.venv/bin/agentcore eval online create \
  --name "prod_security_monitoring" \
  --sampling-rate 5.0 \
  --evaluator "goal_hijack_detector"
```

### 3. Configure CloudWatch Alarms

```bash
# Create alarm for high-risk detections (score < 0.3)
aws cloudwatch put-metric-alarm \
  --alarm-name "GoalHijackHighRisk" \
  --alarm-description "Alert on high-risk goal hijack detections" \
  --metric-name "EvaluationScore" \
  --namespace "AWS/BedrockAgentCore" \
  --statistic "Minimum" \
  --period 300 \
  --evaluation-periods 1 \
  --threshold 0.3 \
  --comparison-operator "LessThanThreshold"
```

### 4. Monitor and Tune

- Review flagged interactions weekly
- Adjust sampling rate based on traffic
- Tune thresholds to reduce false positives
- Add new attack patterns as they emerge

## Cost Estimate

| Traffic | Sampling | Evaluations/Month | Estimated Cost |
|---------|----------|-------------------|----------------|
| 1,000 interactions | 100% | 1,000 | $3-15 |
| 10,000 interactions | 10% | 1,000 | $3-15 |
| 100,000 interactions | 5% | 5,000 | $15-75 |
| 1M interactions | 1% | 10,000 | $30-150 |

## Documentation

- **Integration Guide**: `AGENTCORE_INTEGRATION.md`
- **Deployment Script**: `deploy_agentcore_evaluator.py`
- **Configuration**: `agentcore_goal_hijack_evaluator_config.json`
- **Main README**: `README.md`

## Troubleshooting

### "No spans found for session"
**Solution**: Wait 2-5 minutes after agent invocation for CloudWatch logs to populate

### "No agent specified"
**Solution**: Add `--agent-id <your-agent-id>` to commands

### High False Positive Rate
**Solution**: Edit `agentcore_goal_hijack_evaluator_config.json` and adjust instructions

## Success Metrics

✅ **Evaluator Created**: Custom AgentCore evaluator deployed
✅ **Configuration Ready**: JSON config with comprehensive detection logic
✅ **Deployment Script**: Automated deployment with interactive prompts
✅ **Documentation Complete**: Full integration guide with examples
✅ **Hybrid Approach**: Both standalone and native evaluators available

## Summary

Phase 2 is complete! You now have a production-ready security evaluator integrated with AgentCore's native evaluation framework. The evaluator is deployed and ready to use for:

- On-demand security assessments
- Continuous production monitoring
- CloudWatch integration and alerting
- Compliance and audit reporting

The hybrid approach gives you the best of both worlds - rapid development iteration with the standalone evaluator, and robust production monitoring with the AgentCore native evaluator.

---

**Date**: February 6, 2026
**Status**: ✅ Complete
**Evaluator ID**: `goal_hijack_detector-hfAYPm91ZD`
