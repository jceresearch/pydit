"""Format the package, upgrade its lockfile, and prepare the next minor release."""

from __future__ import annotations

import argparse
import re
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VERSION_PATTERN = re.compile(r"\d+\.\d+\.\d+")


def read_assignment(contents: str, name: str) -> str:
    pattern = re.compile(
        rf"(?m)^[ \t]*{re.escape(name)}[ \t]*=[ \t]*[\"']([^\"']+)[\"'][ \t]*$"
    )
    matches = list(pattern.finditer(contents))
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one {name} assignment, found {len(matches)}"
        )
    return matches[0].group(1)


def replace_assignment(contents: str, name: str, old: str, new: str) -> str:
    pattern = re.compile(
        rf"(?m)^([ \t]*{re.escape(name)}[ \t]*=[ \t]*[\"'])"
        rf"{re.escape(old)}([\"'])[ \t]*$"
    )
    updated, count = pattern.subn(
        lambda match: f"{match.group(1)}{new}{match.group(2)}", contents
    )
    if count != 1:
        raise ValueError(
            f"Expected exactly one {name} = {old!r} assignment, found {count}"
        )
    return updated


def validate_version(version: str) -> str:
    if VERSION_PATTERN.fullmatch(version) is None:
        raise ValueError(
            f"Expected version in numeric major.minor.patch format, got {version!r}"
        )
    return version


def next_patch_version(version: str) -> str:
    validate_version(version)
    major, minor, patch = version.split(".")
    return f"{major}.{minor}.{int(patch) + 1:0{len(patch)}d}"


def replace_project_version(contents: str, old: str, new: str) -> str:
    project = tomllib.loads(contents).get("project")
    if not isinstance(project, dict) or project.get("version") != old:
        raise ValueError("The [project] version changed unexpectedly")

    section = re.search(r"(?ms)^\[project\]\s*\n.*?(?=^\[|\Z)", contents)
    if section is None:
        raise ValueError("Could not find the [project] section in pyproject.toml")

    updated_section = replace_assignment(section.group(), "version", old, new)
    return contents[: section.start()] + updated_section + contents[section.end() :]


def run_ruff(*args: str) -> None:
    subprocess.run(
        ["uv", "run", "--link-mode", "copy", "--extra", "dev", "ruff", *args],
        cwd=ROOT,
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Format the package and prepare a release."
    )
    parser.add_argument(
        "--version",
        help="Set a specific release version instead of incrementing the patch version.",
    )
    args = parser.parse_args()

    pyproject_path = ROOT / "pyproject.toml"
    conf_path = ROOT / "docs/source/conf.py"
    init_path = ROOT / "pydit/__init__.py"
    changelog_path = ROOT / "CHANGELOG.md"

    pyproject = pyproject_path.read_text(encoding="utf-8")
    conf = conf_path.read_text(encoding="utf-8")
    init = init_path.read_text(encoding="utf-8")
    changelog = changelog_path.read_text(encoding="utf-8")

    current_version = tomllib.loads(pyproject)["project"]["version"]
    new_version = (
        validate_version(args.version)
        if args.version is not None
        else next_patch_version(current_version)
    )
    conf_version = read_assignment(conf, "release")
    init_version = read_assignment(init, "__version__")
    new_header = f"## V{new_version}"
    if re.search(rf"(?m)^{re.escape(new_header)}\s*$", changelog):
        raise ValueError(f"CHANGELOG.md already has a section for {new_version}")

    replace_project_version(pyproject, current_version, new_version)
    replace_assignment(conf, "release", conf_version, new_version)
    replace_assignment(init, "__version__", init_version, new_version)

    # Fix what can be fixed in the package and tests, then run the exact
    # checks the release workflow runs so CI cannot fail on them.
    run_ruff("check", "--fix", "pydit", "tests")
    run_ruff("format", "pydit", "tests")
    run_ruff("check", "./pydit")
    run_ruff("format", "--check", "./pydit")
    subprocess.run(["uv", "lock", "--upgrade"], cwd=ROOT, check=True)

    pyproject_path.write_text(
        replace_project_version(
            pyproject_path.read_text(encoding="utf-8"), current_version, new_version
        ),
        encoding="utf-8",
    )
    conf_path.write_text(
        replace_assignment(
            conf_path.read_text(encoding="utf-8"), "release", conf_version, new_version
        ),
        encoding="utf-8",
    )
    init_path.write_text(
        replace_assignment(
            init_path.read_text(encoding="utf-8"),
            "__version__",
            init_version,
            new_version,
        ),
        encoding="utf-8",
    )
    changelog_path.write_text(
        f"# Changelog\n\n{new_header}\n\n### Changes\n\n- TODO: Add release notes.\n\n"
        + changelog.removeprefix("# Changelog\n\n"),
        encoding="utf-8",
    )
    print(
        f"Prepared release {new_version}. Review and complete CHANGELOG.md before publishing."
    )


if __name__ == "__main__":
    main()
