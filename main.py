from flask import Flask, render_template, request
import requests
import os  

app = Flask(__name__)

API_BASE = os.getenv("API_BASE", "http://localhost:5000")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/pokedex")
def pokedex_page():
    try:  
        response = requests.get(f"{API_BASE}/pokedex", timeout=5)
        response.raise_for_status()
        pokedex = response.json()
    except (requests.exceptions.RequestException, ValueError):
        pokedex = []  
    return render_template('pokedex.html', pokedex=pokedex)

@app.route('/search', methods=['GET'])
def search():
    name = request.args.get('pokemon')
    if not name:
        return render_template('search.html', result=None, not_found=False)
    try:  
        response = requests.get(f'{API_BASE}/strength/{name}', timeout=5)
        if response.status_code == 200:
            result = response.json()
            not_found = False
        else:
            result = None
            not_found = True
    except requests.exceptions.RequestException:
        result = None
        not_found = True
    return render_template('search.html', result=result, not_found=not_found)

@app.route('/compare', methods=['GET'])
def compare():
    poke1 = request.args.get('poke1')
    poke2 = request.args.get('poke2')
    result = None
    if poke1 and poke2:
        try:  
            response = requests.get(f'{API_BASE}/compare/{poke1}/{poke2}', timeout=5)
            if response.status_code == 200:
                result = response.json()
        except requests.exceptions.RequestException:
            result = None
    return render_template('compare.html', result=result, poke1=poke1, poke2=poke2)

@app.route('/legendary')
def legendary():
    try:  
        response = requests.get(f"{API_BASE}/legendary", timeout=5)
        result = response.json()
    except (requests.exceptions.RequestException, ValueError):
        result = []
    return render_template("legendary.html", legendary=result)

@app.route('/leaderboard')
def leaderboard():
    try:
        response = requests.get(f"{API_BASE}/leaderboard/", timeout=5)
        result = response.json()
    except (requests.exceptions.RequestException, ValueError):
        result = []
    return render_template("leaderboard.html", leaderboard=result)

@app.route('/evolution', methods=['GET'])
def evolution():
    name = request.args.get('name')
    chain = None
    not_found = False
    if name:
        try: 
            response = requests.get(f'{API_BASE}/evolution/{name}', timeout=5)
            if response.status_code == 200:
                chain = response.json()
            else:
                not_found = True
        except requests.exceptions.RequestException:
            not_found = True
    return render_template('evolution.html', chain=chain, name=name, not_found=not_found)

@app.route('/weakness', methods=['GET'])
def weakness():
    name = request.args.get('name')
    result = None
    if name:
        try: 
            response = requests.get(f"{API_BASE}/weakness/{name}", timeout=5)
            result = response.json()
        except (requests.exceptions.RequestException, ValueError):
            result = None
    return render_template('weakness.html', result=result, name=name)

@app.route('/pokemon_image/<name>')
def pokemon_image(name):
    try:  
        response = requests.get(f'{API_BASE}/pokemon/{name}/image', timeout=5)
        image_url = response.json().get('image_url') if response.status_code == 200 else None
    except (requests.exceptions.RequestException, ValueError):
        image_url = None
    return render_template('pokemon_image.html', name=name, image_url=image_url)


if __name__ == "__main__":
    app.run(debug=True, port=3000)
