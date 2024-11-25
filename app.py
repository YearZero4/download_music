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
    arl = 'de306be854e841eba1a47b6ecdab1c9ecae0662b7b52adfe71e657f4a6aa9ab7543e316d385f97ac5ad16565c1687d1271c0564cba153ba939415507782af1f0f513d087e200f93388f13c7d2459938ad15f9c359a3ff897c2bede9769d6ee37'
    if not os.path.exists('musicas_descargadas'):
    	os.makedirs('musicas_descargadas')
    command = f'deemix -p musicas_descargadas/ "{link}"'
    subprocess.run(command, shell=True, input=arl.encode())
    return "Descarga en proceso"
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", default=5000))
