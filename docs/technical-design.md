# Technical Design - AI-Powered Employee Onboarding

## 1. Design Decisions

### n8n as Workflow Orchestrator

n8n is responsible for coordinating the complete onboarding workflow, including triggering, validation, AI invocation, approvals, provisioning, retries, and exception handling.

This keeps the workflow visible and easier for People Ops and IT teams to understand and maintain.

### Claude as AI Decision Layer

Claude is used as an active decision-making component rather than only a chatbot.

It analyzes employee information and approved policies to:

- Create an onboarding action plan
- Determine standard onboarding actions
- Identify sensitive or non-standard access
- Generate onboarding communication
- Help classify and handle exceptions

Claude does not receive enterprise credentials or directly call enterprise APIs.

### MCP as Controlled Tool Layer

The MCP server provides controlled tools for enterprise operations.

This creates a security boundary between the AI layer and enterprise systems.

Only predefined and authorized operations can be executed through MCP.

### Human-in-the-Loop

Sensitive, privileged, or non-standard access requires human approval before execution.

This reduces the risk of the AI granting inappropriate access.

## 2. Failure Handling

Failures are classified into three categories:

- Transient failures
- Permanent failures
- Approval or policy failures

Transient failures are retried using exponential backoff.

Permanent failures are not repeatedly retried.

If provisioning succeeds in some systems but fails in another, the workflow records the successful operations and retries only the failed operation.

After repeated failures, a FreshService ticket is created for IT intervention.

## 3. Edge Cases

The workflow should handle:

- Missing employee information
- Duplicate employee records
- Invalid email addresses
- Unsupported departments or job roles
- Existing users in target systems
- API rate limits
- Target system downtime
- Partial provisioning failures
- Sensitive access requests
- AI returning an invalid or unexpected action
- Employee start-date changes

The workflow should not continue with provisioning when required employee information or authorization is missing.

## 4. Security and Governance

Security is based on least privilege.

Each integration uses a dedicated service identity with only the permissions required for onboarding.

Credentials and API secrets are stored in a secure secret manager and are never included in Claude prompts or normal application logs.

Claude can only request operations exposed through approved MCP tools.

All AI-generated actions are validated before execution.

Sensitive actions require human approval.

## 5. Auditability

Each onboarding execution receives a unique workflow execution ID.

The audit record contains:

- Employee ID
- Workflow execution ID
- Timestamp
- Target system
- Requested operation
- Execution result
- Retry count
- Approval status
- Error information
- Final workflow status

Secrets, passwords, access tokens, and other sensitive credentials are excluded from audit logs.

## 6. Future Improvements

With additional implementation time, the solution could be extended with:

- Automated evaluation of AI decisions
- More detailed onboarding policies
- Role-based access templates
- Better observability dashboards
- Dead-letter handling for failed workflows
- Automated reconciliation between Workday and target systems
- Approval workflows integrated with Slack or an internal portal
- More enterprise integrations
- Automated testing for MCP tools and workflow scenarios