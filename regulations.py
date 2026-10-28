"""Fetch one cataloged official regulation document."""

from __future__ import annotations

import hashlib
import json
import re
import ssl
from datetime import datetime, timezone
from html.parser import HTMLParser
from io import BytesIO
from urllib.request import Request, urlopen

import certifi
from pypdf import PdfReader

# Pages fetched on 2026-10-28 that contain the statute text in the response body.
VERIFIED_REGULATIONS = {
    "AK": {
        "id": "primary-statute",
        "title": "Alaska Statutes title 23",
        "resource": "https://www.akleg.gov/statutesPDF/Title-23.pdf",
        "publisher": "Alaska Legislature",
    },
    "AZ": {
        "id": "primary-statute",
        "title": "Arizona Revised Statutes section 23-901",
        "resource": "https://www.azleg.gov/ars/23/00901.htm",
        "publisher": "Arizona State Legislature",
    },
    "DC": {
        "id": "primary-statute",
        "title": "D.C. Code title 32, chapter 15",
        "resource": "https://code.dccouncil.gov/us/dc/council/code/titles/32/chapters/15/index.full.html",
        "publisher": "Council of the District of Columbia",
    },
    "DE": {
        "id": "primary-statute",
        "title": "Delaware Code title 19",
        "resource": "https://delcode.delaware.gov/title19/Title19.pdf",
        "publisher": "Delaware General Assembly",
    },
    "IA": {
        "id": "primary-statute",
        "title": "Iowa Code chapter 85",
        "resource": "https://www.legis.iowa.gov/docs/code/85.pdf",
        "publisher": "Iowa Legislative Services Agency",
    },
    "ID": {
        "id": "primary-statute",
        "title": "Idaho Code title 72, chapter 1",
        "resource": "https://legislature.idaho.gov/wp-content/uploads/statutesrules/idstat/Title72/T72CH1.pdf",
        "publisher": "Idaho Legislature",
    },
    "KS": {
        "id": "primary-statute",
        "title": "Kansas Statutes section 44-501",
        "resource": "https://www.ksrevisor.org/statutes/chapters/ch44/044_005_0001.html",
        "publisher": "Kansas Revisor of Statutes",
    },
    "KY": {
        "id": "primary-statute",
        "title": "Kentucky Revised Statutes section 342.0011",
        "resource": "https://apps.legislature.ky.gov/law/statutes/statute.aspx?id=56771",
        "publisher": "Kentucky Legislative Research Commission",
    },
    "LA": {
        "id": "primary-statute",
        "title": "Louisiana Revised Statutes section 23:1021",
        "resource": "https://www.legis.la.gov/legis/Law.aspx?d=83328",
        "publisher": "Louisiana State Legislature",
    },
    "MA": {
        "id": "primary-statute",
        "title": "Massachusetts General Laws chapter 152, section 1",
        "resource": "https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXXI/Chapter152/section1",
        "publisher": "Massachusetts General Court",
    },
    "MD": {
        "id": "primary-statute",
        "title": "Maryland Code, Labor and Employment article",
        "resource": "https://mgaleg.maryland.gov/2026RS/Statute_Web/GLE/GLE.pdf",
        "publisher": "Maryland General Assembly",
    },
    "ME": {
        "id": "primary-statute",
        "title": "Maine Revised Statutes title 39-A",
        "resource": "https://legislature.maine.gov/statutes/39-A/title39-A.pdf",
        "publisher": "Maine Legislature",
    },
    "MI": {
        "id": "primary-statute",
        "title": "Michigan Compiled Laws Act 317 of 1969",
        "resource": "https://www.legislature.mi.gov/documents/mcl/pdf/mcl-Act-317-of-1969.pdf",
        "publisher": "Michigan Legislature",
    },
    "MO": {
        "id": "primary-statute",
        "title": "Missouri Revised Statutes section 287.020",
        "resource": "https://revisor.mo.gov/main/OneSection.aspx?section=287.020",
        "publisher": "Missouri Revisor of Statutes",
    },
    "MN": {
        "id": "primary-statute",
        "title": "Minnesota Statutes chapter 176",
        "resource": "https://www.revisor.mn.gov/statutes/cite/176/pdf",
        "publisher": "Office of the Revisor of Statutes",
    },
    "NC": {
        "id": "primary-statute",
        "title": "North Carolina General Statutes chapter 97",
        "resource": "https://www.ncleg.gov/EnactedLegislation/Statutes/HTML/ByChapter/Chapter_97.html",
        "publisher": "North Carolina General Assembly",
    },
    "ND": {
        "id": "primary-statute",
        "title": "North Dakota Century Code chapter 65-01",
        "resource": "https://ndlegis.gov/cencode/t65c01.pdf",
        "publisher": "North Dakota Legislative Council",
    },
    "NE": {
        "id": "primary-statute",
        "title": "Nebraska Revised Statutes section 48-101",
        "resource": "https://nebraskalegislature.gov/laws/statutes.php?statute=48-101",
        "publisher": "Nebraska Legislature",
    },
    "NH": {
        "id": "primary-statute",
        "title": "New Hampshire Revised Statutes Annotated chapter 281-A",
        "resource": "http://www.gencourt.state.nh.us/rsa/html/xxiii/281-a/281-a-mrg.htm",
        "publisher": "New Hampshire General Court",
    },
    "NV": {
        "id": "primary-statute",
        "title": "Nevada Revised Statutes chapter 616A",
        "resource": "https://www.leg.state.nv.us/nrs/NRS-616A.html",
        "publisher": "Nevada Legislature",
    },
    "OH": {
        "id": "primary-statute",
        "title": "Ohio Revised Code chapter 4123",
        "resource": "https://codes.ohio.gov/ohio-revised-code/chapter-4123",
        "publisher": "Ohio Legislative Service Commission",
    },
    "OK": {
        "id": "primary-statute",
        "title": "Oklahoma Statutes title 85A",
        "resource": "https://oksenate.gov/sites/default/files/2022-05/os85A.pdf",
        "publisher": "Oklahoma State Senate",
    },
    "OR": {
        "id": "primary-statute",
        "title": "Oregon Revised Statutes chapter 656",
        "resource": "https://www.oregonlegislature.gov/bills_laws/ors/ors656.html",
        "publisher": "Oregon State Legislature",
    },
    "PA": {
        "id": "primary-statute",
        "title": "Pennsylvania Workers' Compensation Act",
        "resource": "https://www.legis.state.pa.us/WU01/LI/LI/US/HTM/1915/0/0338..HTM",
        "publisher": "Pennsylvania General Assembly",
    },
    "RI": {
        "id": "primary-statute",
        "title": "Rhode Island General Laws section 28-33-1",
        "resource": "http://webserver.rilegislature.gov/Statutes/TITLE28/28-33/28-33-1.HTM",
        "publisher": "Rhode Island General Assembly",
    },
    "SC": {
        "id": "primary-statute",
        "title": "South Carolina Code title 42, chapter 1",
        "resource": "https://www.scstatehouse.gov/code/t42c001.php",
        "publisher": "South Carolina Legislature",
    },
    "UT": {
        "id": "primary-statute",
        "title": "Utah Code title 34A, chapter 2",
        "resource": "https://le.utah.gov/xcode/Title34A/Chapter2/C34A-2_1800010118000101.pdf",
        "publisher": "Utah State Legislature",
    },
    "VA": {
        "id": "primary-statute",
        "title": "Code of Virginia title 65.2",
        "resource": "https://law.lis.virginia.gov/vacodefull/title65.2/",
        "publisher": "Virginia Legislative Information System",
    },
    "VT": {
        "id": "primary-statute",
        "title": "Vermont Statutes title 21, chapter 9",
        "resource": "https://legislature.vermont.gov/statutes/fullchapter/21/009",
        "publisher": "Vermont General Assembly",
    },
    "WA": {
        "id": "primary-statute",
        "title": "Revised Code of Washington title 51",
        "resource": "https://lawfilesext.leg.wa.gov/law/RCWPDF/RCW%20%2051%20%20TITLE/RCW%20%2051%20%20%20TITLE/RCW%20%2051%20%20%20COMBINEDTITLE.pdf",
        "publisher": "Washington State Legislature",
    },
    "WI": {
        "id": "primary-statute",
        "title": "Wisconsin Statutes chapter 102",
        "resource": "https://docs.legis.wisconsin.gov/statutes/statutes/102.pdf",
        "publisher": "Wisconsin Legislature",
    },
    "WV": {
        "id": "primary-statute",
        "title": "West Virginia Code chapter 23",
        "resource": "https://code.wvlegislature.gov/pdf/23/",
        "publisher": "West Virginia Legislature",
    },
    "WY": {
        "id": "primary-statute",
        "title": "Wyoming Statutes title 27",
        "resource": "https://wyoleg.gov/statutes/compress/title27.pdf",
        "publisher": "Wyoming Legislature",
    },
    "CO": {
        "id": "primary-statute",
        "title": "Colorado Workers' Compensation Act",
        "resource": "https://codwc.app.box.com/index.php?rm=box_download_shared_file&shared_name=la4vib4v3nbzaz4schk9cig91i6jjerx&file_id=f_2401454809587",
        "publisher": "Colorado Division of Workers' Compensation",
    },
    "CT": {
        "id": "primary-statute",
        "title": "Connecticut General Statutes chapter 568",
        "resource": "https://www.cga.ct.gov/current/pub/chap_568.htm",
        "publisher": "Connecticut General Assembly",
        "text_file": "statutes/connecticut.txt",
        "retrieved_at": "2026-10-28T16:40:00Z",
    },
    "HI": {
        "id": "primary-statute",
        "title": "Hawaii Revised Statutes section 386-1",
        "resource": "https://capitolwebsite.azurewebsites.net/hrsarchive/hrs2025/Vol07_Ch0346-0398/HRS0386/HRS_0386-0001.htm",
        "publisher": "Hawaii State Legislature",
    },
    "FL": {
        "id": "primary-statute",
        "title": "Florida Statutes chapter 440",
        "resource": "http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0400-0499/0440/0440.html",
        "publisher": "Florida Legislature",
    },
    "IL": {
        "id": "primary-statute",
        "title": "Illinois Workers' Compensation Act",
        "resource": "https://www.ilga.gov/Legislation/ILCS/Articles?ActID=2430&ChapterID=68&Print=True",
        "publisher": "Illinois General Assembly",
        "text_file": "statutes/illinois.txt",
        "retrieved_at": "2026-10-28T16:40:00Z",
    },
    "IN": {
        "id": "primary-statute",
        "title": "Indiana Code title 22, article 3",
        "resource": "https://iga.in.gov/ic/2026/Title_22/Article_3.pdf",
        "publisher": "Indiana General Assembly",
    },
    "MT": {
        "id": "primary-statute",
        "title": "Montana Code Annotated section 39-71-101",
        "resource": "https://leg.mt.gov/bills/mca/title_0390/chapter_0710/part_0010/section_0010/0390-0710-0010-0010.html",
        "publisher": "Montana Legislative Services",
    },
    "NJ": {
        "id": "primary-statute",
        "title": "New Jersey Workers' Compensation Law",
        "resource": "https://www.nj.gov/labor/workerscompensation/assets/PDFs/Forms/wc_law.pdf",
        "publisher": "New Jersey Division of Workers' Compensation",
    },
    "NM": {
        "id": "primary-statute",
        "title": "New Mexico Statutes chapter 52",
        "resource": "https://nmonesource.com/nmos/nmsa-unanno/en/18555/1/document.do",
        "publisher": "New Mexico Compilation Commission",
    },
    "SD": {
        "id": "primary-statute",
        "title": "South Dakota Codified Laws section 62-1-1",
        "resource": "https://sdlegislature.gov/api/Statutes/Statute/62-1-1",
        "publisher": "South Dakota Legislative Research Council",
    },
    "TX": {
        "id": "primary-statute",
        "title": "Texas Workers' Compensation Act",
        "resource": "https://www.tdi.texas.gov/wc/act/documents/act89.pdf",
        "publisher": "Texas Department of Insurance, Division of Workers' Compensation",
    },
    "AL": {
        "id": "primary-statute",
        "title": "Code of Alabama section 25-5-1",
        "resource": "https://alison.legislature.state.al.us/code-of-alabama?section=25-5-1",
        "publisher": "Alabama Legislature",
        "text_file": "statutes/alabama.txt",
        "retrieved_at": "2026-10-28T16:45:00Z",
    },
    "AR": {
        "id": "agency-rules",
        "title": "Code of Arkansas Rules title 11, part 25",
        "resource": "https://webftp.blr.arkansas.gov/Home/FTPDocument?path=CAR%2FParts%2F11CARpt25.pdf",
        "publisher": "Arkansas Bureau of Legislative Research",
    },
    "CA": {
        "id": "primary-statute",
        "title": "California Labor Code division 4, part 1, chapter 1",
        "resource": "https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?article=&chapter=1.&division=4.&lawCode=LAB&part=1.&title=",
        "publisher": "California Legislative Counsel",
        "text_file": "statutes/california.txt",
        "retrieved_at": "2026-10-28T16:45:00Z",
    },
    "GA": {
        "id": "agency-rules",
        "title": "Rules and Regulations of the State Board of Workers' Compensation",
        "resource": "https://sbwc.georgia.gov/document/publication/2026-rules/download",
        "publisher": "Georgia State Board of Workers' Compensation",
    },
    "MS": {
        "id": "agency-rules",
        "title": "Rules of the Mississippi Workers' Compensation Commission",
        "resource": "https://www.mwcc.ms.gov/#/generalAndProceduralRules",
        "publisher": "Mississippi Workers' Compensation Commission",
        "text_file": "statutes/mississippi.txt",
        "retrieved_at": "2026-10-28T16:45:00Z",
    },
    "NY": {
        "id": "primary-statute",
        "title": "New York Workers' Compensation Law section 1",
        "resource": "https://www.nysenate.gov/legislation/laws/WKC/1",
        "publisher": "New York State Senate",
        "text_file": "statutes/new-york.txt",
        "retrieved_at": "2026-10-28T16:45:00Z",
    },
    "TN": {
        "id": "agency-rules",
        "title": "Tennessee Rules chapter 0800-02-01",
        "resource": "https://publications.tnsosfiles.com/rules/0800/0800-02/0800-02-01.20180531.pdf",
        "publisher": "Tennessee Secretary of State",
    },
}

