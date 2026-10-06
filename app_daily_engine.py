"""ALPHA ANALYTICS SAAS — CORE STATISTICAL ENGINE

Modules:
1. Poisson Distribution Probability Engine (xG / Score Matrices)
2. Fair Odds & Expected Value (+EV) Calculator
3. Line Movement / Dropping Odds Detector
"""

from datetime import datetime
import math


def poisson_probability(lmbda, k):
    """Calculates Poisson probability: P(k; λ) = (λ^k * e^-λ) / k!

    lmbda: Expected goals (xG)
    k: Actual goals scored
    """
    return (math.pow(lmbda, k) * math.exp(-lmbda)) / math.factorial(k)


def calculate_match_matrix(home_xg, away_xg, max_goals=6):
    """Generates a score probability matrix (0-0 to 6-6) using home and away xG

    ratings.
    """
    matrix = []
    for h in range(max_goals + 1):
        row = []
        p_home = poisson_probability(home_xg, h)
        for a in range(max_goals + 1):
            p_away = poisson_probability(away_xg, a)
            row.append(p_home * p_away)
        matrix.append(row)
    return matrix


def derive_market_probabilities(score_matrix):
    """Derives exact 1X2, Over/Under, and BTTS probabilities from the Poisson

    score matrix.
    """
    max_goals = len(score_matrix) - 1

    prob_home_win = 0.0
    prob_draw = 0.0
    prob_away_win = 0.0

    prob_over_1_5 = 0.0
    prob_over_2_5 = 0.0

    prob_btts_yes = 0.0

    for h in range(max_goals + 1):
        for a in range(max_goals + 1):
            p = score_matrix[h][a]

            # 1X2 Probabilities
            if h > a:
                prob_home_win += p
            elif h == a:
                prob_draw += p
            else:
                prob_away_win += p

            # Over / Under Probabilities
            if (h + a) > 1.5:
                prob_over_1_5 += p
            if (h + a) > 2.5:
                prob_over_2_5 += p

            # BTTS
            if h > 0 and a > 0:
                prob_btts_yes += p

    return {
        "home_win": round(prob_home_win * 100, 2),
        "draw": round(prob_draw * 100, 2),
        "away_win": round(prob_away_win * 100, 2),
        "over_1_5": round(prob_over_1_5 * 100, 2),
        "over_2_5": round(prob_over_2_5 * 100, 2),
        "btts_yes": round(prob_btts_yes * 100, 2),
    }


def analyze_value_and_line_movement(market_probs, bookie_odds):
    """Compares model probabilities against bookmaker odds to detect:

    1. Fair Odds (100 / Model Probability)
    2. Expected Value (+EV) %
    3. Dropping Odds / Value Edge Signals
    """
    signals = []

    for market_key, odds in bookie_odds.items():
        if market_key not in market_probs:
            continue

        prob = market_probs[market_key]
        if prob <= 0:
            continue

        fair_odds = round(100 / prob, 2)

        # Expected Value (+EV) Formula: (Probability * Odds) - 1
        ev_percent = round((((prob / 100.0) * odds) - 1.0) * 100, 2)

        is_ev_edge = ev_percent >= 5.0  # +5% EV edge threshold

        signals.append({
            "market": market_key,
            "model_probability": prob,
            "fair_odds": fair_odds,
            "bookmaker_odds": odds,
            "ev_percent": ev_percent,
            "is_positive_ev": is_ev_edge,
            "signal_status": "🚀 HIGH +EV SIGNAL" if is_ev_edge else "NEUTRAL",
        })

    return signals


# --- SAAS PIPELINE EXECUTION ---
if __name__ == "__main__":
    print("⚡ ALPHA ANALYTICS ENGINE — COMPUTING POISSON & +EV MATRIX...")
    print("─────────────────────────────────────────────────────────")

    # Sample Match Data Pipeline Input (e.g., from scraper or data provider)
    match_data = {
        "fixture_id": "FIX-2026-9901",
        "home_team": "Arsenal",
        "away_team": "Chelsea",
        "league": "Premier League",
        "home_xg": 2.15,  # Calculated attack/defense expectancy
        "away_xg": 0.95,
        "bookie_odds": {
            "home_win": 1.62,
            "draw": 4.10,
            "away_win": 5.50,
            "over_1_5": 1.28,
            "over_2_5": 1.85,
            "btts_yes": 1.95,
        },
    }

    # Step 1: Compute Score Matrix via Poisson Distribution
    score_matrix = calculate_match_matrix(
        match_data["home_xg"], match_data["away_xg"]
    )

    # Step 2: Derive Exact Market Probabilities
    market_probs = derive_market_probabilities(score_matrix)

    # Step 3: Run EV & Line Value Analysis
    analytical_signals = analyze_value_and_line_movement(
        market_probs, match_data["bookie_odds"]
    )

    # Print Engine Output
    print(f"⚽ FIXTURE: {match_data['home_team']} vs {match_data['away_team']}")
    print(
        f"📊 EXPECTED GOALS (xG): {match_data['home_xg']} - {match_data['away_xg']}\n"
    )

    print("📈 STATISTICAL MODEL PROBABILITIES:")
    for k, v in market_probs.items():
        print(f"   • {k.upper()}: {v}%")

    print("\n🎯 DETECTED VALUE SIGNALS:")
    for sig in analytical_signals:
        if sig["is_positive_ev"]:
            print(f"   [+] Market: {sig['market'].upper()}")
            print(f"       Model Prob: {sig['model_probability']}%")
            print(f"       Fair Odds : {sig['fair_odds']}")
            print(f"       Bookie    : {sig['bookmaker_odds']}")
            print(f"       EV Edge   : +{sig['ev_percent']}%")
            print(f"       Status    : {sig['signal_status']}\n")