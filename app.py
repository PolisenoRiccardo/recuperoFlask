import io
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, Response
app = Flask(__name__)

scuola = pd.read_csv('POLISENO RICCARDO - ds1880_studenti_scuola_secondaria_2grado_sudd_indirizzo_statale_as_2020_2021.csv', sep=';')


@app.route('/', methods=['GET'])
def home():   
    percorsi = list(set(scuola['PERCORSO']))
    return render_template('home.html', percorsi = percorsi)

@app.route('/datiscuola', methods=['GET'])
def datiscuola():
    scuolaInserita = request.args.get('DenominazioneScuola') 
    table = scuola[scuola['DenominazioneScuola'] == scuolaInserita]
    return render_template('risultato.html', table = table.to_html())

@app.route('/datipercorso', methods=['GET'])
def datipercorso():
    percorsoInserita = request.args.get('percorsi') 
    table = scuola[scuola['PERCORSO'].str.contains(percorsoInserita)][['DenominazioneScuola']].drop_duplicates(subset='DenominazioneScuola').sort_values(by = 'DenominazioneScuola')
    return render_template('risultato.html', table = table.to_html())

@app.route('/grafico', methods=['GET'])
def grafico():
    
    alunniPerIndirizzo = scuola.groupby('PERCORSO').sum()[['ALUNNIMASCHI','ALUNNIFEMMINE']]
    alunniPerIndirizzo['AlunniTotali'] = alunniPerIndirizzo['ALUNNIMASCHI'] + alunniPerIndirizzo['ALUNNIFEMMINE']
    alunniPerIndirizzo = alunniPerIndirizzo.sort_values(by='AlunniTotali', ascending = False)

    labels = alunniPerIndirizzo.index
    dati = alunniPerIndirizzo['AlunniTotali']
    fig, ax = plt.subplots(figsize = (10, 8))
    plt.subplots_adjust(bottom=0.3)
    ax.bar(labels, dati,width = 0.5, color="green")
    plt.xticks(rotation=90)
    ax.set_ylabel('Numero di studenti')
    ax.set_xlabel('Percorsi attivati')
    ax.set_title('Studenti iscritti ai diversi percorsi')

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=32245, debug=True)