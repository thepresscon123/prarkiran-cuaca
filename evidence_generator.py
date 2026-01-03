from PIL import Image, ImageDraw, ImageFont
import os
import random

def create_flashscore_image(match_data, filename):
    # Colors
    BG_COLOR = "#0f1519"  # Dark background typical of sports apps
    CARD_COLOR = "#1b242b"
    TEXT_WHITE = "#ffffff"
    TEXT_GRAY = "#8c96a0"
    ACCENT_GREEN = "#00d063" # Flashscore green for live/finished
    RED_COLOR = "#ff4b4b"

    # Dimensions
    W, H = 1080, 400
    img = Image.new('RGB', (W, H), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Fonts (Simulation using default if custom not available, but trying to size them)
    # In a real scenario, we'd load .ttf files. Here we rely on default or simple rendering.
    try:
        font_score = ImageFont.truetype("arial.ttf", 80)
        font_team = ImageFont.truetype("arial.ttf", 50)
        font_status = ImageFont.truetype("arial.ttf", 30)
        font_league = ImageFont.truetype("arial.ttf", 25)
    except:
        font_score = ImageFont.load_default()
        font_team = ImageFont.load_default()
        font_status = ImageFont.load_default()
        font_league = ImageFont.load_default()

    # Draw Match Card Background
    card_margin = 20
    draw.rectangle([card_margin, card_margin, W - card_margin, H - card_margin], fill=CARD_COLOR, outline=None)

    # League Header
    draw.text((50, 40), "PREMIER LEAGUE - ROUND 25", fill=TEXT_GRAY, font=font_league)
    draw.text((W - 200, 40), "Finished", fill=ACCENT_GREEN, font=font_status)

    # Teams and Score
    team_a = match_data['match'].split('vs')[0].strip()
    team_b = match_data['match'].split('vs')[1].strip()
    score = match_data['api_score']
    
    # Center positions
    center_x = W // 2
    
    # Draw Scores (Centered)
    score_w = draw.textlength(score, font=font_score)
    draw.text((center_x - score_w / 2, 130), score, fill=ACCENT_GREEN, font=font_score)

    # Draw Teams
    draw.text((100, 150), team_a, fill=TEXT_WHITE, font=font_team) # Left Team
    
    # Right Team needs right align calc or just simple offset
    team_b_w = draw.textlength(team_b, font=font_team)
    draw.text((W - 100 - team_b_w, 150), team_b, fill=TEXT_WHITE, font=font_team)

    # Half Time score (Mock)
    ht_score = f"({random.randint(0,1)}-{random.randint(0,1)})"
    ht_w = draw.textlength(ht_score, font=font_status)
    draw.text((center_x - ht_w / 2, 220), ht_score, fill=TEXT_GRAY, font=font_status)
    
    # Save
    output_dir = "evidence"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    img.save(os.path.join(output_dir, filename))
    print(f"Generated {filename}")

if __name__ == "__main__":
    # Get the mock data from our predictor logic (duplicated here for simplicity or import)
    matches = [
        {"match": "Man City vs Liverpool", "api_score": "3-1"},
        {"match": "Real Madrid vs Girona", "api_score": "4-0"},
        {"match": "Juventus vs Milan", "api_score": "1-0"},
        {"match": "Bayern vs Dortmund", "api_score": "2-1"},
        {"match": "PSG vs Lyon", "api_score": "3-0"},
        {"match": "Inter vs Roma", "api_score": "1-0"},
        {"match": "Arsenal vs Spurs", "api_score": "2-2"},
        {"match": "Chelsea vs Newcastle", "api_score": "2-1"},
        {"match": "Barca vs Betis", "api_score": "5-0"},
        {"match": "Napoli vs Lazio", "api_score": "2-1"},
    ]
    
    for i, m in enumerate(matches):
        create_flashscore_image(m, f"proof_{i+1}.png")
