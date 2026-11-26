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
    "MER_119": "https://adguard.com/?aid=138327",
    "MER_096": "https://fastestvpn.com/pro-lifetime-deal?a_aid=f17al0282rd89",
    "MER_008": "https://www.interserver.net/vps?id=1196747&sid={clickid}",
    "MER_063": "https://www.greengeeks.com/track/affiliatechproject/cp-ffltc/lp-1",
    "MER_062": "https://hosting.com/hosting/vps-hosting/managed/linux/?utm_source=fp_affiliate&utm_medium=15437677&utm_campaign=42825&utm_content=affiliates&fpr=h37jvi",
    "MER_054": "https://www.creativefabrica.com/promo/yearly/ref/29328369/?subid=[clickid]",
    "MER_061": "https://systeme.io/?sa=sa023692845080664785297106081136cf8d3a59ee",
}

CATEGORY_URL_OVERRIDES: dict[tuple[str, str], str] = {
    ("webapp_cms", "MER_008"): "https://www.interserver.net/vps?id=1196747&sid=hubhum_01_MER008",
    ("webapp_cms", "MER_062"): "https://hosting.com/hosting/vps-hosting/managed/linux/?utm_source=fp_affiliate&utm_medium=15437677&utm_campaign=42825&utm_content=affiliates&fpr=h37jvi&subid=hubhum_01_MER062",
    ("webdev_wordpress", "MER_008"): "https://www.interserver.net/webhosting?id=1196747&sid=hubhum_01_MER008",
    ("webdev_wordpress", "MER_062"): "https://hosting.com/hosting/platforms/wordpress-hosting/?utm_source=fp_affiliate&utm_medium=15437677&utm_campaign=42825&utm_content=affiliates&fpr=h37jvi&subid=hubhum_01_MER062",
    ("productivity_utilities", "MER_008"): "https://www.interserver.net/vps?id=1196747&sid=hubhum_01_MER008",
}

VERIFIED_TRACKING_TOKENS = (
    "aff=",
    "aid=",
    "a_aid=",
    "id=1196747",
    "/track/affiliatechproject/",
    "fpr=",
    "rid=",
    "/ref/29328369",
    "sa=",
)

