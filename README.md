# HeliosHR AI Employee Onboarding Automation

An AI-powered employee onboarding automation solution designed for HeliosHR, a 600-person B2B SaaS company.

The solution automates employee onboarding from Workday through enterprise systems such as Okta, Google Workspace, Slack, and Jira, while using Claude as an AI decision/orchestration layer and MCP as a controlled execution boundary.

---

## 1. Problem

The current onboarding process is largely manual.

When a new employee joins:

1. HR updates the employee record.
2. IT receives the onboarding information.
3. IT manually provisions access across multiple systems.
4. IT follows up when provisioning fails.
5. Access decisions and onboarding actions may require manual tracking.

This process can take **3–5 business days** and can result in errors or inconsistent access.

---

## 2. Proposed Solution

The proposed solution automates the onboarding workflow using:

- **Workday** as the employee source of truth
- **n8n** as the workflow orchestrator
- **Claude** as the AI decision and planning layer
- **MCP Server** as the controlled tool execution layer
- **Okta** for identity provisioning
- **Google Workspace** for corporate accounts
- **Slack** for collaboration access
- **Jira** for engineering access
- **FreshService** for exception handling and IT escalation

### High-Level Flow

```text
Workday
   |
   v
n8n Workflow
   |
   v
Validate Employee Data
   |
   v
Claude AI Agent
   |
   v
Validate AI Output
   |
   +----------------------+
   |                      |
   v                      v
Standard Access      Sensitive /
                     Non-standard
                     Access
                          |
                          v
                    Human Approval
                          |
                          v
                    MCP Server
                          |
          +---------------+---------------+
          |               |               |
          v               v               v
        Okta       Google Workspace     Slack
          |
          v
        Jira
          |
          v
    Result Handling
          |
     +----+----+
     |         |
   Success   Failure
     |         |
     v         v
 Audit      Retry
              |
              v
        FreshService
```

---

## 3. Why Claude Is Used

Claude is not used only as a chatbot.

It acts as an **AI onboarding decision and planning layer**.

Claude receives:

- Validated employee information
- Department
- Job title
- Approved access policies
- Standard onboarding rules

Claude creates a structured onboarding plan containing:

- Required actions
- Reason for each action
- Whether human approval is required
- Overall execution status

For example, an Engineering employee may require Jira access while another department may not.

The key design principle is:

> **AI decides and recommends; controlled automation validates and executes.**

Claude does not receive enterprise credentials and does not directly call enterprise APIs.

---

## 4. MCP Security Boundary

The MCP server provides a controlled interface between the AI layer and enterprise systems.

Example MCP tools:

```text
create_okta_user
create_google_workspace_user
add_slack_user
grant_jira_access
create_freshservice_ticket
```

The MCP layer:

1. Authenticates the request.
2. Validates the requested tool.
3. Checks the tool against an allow-list.
4. Validates inputs.
5. Applies authorization and policy checks.
6. Executes the operation.
7. Returns a structured result.
8. Records the operation for audit.

This prevents Claude from having unrestricted access to enterprise systems.

---

## 5. Security and Governance

The solution follows a least-privilege approach.

### Key controls

- Dedicated service identities
- Role-based access
- Approved MCP tools only
- Input validation
- AI output validation
- Human approval for sensitive or non-standard access
- Centralized secret management
- No passwords or API keys in AI prompts
- No credentials in application logs
- Audit trail for provisioning actions

Sensitive or privileged access should never be automatically granted only because the AI requested it.

---

## 6. Error Handling

The workflow categorizes failures into:

### Transient failures

Examples:

- Temporary API failure
- Rate limiting
- Temporary service outage

These can be retried using exponential backoff.

Example:

```text
Attempt 1
   |
   v
Failure
   |
   v
Retry
   |
   v
Success
```

The prototype demonstrates this using a simulated Jira failure.

Example output:

```text
[MCP] Temporary failure: grant_jira_access
[Retry] Retrying grant_jira_access...
[MCP] Executing: grant_jira_access for john.doe@helioshr.com
```

### Permanent failures

Examples:

- Invalid employee data
- Unsupported department
- Unauthorized action
- Invalid tool request

These should not be repeatedly retried.

### Escalation

If retries are exhausted, the workflow can create a FreshService ticket for IT intervention.

---

## 7. Idempotency

The onboarding workflow should be safe to retry.

The Workday employee ID is used as the primary onboarding identifier.

Before creating an account or granting access, the implementation should check whether the operation has already been completed.

This prevents duplicate provisioning when:

- n8n retries a workflow
- an API times out after successfully completing an operation
- a workflow is manually restarted

---

## 8. Auditability

Every important onboarding operation should be recorded.

Example audit information:

