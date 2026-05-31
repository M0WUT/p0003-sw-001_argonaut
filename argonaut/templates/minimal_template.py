# Standard imports

from pathlib import Path

# Third party imports

# Local imports
from argonaut.misc.git import generate_github_repo_url
from argonaut.config.document_type import DocumentType


def init_minimal_folder(
    local_path: Path,
    repo_owner: str,
    repo_name: str,
    document_type: DocumentType,
    document_reference: str,
    document_name: str,
    document_description: str,
) -> dict[str, str]:

    # SW folders are separate repos but with no template
    # provided

    # Add README
    readme_path = local_path / "README.md"
    with open(readme_path, "w+") as readme_file:
        readme_file.write(f"# {document_reference} - {document_name}\n")
        readme_file.write(f"{document_description}\n")

    return {
        "name": document_name,
        "description": document_description,
        "url": generate_github_repo_url(repo_owner, repo_name),
    }
