#!/usr/bin/env python3

import os
import subprocess
import sys
import tempfile


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

START = "e21f685"
END = "9889fd2"

EDITOR = "nvim"


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def git(*args):
    return subprocess.check_output(
        ["git", *args],
        text=True,
    ).strip()


def get_commits():
    """
    Return all commits from START to END in chronological order.
    """
    output = git(
        "rev-list",
        "--reverse",
        f"{START}^..{END}",
    )

    return output.splitlines()


def get_commit_info(commit):
    """
    Get all information required to recreate the commit while
    preserving its identity and timestamps.
    """

    fmt = (
        "%an%n"
        "%ae%n"
        "%aI%n"
        "%cn%n"
        "%ce%n"
        "%cI%n"
        "%B"
    )

    output = git(
        "show",
        "-s",
        f"--format={fmt}",
        commit,
    )

    lines = output.splitlines()

    author_name = lines[0]
    author_email = lines[1]
    author_date = lines[2]

    committer_name = lines[3]
    committer_email = lines[4]
    committer_date = lines[5]

    message = "\n".join(lines[6:]).rstrip()

    return {
        "author_name": author_name,
        "author_email": author_email,
        "author_date": author_date,
        "committer_name": committer_name,
        "committer_email": committer_email,
        "committer_date": committer_date,
        "message": message,
    }


# ---------------------------------------------------------------------------
# Neovim commit message editor
# ---------------------------------------------------------------------------

def edit_message(initial_message, commit_number, total_commits):
    """
    Open Neovim with the current commit message.

    The user can edit both:
      - commit subject
      - commit body / description
    """

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".commitmsg",
        delete=False,
        encoding="utf-8",
    ) as file:

        file.write(initial_message)
        file.write("\n")

        message_file = file.name

    print()
    print("=" * 80)
    print(f"Commit {commit_number}/{total_commits}")
    print("=" * 80)
    print()
    print("Opening Neovim...")
    print("Edit the commit subject and description.")
    print("Save and exit with :wq")
    print()

    try:
        subprocess.run(
            [EDITOR, message_file],
            check=True,
        )

        with open(
            message_file,
            "r",
            encoding="utf-8",
        ) as file:
            message = file.read().strip()

    finally:
        try:
            os.unlink(message_file)
        except FileNotFoundError:
            pass

    if not message:
        print()
        print("ERROR: Commit message cannot be empty.")
        print("Rewrite stopped.")
        sys.exit(1)

    return message


# ---------------------------------------------------------------------------
# Commit creation
# ---------------------------------------------------------------------------

def create_commit(
    parent,
    tree,
    info,
    message,
):
    """
    Recreate a commit using the original author and committer
    information and the original timestamps.
    """

    env = os.environ.copy()

    # Preserve author information.
    env["GIT_AUTHOR_NAME"] = info["author_name"]
    env["GIT_AUTHOR_EMAIL"] = info["author_email"]
    env["GIT_AUTHOR_DATE"] = info["author_date"]

    # Preserve committer information.
    env["GIT_COMMITTER_NAME"] = info["committer_name"]
    env["GIT_COMMITTER_EMAIL"] = info["committer_email"]
    env["GIT_COMMITTER_DATE"] = info["committer_date"]

    args = [
        "commit-tree",
        tree,
    ]

    if parent:
        args.extend([
            "-p",
            parent,
        ])

    result = subprocess.run(
        ["git", *args],
        input=message + "\n",
        text=True,
        capture_output=True,
        env=env,
        check=True,
    )

    return result.stdout.strip()


# ---------------------------------------------------------------------------
# Main rewrite process
# ---------------------------------------------------------------------------

def main():

    # Make sure we are inside a Git repository.
    try:
        git("rev-parse", "--show-toplevel")
    except subprocess.CalledProcessError:
        print("ERROR: This is not a Git repository.")
        sys.exit(1)

    commits = get_commits()

    if not commits:
        print("ERROR: No commits found.")
        sys.exit(1)

    print()
    print("=" * 80)
    print("Git Commit Message Rewrite")
    print("=" * 80)
    print()
    print(f"Start commit : {START}")
    print(f"End commit   : {END}")
    print(f"Total commits: {len(commits)}")
    print()
    print("Original AuthorDate and CommitterDate will be preserved.")
    print("Commit contents will not be changed.")
    print()
    print("=" * 80)
    print()

    parent = None

    for index, old_commit in enumerate(commits, start=1):

        info = get_commit_info(old_commit)

        print()
        print("=" * 80)
        print(f"Commit {index}/{len(commits)}")
        print("=" * 80)
        print()
        print(f"Old commit:")
        print(old_commit)
        print()
        print(f"Author date:")
        print(info["author_date"])
        print()
        print(f"Committer date:")
        print(info["committer_date"])
        print()
        print("Current commit message:")
        print("-" * 80)
        print(info["message"])
        print("-" * 80)

        # Open Neovim for editing.
        new_message = edit_message(
            info["message"],
            index,
            len(commits),
        )

        # Get the exact tree from the original commit.
        tree = git(
            "rev-parse",
            f"{old_commit}^{{tree}}",
        )

        # Recreate the commit.
        new_commit = create_commit(
            parent=parent,
            tree=tree,
            info=info,
            message=new_message,
        )

        print()
        print(f"Original commit: {old_commit}")
        print(f"New commit:      {new_commit}")
        print()

        parent = new_commit

    # -----------------------------------------------------------------------
    # Finished
    # -----------------------------------------------------------------------

    print()
    print("=" * 80)
    print("REWRITE COMPLETED")
    print("=" * 80)
    print()
    print(f"New HEAD: {parent}")
    print()
    print("IMPORTANT:")
    print()
    print("Your current branch has NOT been moved yet.")
    print()
    print("Verify the new history first.")
    print()
    print("After verification, move the branch with:")
    print()
    print(f"    git reset --hard {parent}")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
