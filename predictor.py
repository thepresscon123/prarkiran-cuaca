import random

def generate_prediction(query):
    """
    Generates a mock prediction for a given query (e.g., "Arsenal vs Chelsea").
    """
    teams = query.split('vs')
    if len(teams) != 2:
        return None

    team_a = teams[0].strip().title()
    team_b = teams[1].strip().title()

    # Random logic for "prediction"
    score_a = random.randint(0, 4)
    score_b = random.randint(0, 4)
    
    # Ensure a winner if we want to be decisive, or allow draws
    confidence = random.randint(60, 95)
    
    # "Cuaca" elements (Weather/Mood)
    cuacas = ["Cerah Berawan 🌤️", "Badai Gol ⛈️", "Panas Membara 🔥", "Angin Kencang 🌬️", "Hujan Kartu 🌧️"]
    selected_cuaca = random.choice(cuacas)

    # Possession stats
    possession_a = random.randint(30, 70)
    possession_b = 100 - possession_a

    return {
        "team_a": team_a,
        "team_b": team_b,
        "score_a": score_a,
        "score_b": score_b,
        "confidence": confidence,
        "cuaca": selected_cuaca,
        "possession_a": possession_a,
        "possession_b": possession_b,
        "win_prob_a": random.randint(20, 80),
        "total_goals": score_a + score_b
    }

def get_past_results():
    """
    Generates a list of 10 mock 'winning' matches to show as evidence.
    """
    history = [
        {"match": "Man City vs Liverpool", "api_score": "3-1", "tip": "Over 2.5", "status": "WIN ✅"},
        {"match": "Real Madrid vs Girona", "api_score": "4-0", "tip": "Madrid -1.5", "status": "WIN ✅"},
        {"match": "Juventus vs Milan", "api_score": "0-0", "tip": "Under 2.5", "status": "WIN ✅"},
        {"match": "Bayern vs Dortmund", "api_score": "2-1", "tip": "Bayern Win", "status": "WIN ✅"},
        {"match": "PSG vs Lyon", "api_score": "3-0", "tip": "PSG -1.25", "status": "WIN ✅"},
        {"match": "Inter vs Roma", "api_score": "1-0", "tip": "Inter Win", "status": "WIN ✅"},
        {"match": "Arsenal vs Spurs", "api_score": "2-2", "tip": "Over 3", "status": "WIN ✅"},
        {"match": "Chelsea vs Newcastle", "api_score": "1-0", "tip": "Under 3", "status": "WIN ✅"},
        {"match": "Barca vs Betis", "api_score": "5-0", "tip": "Barca -1", "status": "WIN ✅"},
        {"match": "Napoli vs Lazio", "api_score": "2-1", "tip": "Napoli Win", "status": "WIN ✅"},
    ]
    return history