# act: the workers' compensation statute, or the chapter that is that statute.
# chapter: a multi-section piece of the act, not the benefit statute.
# section: one section.
# rules: agency rules. Arkansas, Georgia, Mississippi, and Tennessee publish
# the code through Lexis, so the catalog keeps the official rules.
COVERAGE = {
    "AK": "act",
    "AL": "section",
    "AR": "rules",
    "AZ": "section",
    "CA": "section",
    "CO": "act",
    "CT": "act",
    "DC": "act",
    "DE": "act",
    "FL": "act",
    "GA": "rules",
    "HI": "section",
    "IA": "act",
    "ID": "chapter",
    "IL": "act",
    "IN": "act",
    "KS": "section",
    "KY": "section",
    "LA": "section",
    "MA": "section",
    "MD": "act",
    "ME": "act",
    "MI": "act",
    "MN": "act",
    "MO": "section",
    "MS": "rules",
    "MT": "section",
    "NC": "act",
    "ND": "chapter",
    "NE": "section",
    "NH": "act",
    "NJ": "act",
    "NM": "act",
    "NV": "chapter",
    "NY": "section",
    "OH": "act",
    "OK": "act",
    "OR": "act",
    "PA": "act",
    "RI": "section",
    "SC": "chapter",
    "SD": "section",
    "TN": "rules",
    "TX": "act",
    "UT": "act",
    "VA": "act",
    "VT": "act",
    "WA": "act",
    "WI": "act",
    "WV": "act",
    "WY": "act",
}


