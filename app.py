from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
DATA_FILE = 'data.json'
DAILY_LIMIT = 400

def load_data():
    today = datetime.now().strftime('%Y-%m-%d')
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            data = json.load(f)
    else:
        data = {'date': '', 'entries': [], 'manual_stars': 0, 'pb': {}}
    
    if data.get('date') != today:
        data = {'date': today, 'entries': [], 'manual_stars': 0, 'pb': data.get('pb', {})}
    return data

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def get_stars(data):
    total = sum(e['amount'] for e in data['entries'])
    stars = 1 if total >= DAILY_LIMIT else max(1, 5 - int(total / DAILY_LIMIT * 4))
    return stars + data.get('manual_stars', 0)

@app.route('/')
def tracker():
    data = load_data()
    total = sum(e['amount'] for e in data['entries'])
    percentage = min(100, int(total / DAILY_LIMIT * 100))
    return render_template('tracker.html', total=total, percentage=percentage, stars=get_stars(data), entries=data['entries'])

@app.route('/games')
def games():
    data = load_data()
    return render_template('games.html', stars=get_stars(data), pbs=data.get('pb', {}))

@app.route('/api/add', methods=['POST'])
def add_caffeine():
    data = load_data()
    data['entries'].append({'amount': request.json['amount'], 'time': datetime.now().strftime('%H:%M')})
    save_data(data)
    return jsonify({'total': sum(e['amount'] for e in data['entries']), 'stars': get_stars(data)})

@app.route('/api/remove', methods=['POST'])
def remove_entry():
    data = load_data()
    idx = request.json['index']
    if 0 <= idx < len(data['entries']):
        data['entries'].pop(idx)
    save_data(data)
    return jsonify({'status': 'ok'})

@app.route('/api/reset', methods=['POST'])
def reset_day():
    data = load_data()
    data['entries'], data['manual_stars'] = [], 0
    save_data(data)
    return jsonify({'status': 'ok'})

@app.route('/api/add_stars', methods=['POST'])
def add_stars():
    data = load_data()
    data['manual_stars'] = data.get('manual_stars', 0) + request.json['amount']
    save_data(data)
    return jsonify({'stars': get_stars(data)})

@app.route('/api/save_pb', methods=['POST'])
def save_pb():
    data = load_data()
    if 'pb' not in data:
        data['pb'] = {}
    game, score = request.json['game'], request.json['score']
    if score > data['pb'].get(game, 0):
        data['pb'][game] = score
        save_data(data)
    return jsonify({'is_new': True})

if __name__ == '__main__':
    app.run(debug=True)