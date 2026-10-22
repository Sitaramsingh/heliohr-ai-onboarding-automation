"""
HeliosHR - AI Powered Employee Onboarding Prototype

This prototype simulates:
Workday -> n8n -> Claude -> MCP -> Enterprise Systems
"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Employee:
    employee_id: str
    name: str
    email: str
    department: str
    job_title: str
    manager: str
    start_date: str


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
            errors.append(f"Missing required field: {field}")

    if "@" not in employee.email:
        errors.append("Invalid email address")

    return errors


def claude_create_onboarding_plan(employee: Employee) -> Dict:
    """
    Simulates Claude creating an onboarding plan.

    In the real implementation, Claude would analyze the employee
    information and approved onboarding policies.
    """

    actions = [
        {
            "tool": "create_okta_user",
            "reason": "Create enterprise identity",
        },
        {
            "tool": "create_google_workspace_user",
            "reason": "Create corporate Google account",
        },
        {
            "tool": "add_slack_user",
            "reason": "Provide Slack access",
        },
    ]

    # Example of role-based decision making.
    if employee.department.lower() == "engineering":
        actions.append(
            {
                "tool": "grant_jira_access",
                "reason": "Engineering role requires Jira access",
            }
        )

    return {
        "employee_id": employee.employee_id,
        "actions": actions,
        "requires_human_approval": False,
    }


class MCPServer:
    """Simulated MCP server exposing controlled enterprise tools."""

    ALLOWED_TOOLS = {
        "create_okta_user",
        "create_google_workspace_user",
        "add_slack_user",
        "grant_jira_access",
        "create_freshservice_ticket",
    }

    def execute_tool(self, tool_name: str, employee: Employee) -> Dict:
        """Validate and execute an approved MCP tool."""

        if tool_name not in self.ALLOWED_TOOLS:
            return {
                "success": False,
                "tool": tool_name,
                "error": "Tool is not allowed",
            }

        print(f"[MCP] Executing: {tool_name} for {employee.email}")

        return {
            "success": True,
            "tool": tool_name,
            "employee_id": employee.employee_id,
        }


def run_onboarding(employee: Employee):
    """Run the complete simulated onboarding workflow."""

    print("\n=== HeliosHR Employee Onboarding ===")

    # Step 1: Validate employee data
    print("\n[1] Validating employee data...")

    errors = validate_employee(employee)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f" - {error}")
        return

    print("Validation successful.")

    # Step 2: Claude creates onboarding plan
    print("\n[2] Claude creating onboarding plan...")

    plan = claude_create_onboarding_plan(employee)

    print("Claude generated actions:")

    for action in plan["actions"]:
        print(f" - {action['tool']}: {action['reason']}")

    # Step 3: MCP executes approved tools
    print("\n[3] MCP executing approved tools...")

    mcp = MCPServer()

    results = []

    for action in plan["actions"]:
        result = mcp.execute_tool(
            action["tool"],
            employee,
        )

        results.append(result)

    # Step 4: Final result
    print("\n[4] Onboarding result")

    failed = [result for result in results if not result["success"]]

    if failed:
        print("Onboarding completed with failures.")
        print("Failed operations:")
        for result in failed:
            print(f" - {result['tool']}")
    else:
        print("Onboarding completed successfully.")


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