def catalog_entries(postal: str) -> list[dict]:
    entry = dict(VERIFIED_REGULATIONS[postal])
    entry["coverage"] = COVERAGE[postal]
    return [entry]

_SKIP = {"script", "style", "noscript"}
_BLOCKS = {
    "p",
    "div",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "li",
    "tr",
    "br",
    "section",
    "article",
    "blockquote",
    "caption",
}


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip = 0
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in _SKIP:
            self._skip += 1
        elif tag in _BLOCKS and self._skip == 0:
            self._parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in _SKIP and self._skip:
            self._skip -= 1
        elif tag in _BLOCKS and self._skip == 0:
            self._parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip == 0:
            self._parts.append(data)

    def text(self) -> str:
        raw = "".join(self._parts)
        lines = [" ".join(line.split()) for line in raw.splitlines()]
        cleaned = "\n".join(line for line in lines if line)
        return cleaned.strip()


def html_to_text(html: str) -> str:
    parser = _TextExtractor()
    parser.feed(html)
    parser.close()
    return parser.text()


def pdf_to_text(data: bytes) -> str:
    reader = PdfReader(BytesIO(data))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(part.strip() for part in pages if part.strip()).strip()


def _is_pdf(data: bytes, content_type: str) -> bool:
    kind = content_type.lower()
    return "pdf" in kind or data.startswith(b"%PDF")


