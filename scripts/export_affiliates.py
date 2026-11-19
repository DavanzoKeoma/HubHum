"""Export affiliate merchant catalog from an optional SQLite source DB to data/affiliates_seed.json."""

from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "data" / "affiliates_seed.json"

CONSUMER_BASE_URLS: dict[str, str] = {
    "MER_047": "https://billing.purevpn.com/aff.php?aff=49386762",
    "MER_089": "https://surfshark.com/",
    "MER_048": "https://www.privateinternetaccess.com/",
    "MER_064": "https://torguard.net/",
    "MER_008": "https://www.interserver.net/r/1196747?id={clickid}",
    "MER_009": "https://www.scalahosting.com/",
    "MER_014": "https://www.rosehosting.com/",
    "MER_054": "https://www.creativefabrica.com/promo/yearly/ref/29328369/?subid=[clickid]",
    "MER_349": "https://elements.envato.com/",
    "MER_369": "https://placeit.net/",
    "MER_269": "https://wp-rocket.me/",
    "MER_276": "https://rankmath.com/",
    "MER_265": "https://elementor.com/",
    "MER_023": "https://themeisle.com/",
}

TRIPLET_DEFINITIONS: dict[str, list[dict[str, str]]] = {
    "privacy_security": [
        {
            "merchant_id": "MER_047",
            "context_role": "connection_privacy",
            "section_hint": "### How to install (Download)",
            "tip_template": "Before downloading installers or syncing private files over public Wi-Fi, shield your connection with [PureVPN]({url}) (#ad).",
        },
        {
            "merchant_id": "MER_008",
            "context_role": "private_cloud_backup",
            "section_hint": "### What it does in plain English",
            "tip_template": "For full control over encrypted off-site backups and private syncing, pair your setup with cloud storage on [InterServer]({url}) (#ad).",
        },
        {
            "merchant_id": "MER_054",
            "context_role": "productivity_assets",
            "section_hint": "### Key features",
            "tip_template": "Ready-to-use digital planners, printable checklists, and clean document templates for daily organization via [Creative Fabrica]({url}) (#ad).",
        },
    ],
    "graphics_video_design": [
        {
            "merchant_id": "MER_054",
            "context_role": "fonts_templates",
            "section_hint": "### Key features",
            "tip_template": "Expand your creative library with commercial-safe fonts, lower-third templates, and overlays from [Creative Fabrica]({url}) (#ad).",
        },
        {
            "merchant_id": "MER_349",
            "context_role": "stock_media",
            "section_hint": "### What it does in plain English",
            "tip_template": "When you need royalty-free stock footage, music tracks, and motion presets alongside your edits, check out [Envato Elements Direct]({url}) (#ad).",
        },
        {
            "merchant_id": "MER_047",
            "context_role": "fast_private_transfers",
            "section_hint": "### How to install (Download)",
            "tip_template": "Keep large installer downloads and media transfers private without ISP bandwidth throttling via [PureVPN]({url}) (#ad).",
        },
    ],
    "webapp_cms": [
        {
            "merchant_id": "MER_008",
            "context_role": "managed_cloud_hosting",
            "section_hint": "### How to install (Download)",
            "tip_template": "Prefer not to manage servers by hand? Run it online 24/7 in 1 click on [InterServer]({url}) (#ad).",
        },
        {
            "merchant_id": "MER_276",
            "context_role": "seo_visibility",
            "section_hint": "### Key features",
            "tip_template": "Once your web portal is live, improve search indexing and rich previews with [Rank Math Direct]({url}) (#ad).",
        },
        {
            "merchant_id": "MER_047",
            "context_role": "admin_session_security",
            "section_hint": "### What it does in plain English",
            "tip_template": "Protect remote administrator dashboards when managing your site on the go with [PureVPN]({url}) (#ad).",
        },
    ],
    "webdev_wordpress": [
        {
            "merchant_id": "MER_276",
            "context_role": "seo_growth",
            "section_hint": "### Key features",
            "tip_template": "Help everyday readers find your site faster on search engines with structured tools from [Rank Math Direct]({url}) (#ad).",
        },
        {
            "merchant_id": "MER_269",
            "context_role": "page_speed_caching",
            "section_hint": "### What it does in plain English",
            "tip_template": "Pair clean publishing with instant page caching to keep loading times snappy using [WP Rocket Direct]({url}) (#ad).",
        },
        {
            "merchant_id": "MER_008",
            "context_role": "reliable_cloud_hosting",
            "section_hint": "### How to install (Download)",
            "tip_template": "Run your finished project on dependable, budget-friendly cloud hosting via [InterServer]({url}) (#ad).",
        },
    ],
}

