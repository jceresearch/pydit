"""Format the package, upgrade its lockfile, and prepare the next minor release."""

from __future__ import annotations

import re
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent


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


def next_minor_version(version: str) -> str:
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version)
    if match is None:
        raise ValueError(
            f"Expected a numeric major.minor.patch version, got {version!r}"
        )

    major, minor, patch = match.groups()
    return f"{major}.{int(minor) + 1}.{0:0{len(patch)}d}"


def replace_project_version(contents: str, old: str, new: str) -> str:
    project = tomllib.loads(contents).get("project")
    if not isinstance(project, dict) or project.get("version") != old:
        raise ValueError("The [project] version changed unexpectedly")

    section = re.search(r"(?ms)^\[project\]\s*\n.*?(?=^\[|\Z)", contents)
    if section is None:
        raise ValueError("Could not find the [project] section in pyproject.toml")

    updated_section = replace_assignment(section.group(), "version", old, new)
    return contents[: section.start()] + updated_section + contents[section.end() :]


def main() -> None:
    pyproject_path = ROOT / "pyproject.toml"
    conf_path = ROOT / "docs/source/conf.py"
    init_path = ROOT / "pydit/__init__.py"
    changelog_path = ROOT / "CHANGELOG.md"

    pyproject = pyproject_path.read_text(encoding="utf-8")
    conf = conf_path.read_text(encoding="utf-8")
    init = init_path.read_text(encoding="utf-8")
    changelog = changelog_path.read_text(encoding="utf-8")

    current_version = tomllib.loads(pyproject)["project"]["version"]
    new_version = next_minor_version(current_version)
    conf_version = read_assignment(conf, "release")
    init_version = read_assignment(init, "__version__")
    new_header = f"## V{new_version}"
    if re.search(rf"(?m)^{re.escape(new_header)}\s*$", changelog):
        raise ValueError(f"CHANGELOG.md already has a section for {new_version}")

    replace_project_version(pyproject, current_version, new_version)
    replace_assignment(conf, "release", conf_version, new_version)
    replace_assignment(init, "__version__", init_version, new_version)

    subprocess.run(
        ["uv", "run", "--extra", "dev", "ruff", "format", "pydit", "tests"],
        cwd=ROOT,
        check=True,
    )
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
