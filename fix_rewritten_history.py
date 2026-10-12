import os
import subprocess
import sys

CURRENT_HEAD = "1e53a0e814ebbfe14f40f737fb09e164b7b0c6f8"
ORIGINAL_PARENT = "781b5900205cfd7fff9aa3a03ee85b76ad535107"


def git(*args, env=None):
    result = subprocess.run(
        ["git", *args],
        text=True,
        capture_output=True,
        env=env,
    )

    if result.returncode != 0:
        print(result.stderr)
        sys.exit(1)

    return result.stdout.rstrip("\n")


def get_commits():
    output = git(
        "rev-list",
        "--reverse",
        CURRENT_HEAD,
    )
    return output.splitlines()


def get_commit_info(commit):
    return {
        "tree": git("rev-parse", f"{commit}^{{tree}}"),
        "author_name": git("show", "-s", "--format=%an", commit),
        "author_email": git("show", "-s", "--format=%ae", commit),
        "author_date": git("show", "-s", "--format=%aI", commit),
        "committer_name": git("show", "-s", "--format=%cn", commit),
        "committer_email": git("show", "-s", "--format=%ce", commit),
        "committer_date": git("show", "-s", "--format=%cI", commit),
        "message": git("show", "-s", "--format=%B", commit),
    }


def create_commit(info, parent):
    env = os.environ.copy()

    env["GIT_AUTHOR_NAME"] = info["author_name"]
    env["GIT_AUTHOR_EMAIL"] = info["author_email"]
    env["GIT_AUTHOR_DATE"] = info["author_date"]

    env["GIT_COMMITTER_NAME"] = info["committer_name"]
    env["GIT_COMMITTER_EMAIL"] = info["committer_email"]
    env["GIT_COMMITTER_DATE"] = info["committer_date"]

    args = [
        "commit-tree",
        info["tree"],
    ]

    if parent:
        args += ["-p", parent]

    result = subprocess.run(
        ["git", *args],
        input=info["message"],
        text=True,
        capture_output=True,
        env=env,
    )

    if result.returncode != 0:
        print(result.stderr)
        sys.exit(1)

    return result.stdout.strip()


commits = get_commits()

print(f"Found {len(commits)} rewritten commits.")
print()
print(f"Original parent: {ORIGINAL_PARENT}")
print()

parent = ORIGINAL_PARENT

new_commits = []

for index, old_commit in enumerate(commits, start=1):
    info = get_commit_info(old_commit)

    new_commit = create_commit(
        info,
        parent,
    )

    new_commits.append(new_commit)

    print(f"Commit {index}/{len(commits)}")
    print(f"Old: {old_commit}")
    print(f"New: {new_commit}")
    print(f"Message: {info['message'].splitlines()[0]}")
    print()

    parent = new_commit


new_head = new_commits[-1]

print("=" * 80)
print("CORRECTED REWRITE COMPLETED")
print("=" * 80)
print()
print(f"New HEAD: {new_head}")
print()
print("The current branch has NOT been moved.")
print()
print("Verify the history first.")
print()
print(f"After verification:")
print(f"git reset --hard {new_head}")