CATEGORY_MAPPING: dict[str, dict[str, object]] = {
    "privacy_security": {
        "label": "Privacy, Torrenting & Security",
        "human_tags": ["privacy", "security", "vpn", "password", "torrent", "notes"],
        "merchant_ids": ["MER_047", "MER_089", "MER_048", "MER_064"],
        "injection_message": "Protect your connection before downloading or using this app.",
        "cta_label": "Protect your privacy",
        "i18n": {
            "it": {
                "injection_message": "Proteggi la tua connessione prima di scaricare o usare questa app.",
                "cta_label": "Proteggi la tua privacy",
            },
            "es": {
                "injection_message": "Protege tu conexión antes de descargar o usar esta aplicación.",
                "cta_label": "Protege tu privacidad",
            },
            "fr": {
                "injection_message": "Protégez votre connexion avant de télécharger ou d'utiliser cette application.",
                "cta_label": "Protégez votre vie privée",
            },
            "de": {
                "injection_message": "Schützen Sie Ihre Verbindung, bevor Sie diese App herunterladen oder nutzen.",
                "cta_label": "Privatsphäre schützen",
            },
        },
    },
    "webapp_cms": {
        "label": "Web Apps, CMS & Cloud Tools",
        "human_tags": ["webapp", "cms", "cloud", "self-hosted", "blog", "automation"],
        "merchant_ids": ["MER_008", "MER_009", "MER_014"],
        "injection_message": "Prefer not to configure a server manually? Launch it in 1 click on managed cloud hosting.",
        "cta_label": "Open in Cloud (1-Click)",
        "i18n": {
            "it": {
                "injection_message": "Non vuoi configurare un server a mano? Avvialo in 1 click su un hosting cloud gestito.",
                "cta_label": "Apri nel Cloud (1-Click)",
            },
            "es": {
                "injection_message": "¿No quieres configurar un servidor manualmente? Ábrelo en 1 clic en un hosting optimizado.",
                "cta_label": "Abrir en la Nube (1-Clic)",
            },
            "fr": {
                "injection_message": "Vous ne voulez pas configurer un serveur manuellement ? Lancez-le en 1 clic sur un hébergement optimisé.",
                "cta_label": "Ouvrir dans le Cloud (1-Clic)",
            },
            "de": {
                "injection_message": "Sie möchten keinen Server manuell einrichten? Starten Sie die App mit 1 Klick auf optimiertem Cloud-Hosting.",
                "cta_label": "In der Cloud öffnen (1-Klick)",
            },
        },
    },
    "graphics_video_design": {
        "label": "Graphics, Video & Audio",
        "human_tags": ["graphics", "video", "design", "audio", "editing", "images"],
        "merchant_ids": ["MER_349", "MER_054", "MER_369"],
        "injection_message": "Download ready-to-use fonts, templates, and creative assets for your projects.",
        "cta_label": "Browse ready-to-use templates",
        "i18n": {
            "it": {
                "injection_message": "Scarica font, template e asset creativi pronti all'uso per i tuoi progetti.",
                "cta_label": "Esplora template e asset pronti",
            },
            "es": {
                "injection_message": "Descarga fuentes, plantillas y recursos creativos listos para usar en tus proyectos.",
                "cta_label": "Explorar plantillas listas",
            },
            "fr": {
                "injection_message": "Téléchargez des polices, modèles et ressources créatives prêts à l'emploi pour vos projets.",
                "cta_label": "Explorer les modèles prêts",
            },
            "de": {
                "injection_message": "Laden Sie sofort nutzbare Schriftarten, Vorlagen und Kreativ-Assets für Ihre Projekte herunter.",
                "cta_label": "Vorlagen & Assets entdecken",
            },
        },
    },
    "webdev_wordpress": {
        "label": "Websites & Publishing",
        "human_tags": ["wordpress", "seo", "websites", "ecommerce", "landing", "productivity"],
        "merchant_ids": ["MER_269", "MER_276", "MER_265", "MER_023"],
        "injection_message": "Build and optimize your website faster with industry-standard tools.",
        "cta_label": "Explore website tools",
        "i18n": {
            "it": {
                "injection_message": "Costruisci e ottimizza il tuo sito più velocemente con strumenti professionali.",
                "cta_label": "Scopri gli strumenti web",
            },
            "es": {
                "injection_message": "Crea y optimiza tu sitio web más rápido con herramientas estándar del sector.",
                "cta_label": "Explorar herramientas web",
            },
            "fr": {
                "injection_message": "Créez et optimisez votre site web plus rapidement avec des outils de référence.",
                "cta_label": "Découvrir les outils web",
            },
            "de": {
                "injection_message": "Erstellen und optimieren Sie Ihre Website schneller mit bewährten Standard-Tools.",
                "cta_label": "Website-Tools entdecken",
            },
        },
    },
}