TRIPLET_DEFINITIONS: dict[str, list[dict[str, str]]] = {
    "privacy_security": [
        {
            "merchant_id": "MER_047",
            "context_role": "connection_privacy",
            "section_hint": "### Sponsored Partner Tools (#ad)",
            "tip_template": "Before downloading installers or syncing private files over public Wi-Fi, shield your connection with [PureVPN]({url}) (#ad).",
        },
        {
            "merchant_id": "MER_119",
            "context_role": "system_adblock_privacy",
            "section_hint": "### Sponsored Partner Tools (#ad)",
            "tip_template": "Block intrusive ads, tracking scripts, and phishing domains system-wide across browsers and apps with [AdGuard]({url}) (#ad).",
        },
        {
            "merchant_id": "MER_096",
            "context_role": "lifetime_vpn_tunnel",
            "section_hint": "### Sponsored Partner Tools (#ad)",
            "tip_template": "Protect every device with WireGuard VPN encryption and built-in malware filtering via [FastestVPN]({url}) (#ad).",
        },
    ],
    "webapp_cms": [
        {
            "merchant_id": "MER_008",
            "context_role": "managed_cloud_vps",
            "section_hint": "### Sponsored Partner Tools (#ad)",
            "tip_template": "Launch and host self-hosted web apps and Local AI stacks 24/7 on Linux Cloud VPS servers starting at $3/month with [InterServer VPS]({url}) (#ad).",
        },
        {
            "merchant_id": "MER_063",
            "context_role": "eco_managed_hosting",
            "section_hint": "### Sponsored Partner Tools (#ad)",
            "tip_template": "Run web apps on 300% green-energy SSD hosting with free SSL, nightly backups, and 1-click setup via [GreenGeeks]({url}) (#ad).",
        },
        {
            "merchant_id": "MER_062",
            "context_role": "high_speed_managed_vps",
            "section_hint": "### Sponsored Partner Tools (#ad)",
            "tip_template": "Scale self-hosted web workspaces and databases with high-speed Managed Linux VPS on [Hosting.com (ex A2 Hosting)]({url}) (#ad).",
        },
    ],
    "graphics_video_design": [
        {
            "merchant_id": "MER_054",
            "context_role": "fonts_templates",
            "section_hint": "### Sponsored Partner Tools (#ad)",
            "tip_template": "Download commercial-safe fonts, SVG bundles, and ready-to-use creative templates with [Creative Fabrica]({url}) (#ad).",
        },
        {
            "merchant_id": "MER_061",
            "context_role": "creator_showcase_funnels",
            "section_hint": "### Sponsored Partner Tools (#ad)",
            "tip_template": "Build portfolio pages, digital product storefronts, and automated email delivery free forever with [Systeme.io]({url}) (#ad).",
        },
        {
            "merchant_id": "MER_047",
            "context_role": "fast_private_transfers",
            "section_hint": "### Sponsored Partner Tools (#ad)",
            "tip_template": "Keep large installer downloads and media asset transfers encrypted and private on public networks via [PureVPN]({url}) (#ad).",
        },
    ],
    "webdev_wordpress": [
        {
            "merchant_id": "MER_008",
            "context_role": "reliable_web_hosting",
            "section_hint": "### Sponsored Partner Tools (#ad)",
            "tip_template": "Run your website or publishing stack 24/7 on dependable, price-locked web hosting via [InterServer Web Hosting]({url}) (#ad).",
        },
        {
            "merchant_id": "MER_063",
            "context_role": "eco_wordpress_hosting",
            "section_hint": "### Sponsored Partner Tools (#ad)",
            "tip_template": "Launch fast WordPress and publishing sites with free domain, SSL, and LiteSpeed caching on [GreenGeeks]({url}) (#ad).",
        },
        {
            "merchant_id": "MER_062",
            "context_role": "managed_wordpress_hosting",
            "section_hint": "### Sponsored Partner Tools (#ad)",
            "tip_template": "Accelerate dynamic websites and publishing dashboards with Managed WordPress NVMe servers on [Hosting.com (ex A2 Hosting)]({url}) (#ad).",
        },
    ],
    "productivity_utilities": [
        {
            "merchant_id": "MER_061",
            "context_role": "all_in_one_workspace",
            "section_hint": "### Sponsored Partner Tools (#ad)",
            "tip_template": "Organize client funnels, newsletters, and automated everyday workflows on a free-forever plan with [Systeme.io]({url}) (#ad).",
        },
        {
            "merchant_id": "MER_119",
            "context_role": "distraction_free_browsing",
            "section_hint": "### Sponsored Partner Tools (#ad)",
            "tip_template": "Speed up everyday browsing and block trackers and pop-ups system-wide with [AdGuard]({url}) (#ad).",
        },
        {
            "merchant_id": "MER_008",
            "context_role": "cloud_backup_storage",
            "section_hint": "### Sponsored Partner Tools (#ad)",
            "tip_template": "Store off-site backups and private cloud utilities reliably 24/7 on affordable Linux VPS hosting via [InterServer VPS]({url}) (#ad).",
        },
    ],
}

