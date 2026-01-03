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
        """Parse SofaScore API response - FETCHING ALL MATCHES"""
        matches = []
        events = data.get('events', [])  # Fetch ALL available matches for today
        
        # SBOBET format values
        hdp_values = [-2.5, -2.25, -2.0, -1.75, -1.5, -1.25, -1.0, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5]
        ou_values = [1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0, 4.25, 4.5]
        
        for event in events:
            try:
                # Filter useful information
                tournament = event.get('tournament', {}).get('name', 'Unknown League')
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
                    'league': tournament,
                    'home_team': home_team,
                    'away_team': away_team,
                    'home_score': home_score if home_score != '-' else None,
                    'away_score': away_score if away_score != '-' else None,
                    'time': match_time,
                    'status': status,
                    'is_live': is_live,
                    'prediction': f"{pred_home}-{pred_away}",
                    'hdp': random.choice(hdp_values),
                    'ou': random.choice(ou_values),
                    'key_home': round(random.uniform(0.85, 1.05), 2) if random.random() > 0.5 else -round(random.uniform(0.85, 1.05), 2),
                    'key_away': round(random.uniform(0.85, 1.05), 2) if random.random() > 0.5 else -round(random.uniform(0.85, 1.05), 2)
                })
            except Exception as e:
                continue
        
        return matches if matches else None
    
    def _generate_mock_matches(self):
        """Generate realistic mock match data with 20 matches for all sports feel"""
        now = datetime.now()
        
        hdp_values = [-2.5, -2.25, -2.0, -1.75, -1.5, -1.25, -1.0, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5]
        ou_values = [1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0, 4.25, 4.5]
        
        team_pairs = [
            ("Arsenal", "Liverpool"), ("Real Madrid", "Atletico Madrid"), ("Barcelona", "Sevilla"),
            ("Man City", "Chelsea"), ("Inter Milan", "Juventus"), ("Bayern Munich", "Dortmund"),
            ("PSG", "Lyon"), ("Napoli", "Lazio"), ("Leeds United", "Man United"), ("Tottenham", "Sunderland"),
            ("Ajax", "PSV"), ("Porto", "Benfica"), ("Celtic", "Rangers"), ("Fenerbahce", "Galatasaray"),
            ("Boca Juniors", "River Plate"), ("Flamengo", "Palmeiras"), ("Milan", "Roma"), ("Leverkusen", "Leipzig"),
            ("Al Nassr", "Al Hilal"), ("Inter Miami", "LA Galaxy")
        ]
        
        matches = []
        for home, away in team_pairs:
            is_live = random.random() < 0.2
            matches.append({
                "home_team": home,
                "away_team": away,
                "time": f"{random.randint(0,23):02d}:{random.randint(0,5)*10:02d}",
                "status": "Scheduled" if not is_live else "1st half",
                "is_live": is_live,
                "home_score": random.randint(0, 2) if is_live else None,
                "away_score": random.randint(0, 1) if is_live else None,
                "league": random.choice(["Premier League", "La Liga", "Serie A", "Champions League", "International"])
            })
        
        for match in matches:
            # Add predictions and SBOBET odds
            match['prediction'] = f"{random.randint(0,3)}-{random.randint(0,2)}"
            match['hdp'] = random.choice(hdp_values)
            match['ou'] = random.choice(ou_values)
            # Add Key (Odds)
            match['key_home'] = round(random.uniform(0.85, 1.05), 2) if random.random() > 0.5 else -round(random.uniform(0.85, 1.05), 2)
            match['key_away'] = round(random.uniform(0.85, 1.05), 2) if random.random() > 0.5 else -round(random.uniform(0.85, 1.05), 2)
        
        return matches

if __name__ == "__main__":
    scraper = LiveScoreScraper()
    matches = scraper.fetch_live_scores()
    print(json.dumps(matches, indent=2))
