import os
import subprocess


class GitTools:
    @staticmethod
    def init_repo(repo_path: str) -> str:
        if not os.path.exists(repo_path):
            os.makedirs(repo_path)

        if os.path.isdir(os.path.join(repo_path, ".git")):
            return f"repo exists at {os.path.abspath(repo_path)}"

        output = subprocess.getoutput(f"git init", cwd=repo_path)

        if "empty git" not in output.lower():
            return f"failed to init repo: {output}"

    @staticmethod
    def config_user(repo_path: str, name: str, email: str) -> str:
        subprocess.getoutput(f"git config --global user.name '{name}'", cwd=repo_path)
        subprocess.getoutput(f"git config --global user.email '{email}'", cwd=repo_path)

        name_configured = subprocess.getoutput(
            "git config --global user.name", cwd=repo_path
        ).strip()
        email_configured = subprocess.getoutput(
            "git config --global user.email", cwd=repo_path
        ).strip()

        if name_configured == name and email_configured == email:
            return f"git user configured: {name} <{email}>"
        return (
            f"user configuration failed. Set to {name_configured} <{email_configured}>"
        )

    @staticmethod
    def git_status(repo_path: str) -> str:
        output = subprocess.getoutput("git status --porcelain", cwd=repo_path).strip()

        if not output:
            return "Nothing to commit."

        summary = []
        for line in output.split("\n"):
            if not line:
                continue

            status_xy = line[:2]
            filepath = line[3:].strip()

            if status_xy == "??":
                summary.append(f"untracked: {filepath}")
            elif status_xy == " M":
                summary.append(f"modified (unstaged): {filepath}")
            elif status_xy == "M ":
                summary.append(f"modified (staged): {filepath}")
            elif status_xy == "MM":
                summary.append(f"modified (staged and unstaged): {filepath}")
            elif status_xy.startswith("A"):
                summary.append(f"added (staged): {filepath}")
            elif status_xy.startswith("D"):
                summary.append(f"deleted (staged): {filepath}")
            elif (
                status_xy.startswith("U")
                or status_xy.endswith("U")
                or status_xy == "AA"
                or status_xy == "DD"
            ):
                summary.append(f"unmerged/conflict: {filepath}")
            else:
                summary.append(f"other status ({status_xy}): {filepath}")

        return "\n".join(summary)

    @staticmethod
    def git_add_all(repo_path: str) -> str:

        output = subprocess.getoutput("git add .", cwd=repo_path).strip()

        if output and "fatal" in output.lower():
            return f"error during add: {output}"

        return "changes successfully staged."

    @staticmethod
    def git_commit(repo_path: str, message: str) -> str:

        diff_output = subprocess.getoutput("git diff --cached", cwd=repo_path).strip()
        if not diff_output:
            return "no changes are staged to commit"

        output = subprocess.getoutput(f'git commit -m "{message}"', cwd=repo_path)

        if "fatal" in output.lower() or "error" in output.lower():
            return f"error: {output}"

        commit_hash = output.split("\n")[0].split()[-1] if "commit" in output else "N/A"
        return f"commit hash: {commit_hash}"

    @staticmethod
    def git_diff(repo_path: str) -> str:

        diff_output = subprocess.getoutput("git diff", cwd=repo_path).strip()
        if not diff_output:
            return "no unstaged changes found."

        if len(diff_output) > 2000:
            return (
                "unstaged changes\n"
                + diff_output[:1900]
                + "\n... [Remaining diff truncated]"
            )

        return "unstaged changes:\n" + diff_output

    @staticmethod
    def git_stash(repo_path: str, message: str = "") -> str:

        stash_cmd = "git stash push"
        if message:
            stash_cmd += f' -m "{message}"'

        output = subprocess.getoutput(stash_cmd, cwd=repo_path).strip()

        if "no" in output.lower():
            return "no local changes found to stash"

        if "fatal" in output.lower():
            return f"error: {output}"

        list_output = subprocess.getoutput(
            "git stash list --max-count=1", cwd=repo_path
        ).strip()

        if list_output:
            latest_stash = list_output.split(":")[0]
            return f"changes successfully stashed ({latest_stash})"

        return "changes successfully stashed"
