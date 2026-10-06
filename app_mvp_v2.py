"""ALPHA ANALYTICS SAAS — MVP V2

Includes:
1. Automated Data Layer (2026 Marquee Fixtures)
2. Mathematical Analytics & +EV Filtering Engine
3. Multi-Channel Telegram Growth Broadcaster
"""

from datetime import datetime
import requests

# --- CONFIGURATION LAYER ---
TELEGRAM_BOT_TOKEN = "8943547051:AAHqElPpiLk474qHa-c1KawU8wfeJSLg6Mk"
TELEGRAM_CHANNEL_ID = "@AlphaDataMetricsFeed"
SAAS_DASHBOARD_URL = "https://your-saas-domain.com"

# --- STRICT STATISTICAL THRESHOLDS ---
MIN_MODEL_PROBABILITY = 75.0  # Minimum 75% model confidence
MIN_EV_EDGE_PERCENT = 10.0  # Minimum +10% expected value edge


def fetch_raw_2026_fixtures():
    """Raw Match Data Input Layer.

    In production, this feeds from your scraper or database.
    """
    return [
        {
            "match_id": "M2026-01",
            "home": "Arsenal",
            "away": "Manchester City",
            "league": "English Premier League 2026",
            "market": "Over 1.5 Goals",
            "raw_prob": 88.5,
            "bookmaker_odds": 1.36,
            "kickoff": "16:30 WAT",
        },
        {
            "match_id": "M2026-02",
            "home": "Real Madrid",
            "away": "Barcelona",
            "league": "Spanish La Liga 2026",
            "market": "Both Teams to Score",
            "raw_prob": 82.1,
            "bookmaker_odds": 1.65,
            "kickoff": "20:00 WAT",
        },
        {
            "match_id": "M2026-03",
            "home": "Bayern Munich",
            "away": "Dortmund",
            "league": "German Bundesliga 2026",
            "market": "Home Win",
            "raw_prob": 64.0,  # Below probability threshold (Will be filtered out)
            "bookmaker_odds": 1.80,
            "kickoff": "17:30 WAT",
        },
        {
            "match_id": "M2026-04",
            "home": "Brazil",
            "away": "France",
            "league": "FIFA World Cup 2026",
            "market": "Over 2.5 Goals",
            "raw_prob": 79.4,
            "bookmaker_odds": 1.95,
            "kickoff": "21:00 WAT",
        },
    ]


def run_analytical_engine(fixtures):
    """Core SaaS Engine: Calculates Fair Odds, EV Edge, Risk Tier, and filters

    out bad bets.
    """
    validated_picks = []

    for item in fixtures:
        prob = item["raw_prob"]
        odds = item["bookmaker_odds"]

        # 1. Calculate Fair Odds based on model probability: Fair Odds = 100 / Probability
        fair_odds = round(100 / prob, 2)

        # 2. Calculate Expected Value (EV) Edge %: ((Bookie Odds * Prob) - (100 - Prob)) / 100 * 100
        ev_edge = round(((odds * (prob / 100)) - (1 - (prob / 100))) * 100, 1)

        # 3. Apply Filtering Rules
        if prob >= MIN_MODEL_PROBABILITY and ev_edge >= MIN_EV_EDGE_PERCENT:
            # Assign Risk Tier based on confidence level
            if prob >= 85.0:
                tier = "🔥 HIGH CONVICTION"
            elif ev_edge >= 15.0:
                tier = "🚀 ULTRA VALUE EDGE"
            else:
                tier = "🛡️ STABLE +EV CHOICE"

            validated_picks.append({
                "home": item["home"],
                "away": item["away"],
                "league": item["league"],
                "market": item["market"],
                "prob": prob,
                "bookmaker_odds": odds,
                "fair_odds": fair_odds,
                "ev_edge": ev_edge,
                "tier": tier,
                "kickoff": item["kickoff"],
            })

    return validated_picks


def build_telegram_broadcast_payload(picks):
    """Formats the filtered mathematical picks into Telegram-ready Markdown."""
    today_date = datetime.now().strftime("%B %d, %Y")

    body = f"📊 *ALPHA ANALYTICS 2026 — DAILY VALUE REPORT*\n"
    body += f"📅 *Date:* {today_date}\n"
    body += "───────────────────────────\n\n"
    body += (
        f"🤖 *ALGORITHM STATUS:* {len(picks)} High-Edge Matches Detected\n\n"
    )

    for idx, pick in enumerate(picks, 1):
        body += f"⚽ *MATCH #{idx}: {pick['home'].upper()} vs {pick['away'].upper()}*\n"
        body += f"🏷️ *Tier:* `{pick['tier']}`\n"
        body += f"🏆 *League:* {pick['league']}\n"
        body += f"🎯 *Target Market:* `{pick['market']}`\n"
        body += f"📈 *Model Probability:* {pick['prob']}%\n"
        body += f"💰 *Bookie Odds:* {pick['bookmaker_odds']} | *Fair Odds:* {pick['fair_odds']}\n"
        body += f"🚀 *Mathematical Edge:* `+{pick['ev_edge']}%`\n"
        body += f"⏰ *Kickoff:* {pick['kickoff']}\n"
        body += "───────────────────────────\n"

    body += "\n🔒 *WANT ALL 20+ DAILY +EV SELECTIONS?*\n"
    body += "Stop betting blindly. Automate your discipline.\n\n"
    body += (
        f"👉 [ACCESS FULL SAAS DASHBOARD]({SAAS_DASHBOARD_URL})\n\n"
        "#ValueBetting #SportsAnalytics #WorldCup2026 #BettingTips"
    )

    return body


def broadcast_to_telegram(formatted_text):
    """Publishes the final filtered picks to your Telegram channel."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": formatted_text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
    }

    try:
        response = requests.post(url, json=payload)
        res_data = response.json()

        if res_data.get("ok"):
            print("🚀 [SUCCESS] Filtered analytics feed broadcasted live!")
        else:
            print(f"❌ [API ERROR]: {res_data.get('description')}")
    except Exception as e:
        print(f"💥 [NETWORK ERROR]: {e}")


if __name__ == "__main__":
    print("🤖 Booting Alpha Analytics Engine V2...")

    # Step 1: Fetch Raw Fixtures
    raw_fixtures = fetch_raw_2026_fixtures()
    print(f"📥 Received {len(raw_fixtures)} raw fixtures.")

    # Step 2: Run Analytical Filter
    filtered_picks = run_analytical_engine(raw_fixtures)
    print(
        f"⚡ Filtered down to {len(filtered_picks)} high-conviction +EV"
        " selections."
    )

    # Step 3: Format & Broadcast
    broadcast_content = build_telegram_broadcast_payload(filtered_picks)
    broadcast_to_telegram(broadcast_content)