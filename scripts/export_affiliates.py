"""Export affiliate merchant catalog from local affiliatechproject SQLite DB to data/affiliates_seed.json."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

DEFAULT_DB_PATH = Path(r"C:\Users\keoma\Desktop\affiliatechproject\data\affiliatechproject_db.sqlite")
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "data" / "affiliates_seed.json"

CATEGORY_MAPPING: dict[str, dict[str, object]] = {
    "privacy_security": {
        "label": "Privacy, torrenting, sicurezza",
        "human_tags": ["privacy", "sicurezza", "vpn", "password", "torrent", "security"],
        "merchant_ids": ["MER_047", "MER_089", "MER_048", "MER_064"],
        "injection_message": "Proteggi la tua connessione prima di scaricare o usare questa app.",
        "cta_label": "Proteggi la tua privacy",
    },
    "webapp_cms": {
        "label": "Web app, CMS, gestionali",
        "human_tags": ["webapp", "cms", "gestionale", "cloud", "self-hosted", "blog", "crm"],
        "merchant_ids": ["MER_008", "MER_009", "MER_014"],
        "injection_message": "Non vuoi installarlo a mano su un server? Avvialo in 1 click su un hosting ottimizzato.",
        "cta_label": "Lancia nel Cloud (1-Click)",
    },
    "graphics_video_design": {
        "label": "Grafica, video, design",
        "human_tags": ["grafica", "video", "design", "audio", "editing", "immagini", "video-editor"],
        "merchant_ids": ["MER_349", "MER_054", "MER_369"],
        "injection_message": "Scarica font, template e asset pronti da usare con questo programma.",
        "cta_label": "Esplora template e asset pronti",
    },
    "webdev_wordpress": {
        "label": "Sviluppo web e WordPress",
        "human_tags": ["wordpress", "seo", "siti-web", "ecommerce", "webdev", "landing"],
        "merchant_ids": ["MER_269", "MER_276", "MER_265", "MER_023"],
        "injection_message": "Ottimizza o costruisci il tuo sito con gli standard di settore.",
        "cta_label": "Scopri gli strumenti per il tuo sito",
    },
}

TARGET_MERCHANT_IDS = tuple(
    mid for cfg in CATEGORY_MAPPING.values() for mid in cfg["merchant_ids"]  # type: ignore[index]
)


def build_subid(merchant_id: str) -> str:
    """Generate dedicated HubHum SubID (e.g. MER_047 -> hubhum_01_MER047)."""
    clean_id = merchant_id.replace("_", "")
    return f"hubhum_01_{clean_id}"


def apply_subid_to_url(raw_url: str, subid: str) -> str:
    """Inject the HubHum SubID into a tracked affiliate template or fallback URL."""
    if not raw_url:
        return ""
    if "[clickid]" in raw_url:
        return raw_url.replace("[clickid]", subid)
    if "{clickid}" in raw_url:
        return raw_url.replace("{clickid}", subid)

    parsed = urlparse(raw_url)
    query_params = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query_params.setdefault("subid", subid)
    new_query = urlencode(query_params)
    return urlunparse(parsed._replace(query=new_query))


def fetch_merchants_from_db(db_path: Path) -> tuple[dict[str, dict], dict[str, dict]]:
    """Read target merchants and active link configs in read-only mode."""
    uri = f"file:{db_path.as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        placeholders = ",".join("?" for _ in TARGET_MERCHANT_IDS)
        merchant_rows = cur.execute(
            f"""
            SELECT ID_Merchant, Nome, Network_Affiliazione, Categoria,
                   Direct_Linking_Permesso, PPC_Policy, URL_Policy,
                   Disclosure_Richiesta, Testo_Disclosure_Consigliato,
                   Commissione_Media, Priorita_Score, EPC_Target, Status_URL
            FROM Merchant
            WHERE ID_Merchant IN ({placeholders})
            """,
            TARGET_MERCHANT_IDS,
        ).fetchall()
        merchants = {row["ID_Merchant"]: dict(row) for row in merchant_rows}

        link_rows = cur.execute(
            f"""
            SELECT ID_Link, ID_Merchant, URL_Affiliato, SubID_Parametro,
                   URL_Finale_Testato, Stato_Link, Ultima_Verifica, Note
            FROM Configurazione_Link
            WHERE ID_Merchant IN ({placeholders}) AND Stato_Link = 'Attivo'
            """,
            TARGET_MERCHANT_IDS,
        ).fetchall()
        links = {row["ID_Merchant"]: dict(row) for row in link_rows}
        return merchants, links
    finally:
        conn.close()


def build_seed_payload(db_path: Path = DEFAULT_DB_PATH) -> dict:
    """Build the clean, secret-free affiliates_seed.json structure."""
    merchants, active_links = fetch_merchants_from_db(db_path)

    categories_out: dict[str, dict] = {}
    merchants_index: dict[str, dict] = {}

    for cat_key, cat_cfg in CATEGORY_MAPPING.items():
        cat_merchants = []
        for mid in cat_cfg["merchant_ids"]:  # type: ignore[index]
            m = merchants.get(mid)
            if not m:
                raise RuntimeError(f"Merchant {mid} non trovato nel database {db_path}")

            subid = build_subid(mid)
            link_cfg = active_links.get(mid)
            raw_template = link_cfg["URL_Affiliato"] if link_cfg else m["URL_Policy"]
            tracking_url = apply_subid_to_url(raw_template, subid)
            has_verified_tracking = bool(link_cfg) or ("aff=" in (m.get("URL_Policy") or ""))

            entry = {
                "merchant_id": mid,
                "name": m["Nome"],
                "category_key": cat_key,
                "subid": subid,
                "tracking_url": tracking_url,
                "policy_url": m["URL_Policy"],
                "network": m["Network_Affiliazione"],
                "direct_linking_allowed": m["Direct_Linking_Permesso"] == "Sì",
                "ppc_policy": m["PPC_Policy"],
                "brand_bidding_forbidden": True,
                "disclosure_required": True,
                "disclosure_text": m["Testo_Disclosure_Consigliato"],
                "priority_score": float(m["Priorita_Score"] or 0),
                "epc_target": m["EPC_Target"],
                "verified_tracking_link": has_verified_tracking,
            }
            cat_merchants.append(entry)
            merchants_index[mid] = entry

        # Sort by verified tracking link first, then priority_score descending
        cat_merchants.sort(key=lambda x: (x["verified_tracking_link"], x["priority_score"]), reverse=True)

        categories_out[cat_key] = {
            "label": cat_cfg["label"],
            "human_tags": cat_cfg["human_tags"],
            "injection_message": cat_cfg["injection_message"],
            "cta_label": cat_cfg["cta_label"],
            "primary_merchant_id": cat_merchants[0]["merchant_id"],
            "merchants": cat_merchants,
        }

    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "affiliatechproject_db.sqlite (sanitized export, no secrets)",
        "subid_prefix": "hubhum_01_",
        "compliance": {
            "ftc_disclosure_it": (
                "Trasparenza affiliazioni (#ad): Alcuni link presenti su HubHum sono link di "
                "affiliazione. Se acquisti un servizio tramite questi link potremmo ricevere "
                "una commissione, senza costi aggiuntivi per te."
            ),
            "github_disclaimer": "HubHum is an independent tool and is not affiliated with GitHub, Inc.",
            "brand_bidding_allowed": False,
        },
        "total_merchants": len(merchants_index),
        "categories": categories_out,
        "merchants_by_id": merchants_index,
    }


def main() -> None:
    if not DEFAULT_DB_PATH.exists():
        raise FileNotFoundError(f"Database affiliatechproject non trovato: {DEFAULT_DB_PATH}")

    payload = build_seed_payload(DEFAULT_DB_PATH)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Esportati {payload['total_merchants']} merchant in {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