CATEGORY_MAPPING: dict[str, dict[str, object]] = {
    "privacy_security": {
        "label": "Privacy, Torrenting & Security",
        "human_tags": ["privacy", "security", "vpn", "password", "torrent", "notes"],
        "merchant_ids": ["MER_047", "MER_119", "MER_096"],
        "injection_message": "Protect your connection and block trackers before downloading or using this app.",
        "cta_label": "Protect your privacy",
        "i18n": {
            "it": {
                "injection_message": "Proteggi la tua connessione e blocca i tracker prima di scaricare o usare questa app.",
                "cta_label": "Proteggi la tua privacy",
            },
            "es": {
                "injection_message": "Protege tu conexión y bloquea rastreadores antes de descargar o usar esta aplicación.",
                "cta_label": "Protege tu privacidad",
            },
            "fr": {
                "injection_message": "Protégez votre connexion et bloquez les traqueurs avant de télécharger ou d'utiliser cette application.",
                "cta_label": "Protégez votre vie privée",
            },
            "de": {
                "injection_message": "Schützen Sie Ihre Verbindung und blockieren Sie Tracker, bevor Sie diese App herunterladen oder nutzen.",
                "cta_label": "Privatsphäre schützen",
            },
        },
    },
    "webapp_cms": {
        "label": "Web Apps, CMS & Cloud Tools",
        "human_tags": ["webapp", "cms", "cloud", "self-hosted", "blog", "automation"],
        "merchant_ids": ["MER_008", "MER_063", "MER_062"],
        "injection_message": "Prefer not to configure a server manually? Launch it in 1 click on a $3/mo Linux Cloud VPS.",
        "cta_label": "Open in Cloud (1-Click)",
        "i18n": {
            "it": {
                "injection_message": "Non vuoi configurare un server a mano? Avvialo in 1 click su un VPS Cloud Linux da 3$/mese.",
                "cta_label": "Apri nel Cloud (1-Click)",
            },
            "es": {
                "injection_message": "¿No quieres configurar un servidor manualmente? Ábrelo en 1 clic en un VPS Cloud Linux desde $3/mes.",
                "cta_label": "Abrir en la Nube (1-Clic)",
            },
            "fr": {
                "injection_message": "Vous ne voulez pas configurer un serveur manuellement ? Lancez-le en 1 clic sur un VPS Cloud Linux dès 3 $/mois.",
                "cta_label": "Ouvrir dans le Cloud (1-Clic)",
            },
            "de": {
                "injection_message": "Sie möchten keinen Server manuell einrichten? Starten Sie die App mit 1 Klick auf einem Linux-Cloud-VPS ab 3 $/Monat.",
                "cta_label": "In der Cloud öffnen (1-Klick)",
            },
        },
    },
    "graphics_video_design": {
        "label": "Graphics, Video & Audio",
        "human_tags": ["graphics", "video", "design", "audio", "editing", "images"],
        "merchant_ids": ["MER_054", "MER_061", "MER_047"],
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
        "merchant_ids": ["MER_008", "MER_063", "MER_062"],
        "injection_message": "Host and publish your website faster on price-locked web hosting and managed WordPress servers.",
        "cta_label": "Explore web hosting deals",
        "i18n": {
            "it": {
                "injection_message": "Ospita e pubblica il tuo sito più velocemente su web hosting a prezzo bloccato e server WordPress gestiti.",
                "cta_label": "Scopri offerte web hosting",
            },
            "es": {
                "injection_message": "Aloja y publica tu sitio web más rápido con web hosting a precio fijo y servidores WordPress gestionados.",
                "cta_label": "Explorar ofertas hosting",
            },
            "fr": {
                "injection_message": "Hébergez et publiez votre site plus vite sur un hébergement à prix bloqué et des serveurs WordPress gérés.",
                "cta_label": "Découvrir offres hébergement",
            },
            "de": {
                "injection_message": "Hosten und veröffentlichen Sie Ihre Website schneller auf preisstabilen Webhosting- und Managed-WordPress-Servern.",
                "cta_label": "Webhosting-Angebote entdecken",
            },
        },
    },
    "productivity_utilities": {
        "label": "Productivity, Backups & Everyday Utilities",
        "human_tags": ["productivity", "backup", "notes", "workflow", "utility", "files"],
        "merchant_ids": ["MER_061", "MER_119", "MER_008"],
        "injection_message": "Automate everyday online workflows free forever and safeguard your devices and backups.",
        "cta_label": "Start free workflow tools",
        "i18n": {
            "it": {
                "injection_message": "Automatizza i flussi di lavoro gratis per sempre e proteggi dispositivi e backup nel cloud.",
                "cta_label": "Inizia gratis ora",
            },
            "es": {
                "injection_message": "Automatiza tus flujos de trabajo gratis para siempre y protege tus dispositivos y copias.",
                "cta_label": "Empezar gratis ahora",
            },
            "fr": {
                "injection_message": "Automatisez vos flux en ligne gratuitement à vie et protégez vos appareils et sauvegardes.",
                "cta_label": "Commencer gratuitement",
            },
            "de": {
                "injection_message": "Automatisieren Sie Ihre Abläufe dauerhaft kostenlos und sichern Sie Geräte sowie Cloud-Backups.",
                "cta_label": "Jetzt kostenlos starten",
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
    if not parsed.path:
        parsed = parsed._replace(path="/")
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
    has_verified_tracking = any(tok in tracking_url for tok in VERIFIED_TRACKING_TOKENS)
    if not has_verified_tracking:
        raise RuntimeError(f"Merchant {mid} ({m['Nome']}) privo di Affiliate ID verificato in tracking_url: {tracking_url}")

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
        cat_merchants = []
        for mid in cat_cfg["merchant_ids"]:  # type: ignore[index]
            base_entry = dict(merchants_index[mid])
            override_url = CATEGORY_URL_OVERRIDES.get((cat_key, mid))
            if override_url:
                base_entry["tracking_url"] = override_url
            cat_merchants.append(base_entry)

        triplet_out = []
        for tdef in TRIPLET_DEFINITIONS[cat_key]:
            mid = tdef["merchant_id"]
            m_entry = merchants_index[mid]
            eff_url = CATEGORY_URL_OVERRIDES.get((cat_key, mid), m_entry["tracking_url"])
            triplet_out.append(
                {
                    "merchant_id": m_entry["merchant_id"],
                    "name": m_entry["name"],
                    "tracking_url": eff_url,
                    "subid": m_entry["subid"],
                    "context_role": tdef["context_role"],
                    "section_hint": tdef["section_hint"],
                    "natural_tip": tdef["tip_template"].format(url=eff_url),
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
