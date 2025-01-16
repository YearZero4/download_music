import requests
import os, subprocess
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    titulos = []
    miniaturas = []
    duracion = []
    links = []
    
    if request.method == 'POST':
        if 'query' in request.form:
            query = request.form['query']
            buscar_canciones(query, titulos, links, miniaturas, duracion)
        elif 'link' in request.form:
            return descargar(request.form['link'])

    info = zip(titulos, links, duracion, miniaturas)
    return render_template('index.html', informacion=info)

def buscar_canciones(query, titulos, links, miniaturas, duracion):
    url = f'https://api.deezer.com/search?q={query}'
    response = requests.get(url)
    if response.status_code == 200:
        canciones = response.json().get('data', [])
        for cancion in canciones:
            titulos.append(cancion['title'])
            links.append(cancion['link'])
            miniaturas.append(cancion['album']['cover_medium'])
            minutos = cancion['duration'] // 60
            segundos = cancion['duration'] % 60
            duracion.append(f"{minutos}:{segundos:02d} min")
    else:
        print("Error al buscar canciones")

def descargar(link):
    arl = 'e8e1448dd6353102f5db7d2692fbe1d1510eb9deabb77fa931fdd5f8b00a6d93812fa352e523b7520e905336c680fe7d5f06efa31b936dca89d76faf28e697317cac7f7d3ba4e43a050d6bf5e68af96dbbef093b64f0dc4ffef5119d413af529'
    if not os.path.exists('musicas_descargadas'):
    	os.makedirs('musicas_descargadas')
    command = f'deemix -p musicas_descargadas/ "{link}"'
    subprocess.run(command, shell=True, input=arl.encode())
    return "Descarga en proceso"
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", default=5000))
