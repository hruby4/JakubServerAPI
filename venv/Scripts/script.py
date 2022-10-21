from flask import Flask
from flask import request
import datetime


app = Flask(__name__)
date = datetime.datetime.now()
current_time = date.strftime("%H:%M:%S")
zpravy = []

@app.route('/')
def index():
    return 'Vitejte na serveru SPSE Jecna'

@app.route('/zkouska')
def moje_zkouska():
    return 'Možná budou funovat i háčky a čárky.'


@app.route('/datum')
def datum():
    return str(str(date.day) + ". " + str(date.month) + ". " + str(date.year))

@app.route('/datum_iso')
def datum_iso():

    return str(date.strftime('%Y%m%d'))

@app.route('/cas')
def cas():
    return str(current_time)

@app.route('/datum_cas')
def datum_cas():

    return str(str(date.day) + ". " + str(date.month) + ". " + str(date.year) + "  " + str(current_time))


@app.route('/chat', methods=['GET'])
def chat_show():
    return zpravy

@app.route('/chat/<index>', methods=['GET'])
def chat_show_id(index):
    if (int(index) <= len(zpravy) and int(index) > 0):
        return "zprava: " + str(zpravy[int(index)])
    else:
        return str(index) + " index je bud mimo rozsah a nebo je zaporny"


@app.route('/chat/<zprava>', methods=['POST'])
def chat_post(zprava):
    zpravy.append({"id":str(len(zpravy)+1),"message":str(zprava),"type":"post","links":[
        {"href":"/chat/"+str(len(zpravy)+1),"type":"DELETE"},
        {"href":"/chat/"+str(zprava),"type":"PUT"},
        {"href":"/chat","type":"GET"},
        {"href":"/chat/" + str(len(zpravy)+1),"type":"GET"}],})
    return "odeslano: "+zprava

@app.route('/chat/<zprava>', methods=['PUT'])
def chat_put(zprava):
    isinList = False
    for z in zpravy:
        if(zprava == z):
             isinList = True
    if isinList == False:
        zpravy.append({"id": str(len(zpravy) + 1), "message": str(zprava), "type": "post", "links": [
            {"href": "/chat/" + str(len(zpravy) + 1), "type": "DELETE"},
            {"href": "/chat/" + str(zprava), "type": "POST"},
            {"href": "/chat", "type": "GET"},
            {"href": "/chat/" + str(len(zpravy) + 1), "type": "GET"}], })
        return "zprava vlozena"
    else:
        return "zprava jiz existuje"

@app.route('/chat/<index>', methods=['DELETE'])
def chat_delete(index):
    if(int(index) <= len(zpravy) and int(index) >=0):
        zpravy.pop(int(index))
        return "odstraneno " + str(index)
    else:
        return str(index) + " index je bud mimo rozsah a nebo je zaporny"

@app.route('/doc', methods=['GET'])
def doc_show():
    towrite = open("dokumentace.html", "r",encoding="UTF-8")
    return towrite


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
