"""
Flask Server - API untuk menyediakan data live score
"""
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from scraper import LiveScoreScraper
import os

app = Flask(__name__, static_folder='.')
CORS(app)  # Allow cross-origin requests

scraper = LiveScoreScraper()

@app.route('/')
def index():
    """Serve the main website"""
    return send_from_directory('.', 'website_realtime.html')

@app.route('/api/matches')
def get_matches():
    """API endpoint untuk mendapatkan data pertandingan live"""
    try:
        matches = scraper.fetch_live_scores()
        return jsonify({
            'success': True,
            'data': matches,
            'count': len(matches) if matches else 0
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats')
def get_stats():
    """API endpoint untuk statistik bot"""
    return jsonify({
        'win_rate': 87,
        'total_predictions': 1247,
        'vip_members': 152,
        'win_streak': 9
    })

if __name__ == '__main__':
    print("Server running at http://localhost:5000")
    print("API: http://localhost:5000/api/matches")
    app.run(host='0.0.0.0', port=5000, debug=True)