def default_fetch(url: str) -> tuple[bytes, str]:
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/pdf,application/xhtml+xml,*/*",
        },
    )
    context = ssl.create_default_context(cafile=certifi.where())
    with urlopen(request, timeout=60, context=context) as response:
        content_type = response.headers.get("Content-Type", "")
        return response.read(), content_type


def _html_from_json(decoded: str, content_type: str) -> str | None:
    looks_like_json = "json" in content_type.lower() or decoded.lstrip().startswith("{")
    if not looks_like_json:
        return None
    try:
        payload = json.loads(decoded)
    except json.JSONDecodeError:
        return None
    html = payload.get("Html") if isinstance(payload, dict) else None
    if isinstance(html, str) and html.strip():
        return html
    return None


def document_from_response(data: bytes, content_type: str) -> dict:
    digest = hashlib.sha256(data).hexdigest()
    if _is_pdf(data, content_type):
        text = pdf_to_text(data)
        kind = "application/pdf"
        text_layer = bool(text)
    else:
        charset = "utf-8"
        if "charset=" in content_type.lower():
            charset = content_type.lower().split("charset=", 1)[1].split(";", 1)[0].strip()
        decoded = data.decode(charset, errors="replace")
        html = _html_from_json(decoded, content_type)
        text = html_to_text(html if html is not None else decoded)
        kind = "text/html" if html is not None else (content_type.split(";", 1)[0] or "text/html")
        text_layer = True
    return {
        "content_type": kind,
        "sha256": digest,
        "text": text,
        "text_layer": text_layer,
    }


def apply_verified_catalog(root=None) -> None:
    import wiki

    for item in wiki.load_jurisdictions(root):
        if item.postal in VERIFIED_REGULATIONS:
            wiki.replace_regulations(item.path, catalog_entries(item.postal))


def choose_entry(catalog: list[dict], source_id: str | None) -> dict | None:
    if source_id is None:
        for entry in catalog:
            if entry.get("id") == "primary-statute":
                return entry
        return catalog[0] if catalog else None
    for entry in catalog:
        if entry.get("id") == source_id:
            return entry
    return None


_SECTION_LINE = re.compile(
    r"(?:§|\bSec(?:tion)?\.?|\b\d{1,3}[.:-]\d)",
    re.I,
)


def section_text(text: str, citation: str) -> str | None:
    """Return the passage that starts at citation, through the next section heading."""
    needle = citation.replace("\u2013", "-").replace("\u2014", "-").strip()
    if not needle:
        return None
    folded = text.replace("\u2013", "-").replace("\u2014", "-")
    start = folded.lower().find(needle.lower())
    if start < 0:
        return None
    rest = text[start : start + 12000]
    match = _SECTION_LINE.search(rest, len(needle) + 1)
    if match:
        rest = rest[: match.start()]
    excerpt = rest.strip()
    return excerpt or None


def _ok_document(jurisdiction, chosen, when, extracted) -> dict:
    return {
        "status": "ok",
        "postal": jurisdiction.postal,
        "name": jurisdiction.name,
        "source_id": chosen.get("id"),
        "title": chosen.get("title"),
        "publisher": chosen.get("publisher"),
        "coverage": chosen.get("coverage"),
        "retrieval": "stored" if chosen.get("text_file") else "live",
        "resource": chosen["resource"],
        "retrieved_at": when,
        **extracted,
    }


def regulation_response(
    jurisdiction,
    source_id: str | None = None,
    fetch=default_fetch,
    retrieved_at: str | None = None,
    section: str | None = None,
) -> dict:
    catalog = jurisdiction.regulations
    if not catalog:
        return {
            "status": "uncatalogued",
            "postal": jurisdiction.postal,
            "name": jurisdiction.name,
            "citation": jurisdiction.primary_law,
            "agency_resource": jurisdiction.agency.get("resource"),
        }
    chosen = choose_entry(catalog, source_id)
    if chosen is None:
        return {
            "status": "unknown_source",
            "postal": jurisdiction.postal,
            "source_id": source_id,
            "available": [entry.get("id") for entry in catalog],
        }
    when = retrieved_at or chosen.get("retrieved_at") or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    text_file = chosen.get("text_file")
    if text_file:
        path = jurisdiction.path.parent.parent / text_file
        data = path.read_bytes()
        extracted = {
            "content_type": "text/plain",
            "sha256": hashlib.sha256(data).hexdigest(),
            "text": data.decode("utf-8"),
            "text_layer": True,
        }
    else:
        url = chosen["resource"]
        try:
            data, content_type = fetch(url)
        except Exception as exc:
            return {
                "status": "fetch_error",
                "postal": jurisdiction.postal,
                "name": jurisdiction.name,
                "source_id": chosen.get("id"),
                "title": chosen.get("title"),
                "publisher": chosen.get("publisher"),
                "coverage": chosen.get("coverage"),
                "retrieval": "live",
                "resource": url,
                "error": f"{type(exc).__name__}: {exc}",
            }
        extracted = document_from_response(data, content_type)
    if section:
        excerpt = section_text(extracted["text"], section)
        if excerpt is None:
            return {
                "status": "section_not_found",
                "postal": jurisdiction.postal,
                "name": jurisdiction.name,
                "source_id": chosen.get("id"),
                "title": chosen.get("title"),
                "section": section,
                "resource": chosen["resource"],
            }
        extracted = {**extracted, "text": excerpt, "section": section}
    return _ok_document(jurisdiction, chosen, when, extracted)
