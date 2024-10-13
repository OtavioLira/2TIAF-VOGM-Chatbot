from flask import Flask, request, jsonify
import function

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    return "OK", 200

def format_response(texts: list[str]) -> jsonify:
    return jsonify(
        {
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": texts,                            
                        },
                        "responseType": "HANDLER_PROMPT",
                        "source": "VIRTUAL_AGENT"
                    }
                ]
            }
        }
    )

# Função para buscar o nome pelo código CID
def buscar_nome_por_codigo(cid_codigo):
    cids = function.carregar_cids()
    for cid in cids:
        if cid['codigo'] == cid_codigo:
            return cid['nome']
    return None

# Função para buscar o código CID pelo nome
def buscar_codigo_por_nome(cid_nome):
    cids = function.carregar_cids()
    for cid in cids:
        if cid_nome.lower() in cid['nome'].lower():
            return cid['codigo']
    return None

@app.route("/dialogflow", methods=["POST"])
def dialogflow():
    data = request.get_json()
    print(f"Recebido JSON: {data}")

    intent = data["intentInfo"]["displayName"]

    if intent == "Default Welcome Intent":
        response = format_response(["Olá, sou o assistente virtual VOGM, como posso ajudá-lo?"])

    elif intent == "buscar.cid.por.codigo":
        cid_codigo = data['sessionInfo']['parameters']['lista_cids']
        nome_cid = buscar_nome_por_codigo(cid_codigo)
        if nome_cid:
            response = format_response([f"O nome correspondente ao código CID {cid_codigo} é: {nome_cid}"])
        else:
            response = format_response([f"Código CID {cid_codigo} não encontrado."])

    elif intent == "buscar.cid.por.nome":
        cid_nome = data['sessionInfo']['parameters']['lista_cids']
        codigo_cid = buscar_codigo_por_nome(cid_nome)
        if codigo_cid:
            response = format_response([f"O código CID correspondente ao nome {cid_nome} é: {codigo_cid}"])
        else:
            response = format_response([f"Nome {cid_nome} não encontrado."])

    #elif intent == "listar.cid":
        #lista_cids = function.carregar_cids()[:10]  # Exibe os 10 primeiros CIDs
        #response = format_response([f"Existe uma lista longa com vários códigos CID, aqui estão 10 exemplos: {lista_cids}"])

    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        return response
    else:
        return jsonify(["Erro na requisição"])

if __name__ == "__main__":
    app.run(debug=True)
