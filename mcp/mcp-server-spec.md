# MCP Server Specification

## 1. Purpose

The MCP server provides a secure and controlled interface between the Claude agent and HeliosHR enterprise systems.

Claude does not directly access Okta, Google Workspace, Slack, or Jira APIs. Instead, it requests approved operations through MCP tools.

## 2. Exposed Tools

The MCP server exposes the following tools:

### create_okta_user

Creates an employee identity in Okta.

Input:
- employee_id
- first_name
- last_name
- email
- department
- job_title

### create_google_workspace_user

Creates the employee's Google Workspace account.

Input:
- employee_id
- name
- email
- department

### add_slack_user

Adds the employee to the organization's Slack workspace.

Input:
- employee_id
- email
- department

### grant_jira_access

Grants standard Jira access based on the employee's department and role.

Input:
- employee_id
- department
- job_title
- access_profile

### create_freshservice_ticket

Creates an IT ticket when an onboarding operation requires manual intervention.

Input:
- employee_id
- system
- error
- attempted_action
- severity

## 3. Security Controls

The MCP server should enforce:

- Authentication for every request
- Authorization based on service identity and allowed tools
- Least-privilege permissions
- Input validation
- Allow-listed operations
- No direct credential exposure to the LLM
- Audit logging for every tool invocation
- Sensitive actions requiring human approval

## 4. Tool Execution Flow

Claude requests an operation through an MCP tool.

The MCP server:

1. Authenticates the caller.
2. Validates the requested tool.
3. Validates the input parameters.
4. Checks authorization and access policy.
5. Executes the operation against the target system.
6. Returns a structured result.
7. Records the operation in the audit log.