TARGET_MERCHANT_IDS = tuple(
    dict.fromkeys(
        [mid for cfg in CATEGORY_MAPPING.values() for mid in cfg["merchant_ids"]]  # type: ignore[index]
        + [item["merchant_id"] for items in TRIPLET_DEFINITIONS.values() for item in items]
    )
)


def build_subid(merchant_id: str) -> str:
    """Generate dedicated HubHum SubID (e.g. MER_047 -> hubhum_01_MER047)."""
    clean_id = merchant_id.replace("_", "")
    return f"hubhum_01_{clean_id}"


def apply_subid_to_url(raw_url: str, subid: str) -> str:
    """Inject the HubHum SubID into a tracked affiliate template or consumer landing URL."""
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
    """Read target merchants and active link configs in read-only mode, auditing direct-link policy."""
    uri = f"file:{db_path.as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        placeholders = ",".join("?" for _ in TARGET_MERCHANT_IDS)
        merchant_rows = cur.execute(
            f"""
            SELECT ID_Merchant, Nome, Network_Affiliazione, Categoria,
                   Direct_Linking_Permesso, Richiede_Bridge_Page, PPC_Policy, URL_Policy,
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


def _build_merchant_entry(mid: str, cat_key: str, m: dict, link_cfg: dict | None) -> dict:
    direct_ok = m["Direct_Linking_Permesso"] == "Sì"
    bridge_ok = (m.get("Richiede_Bridge_Page") or "No") == "No"
    if not (direct_ok and bridge_ok):
        raise RuntimeError(
            f"Policy Direct-Link violata per {mid} ({m['Nome']}): "
            f"Direct_Linking={m['Direct_Linking_Permesso']}, Bridge={m.get('Richiede_Bridge_Page')}"
        )

    subid = build_subid(mid)
    raw_template = link_cfg["URL_Affiliato"] if link_cfg else CONSUMER_BASE_URLS.get(mid, m["URL_Policy"])
    tracking_url = apply_subid_to_url(raw_template, subid)
    has_verified_tracking = bool(link_cfg) or ("aff=" in (m.get("URL_Policy") or ""))

    return {
        "merchant_id": mid,
        "name": m["Nome"],
        "category_key": cat_key,
        "subid": subid,
        "tracking_url": tracking_url,
        "policy_url": m["URL_Policy"],
        "network": m["Network_Affiliazione"],
        "direct_linking_allowed": True,
        "bridge_page_required": False,
        "ppc_policy": m["PPC_Policy"],
        "brand_bidding_forbidden": True,
        "disclosure_required": True,
        "disclosure_text": m["Testo_Disclosure_Consigliato"],
        "priority_score": float(m["Priorita_Score"] or 0),
        "epc_target": m["EPC_Target"],
        "verified_tracking_link": has_verified_tracking,
    }


def build_seed_payload(db_path: Path) -> dict:
    """Build the clean, secret-free affiliates_seed.json structure with 3-link contextual triplets."""
    merchants, active_links = fetch_merchants_from_db(db_path)

    categories_out: dict[str, dict] = {}
    merchants_index: dict[str, dict] = {}

    for mid in TARGET_MERCHANT_IDS:
        m = merchants.get(mid)
        if not m:
            raise RuntimeError(f"Merchant {mid} non trovato nel database {db_path}")
        cat_key = next((ck for ck, cfg in CATEGORY_MAPPING.items() if mid in cfg["merchant_ids"]), "webapp_cms")  # type: ignore[operator]
        merchants_index[mid] = _build_merchant_entry(mid, cat_key, m, active_links.get(mid))

    for cat_key, cat_cfg in CATEGORY_MAPPING.items():
        cat_merchants = [merchants_index[mid] for mid in cat_cfg["merchant_ids"]]  # type: ignore[index]
        cat_merchants.sort(key=lambda x: (x["verified_tracking_link"], x["priority_score"]), reverse=True)

        triplet_out = []
        for tdef in TRIPLET_DEFINITIONS[cat_key]:
            m_entry = merchants_index[tdef["merchant_id"]]
            triplet_out.append(
                {
                    "merchant_id": m_entry["merchant_id"],
                    "name": m_entry["name"],
                    "tracking_url": m_entry["tracking_url"],
                    "subid": m_entry["subid"],
                    "context_role": tdef["context_role"],
                    "section_hint": tdef["section_hint"],
                    "natural_tip": tdef["tip_template"].format(url=m_entry["tracking_url"]),
                }
            )

        categories_out[cat_key] = {
            "label": cat_cfg["label"],
            "human_tags": cat_cfg["human_tags"],
            "injection_message": cat_cfg["injection_message"],
            "cta_label": cat_cfg["cta_label"],
            "i18n": cat_cfg["i18n"],
            "primary_merchant_id": cat_merchants[0]["merchant_id"],
            "merchants": cat_merchants,
            "recommended_triplet": triplet_out,
        }

    return {
        "schema_version": "1.2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "hubhum-curated-catalog-v2",
        "subid_prefix": "hubhum_01_",
        "direct_link_policy_audited": True,
        "compliance": {
            "ftc_disclosure_en": (
                "Affiliate transparency (#ad): Some links on HubHum are affiliate links. "
                "If you purchase a service through them, we may earn a commission at no extra cost to you."
            ),
            "github_disclaimer": "HubHum is an independent tool and is not affiliated with GitHub, Inc.",
            "brand_bidding_allowed": False,
        },
        "total_merchants": len(merchants_index),
        "categories": categories_out,
        "merchants_by_id": merchants_index,
    }


def main() -> None:
    env_db = os.environ.get("AFFILIATE_SOURCE_DB_PATH", "").strip()
    if not env_db:
        raise RuntimeError("Set AFFILIATE_SOURCE_DB_PATH to regenerate affiliates_seed.json.")
    db_path = Path(env_db)
    if not db_path.exists():
        raise FileNotFoundError(f"Source database not found: {db_path}")

    payload = build_seed_payload(db_path)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Exported {payload['total_merchants']} merchants (policy audited, 3x triplets) to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
