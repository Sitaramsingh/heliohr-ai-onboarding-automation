"""
HeliosHR - AI Powered Employee Onboarding Prototype

Simulated flow:

Workday
   ↓
n8n
   ↓
Employee Validation
   ↓
Claude AI Agent
   ↓
AI Output Validation
   ↓
MCP Server
   ↓
Okta / Google Workspace / Slack / Jira
   ↓
Retry / Exception Handling
   ↓
Audit Result
"""

from dataclasses import dataclass
from typing import List, Dict


# ---------------------------------------------------------
# Employee Model
# ---------------------------------------------------------

@dataclass
class Employee:
    employee_id: str
    name: str
    email: str
    department: str
    job_title: str
    manager: str
    start_date: str


# ---------------------------------------------------------
# Employee Validation
# ---------------------------------------------------------

def validate_employee(employee: Employee) -> List[str]:
    """Validate required employee information."""

    errors = []

    required_fields = {
        "employee_id": employee.employee_id,
        "name": employee.name,
        "email": employee.email,
        "department": employee.department,
        "job_title": employee.job_title,
        "manager": employee.manager,
        "start_date": employee.start_date,
    }

    for field, value in required_fields.items():
        if not value:
            errors.append(
                f"Missing required field: {field}"
            )

    if "@" not in employee.email:
        errors.append(
            "Invalid email address"
        )

    return errors


# ---------------------------------------------------------
# Claude AI Agent
# ---------------------------------------------------------

def claude_create_onboarding_plan(
    employee: Employee,
) -> Dict:
    """
    Simulates Claude creating an onboarding plan.

    In the real implementation, Claude would receive:
    - Validated employee information
    - Approved access policies

    Claude would then return a structured action plan.
    """

    actions = [
        {
            "tool": "create_okta_user",
            "reason": "Create enterprise identity",
            "requires_approval": False,
        },
        {
            "tool": "create_google_workspace_user",
            "reason": "Create corporate Google account",
            "requires_approval": False,
        },
        {
            "tool": "add_slack_user",
            "reason": "Provide standard collaboration access",
            "requires_approval": False,
        },
    ]

    # Role-based decision
    if employee.department.lower() == "engineering":
        actions.append(
            {
                "tool": "grant_jira_access",
                "reason": "Engineering role requires Jira access",
                "requires_approval": False,
            }
        )

    return {
        "employee_id": employee.employee_id,
        "actions": actions,
        "requires_human_approval": False,
        "status": "READY_FOR_EXECUTION",
    }


# ---------------------------------------------------------
# AI Output Validation
# ---------------------------------------------------------

def validate_ai_output(
    plan: Dict,
    employee: Employee,
) -> List[str]:
    """Validate Claude's structured output before execution."""

    errors = []

    # Make sure the AI is acting on the correct employee
    if plan.get("employee_id") != employee.employee_id:
        errors.append(
            "Employee ID does not match onboarding request"
        )

    # Make sure actions exist
    if "actions" not in plan:
        errors.append(
            "AI response does not contain actions"
        )
        return errors

    # MCP allow-list
    allowed_tools = {
        "create_okta_user",
        "create_google_workspace_user",
        "add_slack_user",
        "grant_jira_access",
        "create_freshservice_ticket",
    }

    for action in plan["actions"]:

        tool_name = action.get("tool")

        if tool_name not in allowed_tools:
            errors.append(
                f"Unsupported tool requested: {tool_name}"
            )

        if "reason" not in action:
            errors.append(
                f"Missing reason for tool: {tool_name}"
            )

        if "requires_approval" not in action:
            errors.append(
                f"Missing approval flag for tool: {tool_name}"
            )

    return errors


# ---------------------------------------------------------
# MCP Server
# ---------------------------------------------------------

class MCPServer:
    """
    Simulated MCP server exposing controlled
    enterprise provisioning tools.
    """

    ALLOWED_TOOLS = {
        "create_okta_user",
        "create_google_workspace_user",
        "add_slack_user",
        "grant_jira_access",
        "create_freshservice_ticket",
    }

    def __init__(self):
        # Used to simulate a temporary Jira failure.
        self.jira_attempts = 0

    def execute_tool(
        self,
        tool_name: str,
        employee: Employee,
    ) -> Dict:
        """
        Validate and execute an approved MCP tool.
        """

        # -------------------------------------------------
        # MCP allow-list validation
        # -------------------------------------------------

        if tool_name not in self.ALLOWED_TOOLS:
            return {
                "success": False,
                "tool": tool_name,
                "employee_id": employee.employee_id,
                "error": "Tool is not allowed",
                "failure_type": "permanent",
            }

        # -------------------------------------------------
        # Simulate one transient Jira failure
        # -------------------------------------------------

        if tool_name == "grant_jira_access":

            self.jira_attempts += 1

            if self.jira_attempts == 1:

                print(
                    "[MCP] Temporary failure: "
                    "grant_jira_access"
                )

                return {
                    "success": False,
                    "tool": tool_name,
                    "employee_id": employee.employee_id,
                    "error": "Temporary Jira API failure",
                    "failure_type": "transient",
                }

        # -------------------------------------------------
        # Simulated successful provisioning
        # -------------------------------------------------

        print(
            f"[MCP] Executing: {tool_name} "
            f"for {employee.email}"
        )

        return {
            "success": True,
            "tool": tool_name,
            "employee_id": employee.employee_id,
        }


