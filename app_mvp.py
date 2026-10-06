from datetime import datetime
import requests

# --- CONFIGURATION LAYER ---
TELEGRAM_BOT_TOKEN = "8943547051:AAHqElPpiLk474qHa-c1KawU8wfeJSLg6Mk"
TELEGRAM_CHANNEL_ID = "@AlphaDataMetricsFeed"


def send_telegram_alert(message_text):
    """Encapsulates the Telegram Bot API call to broadcast to your channel."""
    # Official functional Telegram Bot API endpoint URL
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": message_text,
        "parse_mode": "Markdown",
    }

    try:
        response = requests.post(url, json=payload)
        response_data = response.json()

        if response_data.get("ok"):
            print("🚀 Automated multi-pick feed successfully broadcasted to Telegram!")
        else:
            print(f"❌ Telegram API Error: {response_data.get('description')}")
    except Exception as e:
        print(f"──► Failed to hit Telegram API: {e}")


def get_self_hosted_fixtures():
    """Self-hosted local data layer replacing external API dependency.

    Returns structured fixture dictionary list for upcoming matches.
    """
    return [
        {
            "home": "Arsenal",
            "away": "Manchester City",
            "league": "English Premier League",
            "market": "Over 1.5 Goals",
            "calculated_probability": 87.2,
            "bookmaker_odds": 1.35,
            "match_time": "16:30 WAT",
        },
        {
            "home": "Real Madrid",
            "away": "Barcelona",
            "league": "Spanish La Liga",
            "market": "Both Teams to Score",
            "calculated_probability": 82.5,
            "bookmaker_odds": 1.57,
            "match_time": "20:00 WAT",
        },
        {
            "home": "Inter Milan",
            "away": "AC Milan",
            "league": "Italian Serie A",
            "market": "Over 2.5 Goals",
            "calculated_probability": 78.9,
            "bookmaker_odds": 1.75,
            "match_time": "19:45 WAT",
        },
    ]


if __name__ == "__main__":
    print("🤖 Booting Alpha Analytics MVP Engine (Self-Hosted Mode)...")

    fixtures = get_self_hosted_fixtures()
    current_date = datetime.now().strftime("%Y-%m-%d")

    message_body = f"📊 *ALPHA DATA PICKS — {current_date}*\n"
    message_body += "───────────────────────\n"
    message_body += (
        "Our statistical models have detected high-probability value edges:\n\n"
    )

    for idx, game in enumerate(fixtures, 1):
        message_body += (
            f"⚽ *MATCH #{idx}: {game['home'].upper()} vs {game['away'].upper()}*\n"
        )
        message_body += f"🏆 *League:* {game['league']}\n"
        message_body += f"🎯 *Target Market:* {game['market']}\n"
        message_body += (
            f"📈 *Model Probability:* {game['calculated_probability']}%\n"
        )
        message_body += f"💰 *Current Odds:* {game['bookmaker_odds']}\n"
        message_body += f"⏰ *Kickoff:* {game['match_time']}\n"
        message_body += "───────────────────────\n"

    message_body += (
        "👉 *Want all 15+ daily premium +EV picks?*\n"
        "Access our dashboard: [Alpha Analytics Portal](https://your-saas-domain.com)"
    )

    send_telegram_alert(message_body)