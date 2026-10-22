# AI Usage Statement

## AI Tools Used

I used AI assistance during the development of this take-home assignment to support:

- Understanding and breaking down the assignment requirements
- Designing the employee onboarding architecture
- Structuring the technical design and implementation specification
- Reviewing the role of Claude as an active AI decision layer
- Designing the MCP server and controlled tool interface
- Drafting the Python prototype structure
- Reviewing error handling, security, governance, and auditability considerations
- Improving documentation clarity and readability

## Validation and Refinement

AI-generated suggestions were reviewed and adapted to the specific HeliosHR onboarding scenario.

I validated the prototype by running it locally and confirming that:

1. Employee data validation works.
2. The onboarding plan is generated.
3. MCP tools are restricted to an allow-list.
4. The simulated enterprise provisioning actions execute successfully.
5. The workflow produces a final onboarding status.

The prototype was executed successfully using Python 3.14.7.

## Where AI Was Not Used

AI was not used as a replacement for implementation validation.

The Python prototype was executed locally to verify that the workflow and tool execution logic work as expected.

The final architecture and design decisions were reviewed against the assignment requirements and adjusted to ensure that security, human approval, error handling, and auditability were explicitly addressed.

## AI Design Principle

The key principle used in the solution is:

> AI decides and recommends; controlled automation validates and executes.

Claude is therefore treated as an active participant in the onboarding workflow while MCP and n8n provide controlled execution and governance boundaries.

## Where I Chose Not to Use AI

I did not use AI to make final decisions about security controls,
access governance, retry behavior, or enterprise authorization.

These decisions were reviewed and defined explicitly because they
affect system safety, permissions, and operational behavior.

I also manually tested the Python prototype and reviewed its output
instead of relying only on AI-generated code.