"""Load jurisdiction concepts from the OKF research bundle."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

BUNDLE_DIR = Path(
    os.environ.get(
        "WORKERS_COMP_WIKI",
        Path(__file__).resolve().parent / "state-by-state-research",
    )
)

_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
_PRIMARY_LAW = re.compile(r"^# Primary law\n+(.*?)(?=^# |\Z)", re.M | re.S)


@dataclass(frozen=True)
class Jurisdiction:
    slug: str
    path: Path
    frontmatter: dict
    body: str
    reimbursement: dict

    @property
    def postal(self) -> str:
        return self.reimbursement["jurisdiction"]["postal"]

    @property
    def name(self) -> str:
        return self.reimbursement["jurisdiction"]["name"]

    @property
    def primary_law(self) -> str:
        match = _PRIMARY_LAW.search(self.body)
        if not match:
            return ""
        return " ".join(match.group(1).split())

    @property
    def agency(self) -> dict:
        for source in self.frontmatter.get("sources") or []:
            if source.get("id") == "agency":
                return {"title": source.get("title"), "resource": source.get("resource")}
        return {"title": None, "resource": self.frontmatter.get("resource")}

    @property
    def regulations(self) -> list[dict]:
        raw = self.frontmatter.get("regulations") or []
        return list(raw)

    @property
    def has_regulation_url(self) -> bool:
        return any(entry.get("resource") for entry in self.regulations)

    @property
    def has_fee_schedule(self) -> bool:
        return self.reimbursement.get("medical_fee_schedule") is not None


def bundle_dir() -> Path:
    return BUNDLE_DIR


def reimbursement_path(slug: str, root: Path | None = None) -> Path:
    return (root or bundle_dir()) / "reimbursement" / f"{slug}.json"


def load_reimbursement(slug: str, root: Path | None = None) -> dict:
    path = reimbursement_path(slug, root)
    if not path.is_file():
        raise ValueError(f"{path} is missing")
    return json.loads(path.read_text(encoding="utf-8"))


def load_jurisdiction(path: Path, root: Path | None = None) -> Jurisdiction:
    text = path.read_text(encoding="utf-8")
    match = _FRONTMATTER.search(text)
    if not match:
        raise ValueError(f"{path} is missing YAML frontmatter")
    frontmatter = yaml.safe_load(match.group(1)) or {}
    body = text[match.end() :]
    bundle = root or path.parent.parent
    reimbursement = load_reimbursement(path.stem, bundle)
    return Jurisdiction(
        slug=path.stem,
        path=path,
        frontmatter=frontmatter,
        body=body,
        reimbursement=reimbursement,
    )


def load_jurisdictions(root: Path | None = None) -> list[Jurisdiction]:
    states = (root or bundle_dir()) / "states"
    found = [
        load_jurisdiction(path)
        for path in sorted(states.glob("*.md"))
        if path.name != "index.md"
    ]
    return sorted(found, key=lambda item: item.name)


def _fold(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def resolve_jurisdiction(query: str, root: Path | None = None) -> Jurisdiction:
    needle = _fold(query)
    if needle in {"dc", "districtofcolumbia"}:
        needle = "districtofcolumbia"
    matches = []
    for item in load_jurisdictions(root):
        keys = {_fold(item.postal), _fold(item.name), _fold(item.slug)}
        if needle in keys:
            matches.append(item)
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise ValueError(f"No jurisdiction named {query!r}.")
    names = ", ".join(item.postal for item in matches)
    raise ValueError(f"{query!r} matches more than one jurisdiction: {names}.")


def write_reimbursement(path: Path, reimbursement: dict) -> None:
    """Write the reimbursement object for a jurisdiction markdown path."""
    bundle = path.parent.parent
    dest = reimbursement_path(path.stem, bundle)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        json.dumps(reimbursement, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def append_source(path: Path, source: dict) -> None:
    text = path.read_text(encoding="utf-8")
    match = _FRONTMATTER.search(text)
    if not match:
        raise ValueError(f"{path} is missing YAML frontmatter")
    frontmatter = yaml.safe_load(match.group(1)) or {}
    sources = list(frontmatter.get("sources") or [])
    if any(item.get("id") == source["id"] for item in sources):
        return
    block = (
        f"  - id: {source['id']}\n"
        f"    resource: {_quote(source['resource'])}\n"
        f"    title: {_quote(source['title'])}\n"
        f"    author: {source['author']}\n"
    )
    fm = match.group(1)
    if not fm.endswith("\n"):
        fm += "\n"
    # The sources list is the last frontmatter key. New list items must
    # stay attached to it, ahead of any later key such as regulations.
    regulations = ""
    marker = "\nregulations:"
    if marker in fm:
        fm, regulations = fm.split(marker, 1)
        regulations = marker + regulations
    if not fm.endswith("\n"):
        fm += "\n"
    new_fm = fm + block + regulations.lstrip("\n")
    if regulations and not new_fm.endswith("\n"):
        new_fm += "\n"
    path.write_text("---\n" + new_fm + "---\n" + text[match.end() :], encoding="utf-8")


def _regulation_lines(entries: list[dict]) -> str:
    lines = ["regulations:"]
    for entry in entries:
        lines.append(f"  - id: {entry['id']}")
        lines.append(f"    title: {_quote(entry['title'])}")
        lines.append(f"    resource: {_quote(entry['resource'])}")
        lines.append(f"    publisher: {_quote(entry['publisher'])}")
        for key in ("coverage", "text_file", "retrieved_at"):
            if entry.get(key):
                lines.append(f"    {key}: {_quote(entry[key])}")
    return "\n".join(lines) + "\n"


def set_regulations(path: Path, entries: list[dict]) -> None:
    text = path.read_text(encoding="utf-8")
    match = _FRONTMATTER.search(text)
    if not match:
        raise ValueError(f"{path} is missing YAML frontmatter")
    frontmatter = yaml.safe_load(match.group(1)) or {}
    if frontmatter.get("regulations"):
        return
    fm = match.group(1)
    if not fm.endswith("\n"):
        fm += "\n"
    path.write_text("---\n" + fm + _regulation_lines(entries) + "---\n" + text[match.end() :], encoding="utf-8")


def replace_regulations(path: Path, entries: list[dict]) -> None:
    text = path.read_text(encoding="utf-8")
    match = _FRONTMATTER.search(text)
    if not match:
        raise ValueError(f"{path} is missing YAML frontmatter")
    fm = match.group(1)
    if "\nregulations:" in fm:
        fm = fm.split("\nregulations:", 1)[0]
    if not fm.endswith("\n"):
        fm += "\n"
    path.write_text("---\n" + fm + _regulation_lines(entries) + "---\n" + text[match.end() :], encoding="utf-8")
