import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    #Lê os valores dos formulários
    original_text = request.form['text']
    target_language = request.form['language']

    #Lê as variáveis do .env
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']
    
    #Indica que queremos traduzir e a versão da API (3.0) e o idioma de destino
    path = '/translate?api-version=3.0'
    #Adicionando o parâmetro de idioma de destino
    target_language_parameter = '&to=' + target_language
    #Criando a URL completa
    constructed_url = endpoint + path + target_language_parameter

    #Configuração das informações do cabeçalho, que incluem a chave de assinatura
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    #Criando o corpo da solicitação do texto a ser traduzido
    body = [{ 'text':original_text }]

    #Realizando a chamada de post incluindo o texto a ser traduzido
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    #Recuperando a resposta json que inclui o texto traduzido
    translator_response = translator_request.json()
    #Recuperando o texto traduzido
    translated_text = translator_response[0]['translations'][0]['text']

    #Chamando o index com o texto traduzido
    #texto original, e o texto traduzido
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )