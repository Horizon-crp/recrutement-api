from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
import requests
from os import system, environ
from threading import Thread
import asyncio
data: list = [
  'nom',
  "prenom",
  'age',
  "poste",
  "experience",
  "choose",
  "confiance",
  "pseudo"
]

app = Flask(__name__)
api = Api(app)
CORS(app)
def off():
  asyncio.run(asyncio.sleep(1))
  system("kill 1")

recrutement_arguments = reqparse.RequestParser()
for i in data:
  recrutement_arguments.add_argument(i, type=str, help=f"Nous avons besoin de l'information nommer \"{i}\"", required=True)

class recrutement(Resource):
  def post(self):
    args = recrutement_arguments.parse_args()
    fields = []
    for i in data:
      fields.append({"name": i, "value": args[i]})
    embed = {"fields": fields, 'title': "Candidature"}
    r = requests.post(environ['url'], json={"username": "Candidature", "embeds": [embed]}, headers={"Content-type": "application/json"})
    if r.status_code == 429:
      Thread(target=off).start()
      return {"message": "resend it please."}, 429
    return {"message": "Sent !"}, 200
    
api.add_resource(recrutement, "/recrutement")

@app.route('/')
def home():
  return "<h1>Voici nos page d'api</h1>"

app.run(host='0.0.0.0', port=81)
