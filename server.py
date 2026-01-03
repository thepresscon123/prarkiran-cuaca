from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from scraper import LiveScoreScraper
import os

app = Flask(__name__, static_folder='.')
CORS(app)

scraper = LiveScoreScraper()

@app.route('/')
def index():
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
        'success': True,
        'win_rate': 87,
        'total_predictions': 1247,
        'vip_members': 152,
        'win_streak': '9/10'
    })

# Untuk Vercel (harus ada variable 'app' di level global)
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
