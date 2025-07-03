"""
https://www.perplexity.ai/search/write-a-python-script-that-acc-.STJrVWKSNCylY_UYixbYQ

for each principal (email), lists all the roles assigned to them in the given Google Cloud project.

How it works:

It fetches the IAM policy using gcloud.

It builds a mapping from each principal to a set of roles.

It prints each principal and the roles they have.
"""



import subprocess
import json
import sys
from collections import defaultdict

def get_iam_principals_and_roles(project_id):
    # Fetch the IAM policy for the project as JSON
    try:
        result = subprocess.run(
            [
                "gcloud", "projects", "get-iam-policy", project_id,
                "--format=json"
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error fetching IAM policy: {e.stderr}", file=sys.stderr)
        sys.exit(1)

    policy = json.loads(result.stdout)
    # Map from principal (email) to set of roles
    principal_roles = defaultdict(set)

    for binding in policy.get("bindings", []):
        role = binding.get("role")
        for member in binding.get("members", []):
            # Extract email/identifier after the colon
            if ":" in member:
                principal = member.split(":", 1)[1]
            else:
                principal = member
            principal_roles[principal].add(role)

    return principal_roles

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python list_gcp_project_principals_and_roles.py <PROJECT_ID>")
        sys.exit(1)
    project_id = sys.argv[1]
    principal_roles = get_iam_principals_and_roles(project_id)
    for principal in sorted(principal_roles):
        roles = sorted(principal_roles[principal])
        print(f"{principal}:")
        for role in roles:
            print(f"  - {role}")

