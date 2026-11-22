from pathlib import Path
import multiprocessing as mp

from git import Optional

from argonaut.config.config import (
    PROJECT_JSON_PATH,
    PROJECT_TRACKER_JSON_PATH,
    PROJECT_TRACKER_REPO_NAME,
    PROJECT_TRACKER_REPO_OWNER,
)
from argonaut.document_types.supported_document_types import (
    get_document_type_from_abbreviation,
)
from argonaut.gui.dialog import get_folder_input, show_error, show_info, show_warning
from argonaut.misc.git import (
    get_git_info,
    get_repo_owner_name_from_url,
    git_clone,
    git_pull,
)
from argonaut.tracker.document_tracker import DocumentTracker
from argonaut.tracker.project_tracker import ProjectTracker


def update_project(
    project_path: Path,
    project_repo_owner: Optional[str] = None,
    project_repo_name: Optional[str] = None,
) -> list[str]:
    """
    Updates a folder that is the top level checkout of a project.
    If owner and name are specified, it will check the git info of the folder matches
    Otherwise, it will take owner and name from the git information in the checkout
    """
    git_info = get_git_info(project_path)
    if (
        project_repo_owner is not None
        and project_repo_owner.lower() != git_info.repo_owner.lower()
    ):
        show_error(
            f"Upstream repo owner ({git_info.repo_owner}) does not match expected owner ({project_repo_owner})",
            "Repo owner mismatch",
        )

    if (
        project_repo_name is not None
        and project_repo_name.lower() != git_info.repo_name.lower()
    ):
        show_error(
            f"Upstream repo name ({git_info.repo_name}) does not match expected name ({project_repo_name})",
            "Repo name mismatch",
        )

    if git_info.local_ahead_commit_count > 0:
        show_warning(
            "Local repo is ahead of upstream. Please commit changes before updating",
            "Local repo ahead of upstream",
        )

    # @TODO decide if we care about uncommitted changes. For now, attempt pull and see if it fails
    # Will need some thought as checkouts of other projects will be uncommitted changes

    if git_pull(project_path) is False:
        return [f"{project_repo_owner}/{project_repo_name}"]

    docs_with_issues: list[str] = []

    with DocumentTracker(
        git_info.repo_owner, git_info.repo_name, PROJECT_JSON_PATH
    ) as doc_tracker:
        for doc_type, docs in doc_tracker.project_json["documents"].items():
            if get_document_type_from_abbreviation(doc_type).separate_repo is False:
                # Document is within top level repo
                continue

            # Document is in separate repo
            for doc_number, doc_info in docs.items():
                doc_name = doc_info["name"]
                doc_repo_owner, doc_repo_name = get_repo_owner_name_from_url(
                    doc_info["url"]
                )
                doc_path = (
                    project_path / f"{doc_number}_{doc_name.title().replace(' ', '')}"
                )
                if (
                    update_document_in_separate_repo(
                        doc_path, doc_repo_owner, doc_repo_name
                    )
                    is False
                ):
                    docs_with_issues.append(f"{doc_repo_owner}/{doc_repo_name}")
    return docs_with_issues


def update_document_in_separate_repo(
    document_local_path: Path, repo_owner: str, repo_name: str, show_error: bool = True
) -> bool:
    """
    Returns true if updated successfully (including if nothing to update)
    """
    if document_local_path.exists():
        # Repo exists so just pull
        return git_pull(document_local_path, show_error)
    else:
        return git_clone(
            repo_owner, repo_name, document_local_path, show_error_window=show_error
        )


def update_project_multithreaded(
    output_queue: mp.Queue, root_path: Path, project_number: str, project_info: dict
):
    project_name = project_info["name"]
    project_repo_owner, project_repo_name = get_repo_owner_name_from_url(
        project_info["url"]
    )
    project_path = (
        root_path / f"{project_number}_{project_name.title().replace(' ', '')}"
    )

    if not project_path.exists():
        git_clone(
            project_repo_owner,
            project_repo_name,
            project_path,
        )
    output_queue.put(
        update_project(project_path, project_repo_owner, project_repo_name)
    )


def update_all_projects():
    with ProjectTracker(
        PROJECT_TRACKER_REPO_OWNER,
        PROJECT_TRACKER_REPO_NAME,
        PROJECT_TRACKER_JSON_PATH,
    ) as tracker:
        root_path = get_folder_input(
            "Please select folder where projects will be checked out to"
        )
        queue = mp.Queue()
        processes = [
            mp.Process(
                target=update_project_multithreaded,
                args=(queue, root_path, project_number, project_info),
            )
            for project_number, project_info in tracker.project_json.items()
        ]

        for process in processes:
            process.start()

        for process in processes:
            process.join()

        all_docs_with_issues: list[str] = []

        for _ in processes:
            all_docs_with_issues.extend(queue.get())

        if all_docs_with_issues != []:
            show_warning(
                "Issues found with updating:" + "\n\t".join(all_docs_with_issues),
                "Issues updating documents",
            )
        else:
            show_info("Done", "Done")