```text
Employee ID
Workflow Execution ID
Timestamp
Target System
Operation
Result
Failure Type
Retry Count
Approval Status
Final Status
```

This provides visibility into who/what performed each onboarding action and helps with troubleshooting and compliance.

---

## 9. Repository Structure

```text
heliohr-ai-onboarding-automation/
│
├── README.md
├── AI-USAGE.md
│
├── architecture/
│   └── architecture.md
│
├── data/
│   └── sample_documents/
│       └── loan_policy.txt
│
├── docs/
│   ├── executive-summary.md
│   ├── implementation-spec.md
│   └── technical-design.md
│
├── mcp/
│   └── mcp-server-spec.md
│
└── prototype/
    └── onboarding_workflow.py
```

---

## 10. Prototype

The Python prototype demonstrates the core workflow without requiring live enterprise credentials.

It demonstrates:

- Employee validation
- AI onboarding plan generation
- AI output validation
- MCP tool allow-list
- Role-based action selection
- Human approval handling
- Simulated enterprise provisioning
- Transient failure
- Retry handling
- Audit information

### Run the prototype

From the repository root:

```powershell
py prototype/onboarding_workflow.py
```

### Example successful execution

```text
=== HeliosHR Employee Onboarding ===

[1] Validating employee data...
Validation successful.

[2] Claude creating onboarding plan...
Claude generated actions:
 - create_okta_user: Create enterprise identity
 - create_google_workspace_user: Create corporate Google account
 - add_slack_user: Provide standard collaboration access
 - grant_jira_access: Engineering role requires Jira access

[3] Validating Claude output...
AI output validation successful.

[4] MCP executing approved tools...
[MCP] Executing: create_okta_user for john.doe@helioshr.com
[MCP] Executing: create_google_workspace_user for john.doe@helioshr.com
[MCP] Executing: add_slack_user for john.doe@helioshr.com
[MCP] Temporary failure: grant_jira_access
[Retry] Retrying grant_jira_access...
[MCP] Executing: grant_jira_access for john.doe@helioshr.com

[5] Onboarding result
Onboarding completed successfully.
```

---

## 11. Expected Business Improvement

The following are **pilot targets**, not guaranteed production results.

| KPI | Current State | Pilot Target |
|---|---|---|
| Onboarding completion time | 3–5 business days | Same business day |
| Manual provisioning effort | Multiple manual steps | Majority automated |
| Provisioning failure handling | Manual follow-up | Automated retry + escalation |
| Access errors | Tracked through incidents | Measure reduction in onboarding-related incidents |
| Human approval | Manual decision-making | Only for sensitive/non-standard access |
| Audit coverage | Distributed/manual | Every workflow action recorded |

### Success Metrics

During a pilot, measure:

- Average onboarding completion time
- Number of manual IT actions
- Percentage of workflows completed without intervention
- Failure rate by target system
- Number of incorrect or missing access incidents
- Percentage of workflows requiring human approval
- Mean time to resolve provisioning failures

---

## 12. Limitations and Assumptions

This submission is a design/prototype rather than a production deployment.

The prototype does not use live credentials or real enterprise APIs.

The following would need to be confirmed during production implementation:

- Exact Workday integration mechanism
- Okta API configuration
- Google Workspace authentication
- Slack provisioning API
- Jira API permissions
- FreshService API configuration
- Enterprise identity and secret-management standards
- Final access-control policies
- Human approval workflow

The prototype intentionally focuses on demonstrating the architecture, AI role, MCP boundary, governance, error handling, and implementation approach.

---

## 13. Future Improvements

Potential production enhancements include:

- Real Workday event integration
- Real MCP server implementation
- Production n8n workflows
- Centralized policy management
- Automated reconciliation
- Dead-letter queue for failed workflows
- Provisioning dashboard
- AI evaluation and monitoring
- More enterprise integrations
- Automated access reviews
- Slack or internal portal approval workflows
- Detailed onboarding analytics

---

## 14. Documentation

Additional design details are available in:

- `architecture/architecture.md` — Architecture and data flow
- `docs/technical-design.md` — Technical design and failure handling
- `docs/implementation-spec.md` — Detailed implementation approach
- `docs/executive-summary.md` — Executive-level solution summary
- `mcp/mcp-server-spec.md` — MCP server and tool design
- `AI-USAGE.md` — AI tools used and validation approach

---

## 15. Design Principle

The central design principle of this solution is:

> **AI decides and recommends. Controlled automation validates and executes.**

This keeps the benefits of AI-driven decision making while maintaining security, governance, auditability, and human control over sensitive enterprise access.
```

After saving the file, **don't commit yet**.

Run:

```powershell
git status
```

Send me the output.