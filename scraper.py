"""
Live Score Scraper - Mengambil data pertandingan dari sumber publik
"""
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import random

class LiveScoreScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    def fetch_live_scores(self):
        """
        Fetch live scores from public sources.
        Falls back to mock data if scraping fails.
        """
        try:
            # Try to fetch from a public livescore source
            matches = self._scrape_livescore()
            if matches:
                return matches
        except Exception as e:
            print(f"Scraping failed: {e}")
        
        # Fallback to mock data with realistic timestamps
        return self._generate_mock_matches()
    
    def _scrape_livescore(self):
        """
        Attempt to scrape from livescore websites.
        Using sofascore API endpoint (public).
        """
        try:
            # SofaScore has a public API-like endpoint
            today = datetime.now().strftime("%Y-%m-%d")
            url = f"https://api.sofascore.com/api/v1/sport/football/scheduled-events/{today}"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return self._parse_sofascore(data)
        except Exception as e:
            print(f"SofaScore API failed: {e}")
        
        return None
    
    def _parse_sofascore(self, data):
        """Parse SofaScore API response"""
        matches = []
        events = data.get('events', [])[:15]  # Limit to 15 matches
        
        for event in events:
            try:
                home_team = event.get('homeTeam', {}).get('name', 'Unknown')
                away_team = event.get('awayTeam', {}).get('name', 'Unknown')
                home_score = event.get('homeScore', {}).get('current', '-')
                away_score = event.get('awayScore', {}).get('current', '-')
                status = event.get('status', {}).get('description', 'Scheduled')
                start_timestamp = event.get('startTimestamp', 0)
                
                # Convert timestamp to time string
                if start_timestamp:
                    match_time = datetime.fromtimestamp(start_timestamp).strftime("%H:%M")
                else:
                    match_time = "--:--"
                
                # Determine if live
                is_live = status in ['1st half', '2nd half', 'Halftime', 'Live']
                
                # Generate prediction (mock)
                pred_home = random.randint(0, 3)
                pred_away = random.randint(0, 2)
                
                matches.append({
                    'home_team': home_team,
                    'away_team': away_team,
                    'home_score': home_score if home_score != '-' else None,
                    'away_score': away_score if away_score != '-' else None,
                    'time': match_time,
                    'status': status,
                    'is_live': is_live,
                    'prediction': f"{pred_home}-{pred_away}",
                    'hdp': random.choice([-1.75, -1.5, -1.25, -1.0, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75]),
                    'ou': random.choice([1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5])
                })
            except Exception as e:
                continue
        
        return matches if matches else None
    
    def _generate_mock_matches(self):
        """Generate realistic mock match data"""
        now = datetime.now()
        
        matches = [
            {"home_team": "Arsenal", "away_team": "Liverpool", "time": "19:00", "status": "Scheduled", "is_live": False},
            {"home_team": "Real Madrid", "away_team": "Atletico Madrid", "time": "21:30", "status": "Scheduled", "is_live": False},
            {"home_team": "Barcelona", "away_team": "Sevilla", "time": f"{now.hour}:{now.minute:02d}", "status": "2nd half", "is_live": True, "home_score": 2, "away_score": 0},
            {"home_team": "Man City", "away_team": "Chelsea", "time": "00:00", "status": "Scheduled", "is_live": False},
            {"home_team": "Inter Milan", "away_team": "Juventus", "time": "02:45", "status": "Scheduled", "is_live": False},
            {"home_team": "Bayern Munich", "away_team": "Dortmund", "time": "23:30", "status": "Scheduled", "is_live": False},
            {"home_team": "PSG", "away_team": "Lyon", "time": "03:00", "status": "Scheduled", "is_live": False},
            {"home_team": "Napoli", "away_team": "Lazio", "time": "20:00", "status": "1st half", "is_live": True, "home_score": 1, "away_score": 1},
        ]
        
        for match in matches:
            if 'home_score' not in match:
                match['home_score'] = None
                match['away_score'] = None
            
            # Add predictions
            match['prediction'] = f"{random.randint(0,3)}-{random.randint(0,2)}"
            match['hdp'] = random.choice([-1.75, -1.5, -1.25, -1.0, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75])
            match['ou'] = random.choice([1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5])
        
        return matches

if __name__ == "__main__":
    scraper = LiveScoreScraper()
    matches = scraper.fetch_live_scores()
    print(json.dumps(matches, indent=2))
