import json
from pathlib import Path

import regulations
import wiki

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"
BUNDLE = ROOT / "state-by-state-research"


class _Catalog:
    def __init__(self, entries, postal="OH", name="Ohio", citation="Ohio Rev. Code Chapter 4123.", agency="https://example.test/agency", path=None):
        self.regulations = entries
        self.postal = postal
        self.name = name
        self.primary_law = citation
        self.agency = {"resource": agency}
        self.path = path or Path("/tmp/workers-comp-mcp/states/sample.md")


def test_html_fetch_returns_the_sentence_and_a_hash():
    html = (FIXTURES / "statute.html").read_bytes()

    def fetch(url):
        assert url == "https://example.test/statute"
        return html, "text/html; charset=utf-8"

    item = _Catalog(
        [
            {
                "id": "primary-statute",
                "title": "Sample section",
                "resource": "https://example.test/statute",
                "publisher": "Example Legislature",
            }
        ]
    )
    result = regulations.regulation_response(
        item,
        fetch=fetch,
        retrieved_at="2026-10-28T15:30:00Z",
    )
    assert result["status"] == "ok"
    assert "The employer shall pay compensation." in result["text"]
    assert "This sentence must not appear." not in result["text"]
    assert result["sha256"]
    assert result["retrieved_at"] == "2026-10-28T15:30:00Z"
    assert result["resource"] == "https://example.test/statute"


def test_pdf_fetch_returns_the_text_layer():
    pdf = (FIXTURES / "statute.pdf").read_bytes()

    def fetch(url):
        return pdf, "application/pdf"

    item = _Catalog(
        [
            {
                "id": "primary-statute",
                "title": "Sample PDF",
                "resource": "https://example.test/statute.pdf",
                "publisher": "Example Legislature",
            }
        ]
    )
    result = regulations.regulation_response(item, fetch=fetch, retrieved_at="2026-10-28T15:30:00Z")
    assert result["status"] == "ok"
    assert result["content_type"] == "application/pdf"
    assert "Sample statute text." in result["text"]
    assert result["text_layer"] is True


def test_uncatalogued_state_does_not_guess_a_url():
    item = _Catalog([], postal="ZZ", name="Nowhere", citation="Sample Code section 1.", agency="https://example.test/agency")
    calls = []

    def fetch(url):
        calls.append(url)
        raise AssertionError("fetch should not run")

    result = regulations.regulation_response(item, fetch=fetch)
    assert result["status"] == "uncatalogued"
    assert result["postal"] == "ZZ"
    assert result["citation"] == "Sample Code section 1."
    assert result["agency_resource"] == "https://example.test/agency"
    assert calls == []


def test_cataloged_ohio_url_is_the_verified_section():
    item = wiki.resolve_jurisdiction("OH", BUNDLE)
    assert item.regulations[0]["resource"] == regulations.VERIFIED_REGULATIONS["OH"]["resource"]
    assert item.has_regulation_url is True


def test_coverage_labels_match_the_catalog():
    assert set(regulations.COVERAGE) == set(regulations.VERIFIED_REGULATIONS)


def test_live_fetch_failure_is_a_result():
    item = _Catalog(
        [
            {
                "id": "primary-statute",
                "title": "Sample section",
                "resource": "https://example.test/statute",
                "publisher": "Example Legislature",
                "coverage": "act",
            }
        ]
    )

    def fetch(url):
        raise TimeoutError("timed out")

    result = regulations.regulation_response(item, fetch=fetch)
    assert result["status"] == "fetch_error"
    assert result["resource"] == "https://example.test/statute"
    assert "timed out" in result["error"]
    assert "text" not in result


def test_section_argument_returns_that_passage():
    html = """
    <p>440.02 Definitions. When used in this chapter, accident means an event.</p>
    <p>440.15 Compensation for disability. The employer shall pay compensation.</p>
    <p>440.16 Compensation for death. Other text.</p>
    """.encode()

    def fetch(url):
        return html, "text/html"

    item = _Catalog(
        [
            {
                "id": "primary-statute",
                "title": "Chapter 440",
                "resource": "https://example.test/440",
                "publisher": "Example Legislature",
                "coverage": "act",
            }
        ]
    )
    result = regulations.regulation_response(item, fetch=fetch, section="440.15")
    assert result["status"] == "ok"
    assert "The employer shall pay compensation." in result["text"]
    assert "440.16" not in result["text"]
    assert result["section"] == "440.15"
    missing = regulations.regulation_response(item, fetch=fetch, section="440.99")
    assert missing["status"] == "section_not_found"
    assert "text" not in missing


def test_rules_stay_available_beside_the_act():
    item = _Catalog(
        [
            {
                "id": "primary-statute",
                "title": "The act",
                "resource": "https://example.test/act",
                "publisher": "Example Legislature",
                "coverage": "act",
            },
            {
                "id": "agency-rules",
                "title": "The rules",
                "resource": "https://example.test/rules",
                "publisher": "Example Board",
                "coverage": "rules",
            },
        ]
    )

    def fetch(url):
        body = b"<p>Act text.</p>" if url.endswith("act") else b"<p>Rules text.</p>"
        return body, "text/html"

    default = regulations.regulation_response(item, fetch=fetch)
    assert default["source_id"] == "primary-statute"
    assert "Act text." in default["text"]
    rules = regulations.regulation_response(item, source_id="agency-rules", fetch=fetch)
    assert "Rules text." in rules["text"]
    assert rules["coverage"] == "rules"


def test_every_verified_url_matches_that_states_frontmatter():
    for postal, entry in regulations.VERIFIED_REGULATIONS.items():
        item = wiki.resolve_jurisdiction(postal, BUNDLE)
        assert item.regulations[0]["resource"] == entry["resource"]
        assert item.regulations[0]["title"] == entry["title"]
        assert item.regulations[0]["publisher"] == entry["publisher"]
        assert item.regulations[0].get("text_file") == entry.get("text_file")
        assert item.regulations[0]["coverage"] == regulations.COVERAGE[postal]


def test_stored_text_is_returned_without_a_fetch(tmp_path):
    bundle = tmp_path / "bundle"
    (bundle / "states").mkdir(parents=True)
    (bundle / "statutes").mkdir()
    (bundle / "statutes" / "sample.txt").write_text(
        "The employer shall pay compensation.\n",
        encoding="utf-8",
    )
    item = _Catalog(
        [
            {
                "id": "primary-statute",
                "title": "Stored act",
                "resource": "https://example.test/act",
                "publisher": "Example Legislature",
                "text_file": "statutes/sample.txt",
                "retrieved_at": "2026-10-28T16:40:00Z",
            }
        ],
        path=bundle / "states" / "sample.md",
    )

    def fetch(url):
        raise AssertionError(url)

    result = regulations.regulation_response(item, fetch=fetch)
    assert result["status"] == "ok"
    assert result["text"].strip() == "The employer shall pay compensation."
    assert result["content_type"] == "text/plain"
    assert result["retrieved_at"] == "2026-10-28T16:40:00Z"
    assert result["resource"] == "https://example.test/act"


def test_json_statute_field_is_read_as_html():
    payload = json.dumps(
        {"Statute": "62-1-1", "Html": "<p>62-1-1. Definition of terms. Terms used in this title shall mean:</p>"}
    ).encode()
    text = regulations.document_from_response(payload, "application/json")["text"]
    assert "Definition of terms" in text
    assert "Statute" not in text