# ---------------------------------------------------------
# Human Approval
# ---------------------------------------------------------

def check_human_approval(
    action: Dict,
) -> bool:
    """
    Simulate human approval for sensitive actions.

    In production this could be implemented through
    Slack, n8n approval nodes, or an internal approval UI.
    """

    if action.get("requires_approval"):

        print(
            f"[Approval] Human approval required for "
            f"{action['tool']}"
        )

        # Simulated approval
        print(
            f"[Approval] Approved: {action['tool']}"
        )

        return True

    return True


# ---------------------------------------------------------
# Onboarding Workflow
# ---------------------------------------------------------

def run_onboarding(employee: Employee):
    """Run the complete simulated onboarding workflow."""

    print(
        "\n=== HeliosHR Employee Onboarding ==="
    )

    # -----------------------------------------------------
    # Step 1 - Validate Employee
    # -----------------------------------------------------

    print(
        "\n[1] Validating employee data..."
    )

    errors = validate_employee(employee)

    if errors:

        print(
            "Validation failed:"
        )

        for error in errors:
            print(f" - {error}")

        return

    print(
        "Validation successful."
    )

    # -----------------------------------------------------
    # Step 2 - Claude Creates Plan
    # -----------------------------------------------------

    print(
        "\n[2] Claude creating onboarding plan..."
    )

    plan = claude_create_onboarding_plan(
        employee
    )

    print(
        "Claude generated actions:"
    )

    for action in plan["actions"]:

        print(
            f" - {action['tool']}: "
            f"{action['reason']}"
        )

    # -----------------------------------------------------
    # Step 3 - Validate Claude Output
    # -----------------------------------------------------

    print(
        "\n[3] Validating Claude output..."
    )

    ai_errors = validate_ai_output(
        plan,
        employee,
    )

    if ai_errors:

        print(
            "AI output validation failed:"
        )

        for error in ai_errors:
            print(f" - {error}")

        return

    print(
        "AI output validation successful."
    )

    # -----------------------------------------------------
    # Step 4 - MCP Execution
    # -----------------------------------------------------

    print(
        "\n[4] MCP executing approved tools..."
    )

    mcp = MCPServer()

    results = []

    for action in plan["actions"]:

        # -------------------------------------------------
        # Human approval check
        # -------------------------------------------------

        approved = check_human_approval(
            action
        )

        if not approved:

            results.append(
                {
                    "success": False,
                    "tool": action["tool"],
                    "employee_id": employee.employee_id,
                    "error": "Human approval rejected",
                    "failure_type": "approval",
                }
            )

            continue

        # -------------------------------------------------
        # First execution attempt
        # -------------------------------------------------

        result = mcp.execute_tool(
            action["tool"],
            employee,
        )

        # -------------------------------------------------
        # Retry transient failures
        # -------------------------------------------------

        if (
            not result["success"]
            and result.get("failure_type") == "transient"
        ):

            print(
                f"[Retry] Retrying "
                f"{action['tool']}..."
            )

            result = mcp.execute_tool(
                action["tool"],
                employee,
            )

        results.append(result)

    # -----------------------------------------------------
    # Step 5 - Result Handling
    # -----------------------------------------------------

    print(
        "\n[5] Onboarding result"
    )

    failed = [
        result
        for result in results
        if not result["success"]
    ]

    if failed:

        print(
            "Onboarding completed with failures."
        )

        print(
            "Failed operations:"
        )

        for result in failed:

            print(
                f" - {result['tool']}: "
                f"{result.get('error')}"
            )

            # In production, n8n would create
            # a FreshService ticket.
            print(
                "   -> FreshService ticket "
                "would be created."
            )

    else:

        print(
            "Onboarding completed successfully."
        )

    # -----------------------------------------------------
    # Step 6 - Audit Summary
    # -----------------------------------------------------

    print(
        "\n[6] Audit summary"
    )

    print(
        f"Employee ID: {employee.employee_id}"
    )

    print(
        f"Employee Email: {employee.email}"
    )

    print(
        f"Actions executed: {len(results)}"
    )

    print(
        "Audit record would contain:"
    )

    print(
        " - Employee ID"
    )

    print(
        " - Workflow execution ID"
    )

    print(
        " - Timestamp"
    )

    print(
        " - Target system"
    )

    print(
        " - Operation"
    )

    print(
        " - Result"
    )

    print(
        " - Retry count"
    )

    print(
        " - Approval status"
    )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    employee = Employee(
        employee_id="EMP-1001",
        name="John Doe",
        email="john.doe@helioshr.com",
        department="Engineering",
        job_title="Software Engineer",
        manager="Jane Smith",
        start_date="2026-11-02",
    )

    run_onboarding(employee)