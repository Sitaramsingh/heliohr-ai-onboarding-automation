# HeliosHR AI-Powered Employee Onboarding Architecture

## Architecture Overview

The onboarding workflow starts when a new hire becomes active in Workday. n8n acts as the workflow orchestration layer and coordinates validation, AI decision-making, approvals, provisioning, retries, and audit logging.

Claude acts as the AI decision and orchestration layer. It analyzes the employee information and determines the appropriate onboarding actions based on predefined policies.

Claude does not directly access enterprise systems. All enterprise operations are exposed through a secure MCP server with allow-listed tools and authorization controls.

## High-Level Architecture

```text
                         ┌─────────────────────┐
                         │       Workday       │
                         │  New Hire / Active  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │        n8n          │
                         │ Workflow Orchestrator│
                         └──────────┬──────────┘
                                    │
                         Validate Employee Data
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Prepare AI Context│
                         │ Employee + Policies │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │       Claude        │
                         │ AI Decision / Agent │
                         └──────────┬──────────┘
                                    │
                         Structured Action Plan
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Output Validation │
                         └──────────┬──────────┘
                                    │
                          ┌─────────┴─────────┐
                          │                   │
                    Standard Access     Sensitive Access
                          │                   │
                          │             Human Approval
                          │                   │
                          └─────────┬─────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      MCP Server     │
                         │ Secure Tool Layer   │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
       │    Okta     │       │   Google    │       │    Slack    │
       │ User/Groups │       │ Workspace   │       │ User/Access │
       └─────────────┘       └─────────────┘       └─────────────┘
              │
              │
              ▼
       ┌─────────────┐       ┌─────────────┐
       │    Jira     │       │ FreshService│
       │ User/Access │       │ Exceptions  │
       └─────────────┘       └─────────────┘

                         ┌─────────────────────┐
                         │ Audit / Monitoring  │
                         │ Execution + Results │
                         └─────────────────────┘