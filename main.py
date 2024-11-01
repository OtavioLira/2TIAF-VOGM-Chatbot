from flask import Flask, request, jsonify
import function
import requests

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

def buscar_informacao_medicamento(nome_medicamento):
    url = f"https://api.fda.gov/drug/label.json?search={nome_medicamento}&limit=1"
    response = requests.get(url)
    
    if response.status_code == 200:
        dados = response.json()
        if dados['results']:
            # Extrair algumas informações relevantes
            info = dados['results'][0]
            descricao = info.get('description', 'Descrição não disponível.')
            return f"Informações sobre {nome_medicamento}: {descricao}"
        else:
            return "Nenhuma informação encontrada para o medicamento solicitado."
    else:
        return None


@app.route("/dialogflow", methods=["POST"])
def dialogflow():
    data = request.get_json()
    print(f"Recebido JSON: {data}")

    intent = data["intentInfo"]["displayName"]

    if intent == "Default Welcome Intent":
        response = format_response(["""Olá, sou o assistente virtual VOGM, como posso ajudá-lo? atualmente temos as seguintes funcionalidades
        1. buscar o nome da doença por CID (ex: CID A01)
        2. buscar cid pelo nome (ex: colera)
        3. Listar CID (lista 10 cids)     
        4. Info sobre a CIX (citizen experience)
        5. Info sobre a VOGM (Grupo)
        6. Info sobre o projeto VOGM
        7. Informação do medicamento"""])

    elif intent == "buscar.nome.por.cid":
        cid_codigo = data['sessionInfo']['parameters']['cids']
        nome_cid = buscar_nome_por_codigo(cid_codigo)
        if nome_cid:
            response = format_response([f"O nome correspondente ao código CID {cid_codigo} é: {nome_cid}"])
        else:
            response = format_response([f"Código CID {cid_codigo} não encontrado."])

    elif intent == "buscar.cid.por.nome":
        cid_nome = data['sessionInfo']['parameters']['cids']
        codigo_cid = buscar_codigo_por_nome(cid_nome)
        if codigo_cid:
            response = format_response([f"O código CID correspondente ao nome {cid_nome} é: {codigo_cid}"])
        else:
            response = format_response([f"Nome {cid_nome} não encontrado."])

    elif intent == "listar.cid":
        cids = function.carregar_cids()[:10]  # Exibe os 10 primeiros CIDs
        response = format_response([f"Existe uma lista longa com vários códigos CID, aqui estão 10 exemplos: {cids}"])

    elif intent == "info.cix":
        response = format_response([f"""A CIX é uma GovTech, fornecemos soluções inovadoras para o setor público. Explore nossos serviços e esteja com a gente na construção de um futuro ainda mais conectado e transparente para todos.
        Juntos, estamos transformando a maneira como os cidadãos interagem com o governo e impulsionando o progresso em direção a uma sociedade mais eficiente e inclusiva."""])

    elif intent == "info.VOGM":
        response = format_response([f"""Bem-vindo ao VOGM!
        Somos um grupo dedicado a criar soluções inovadoras que transformam o seu dia a dia. Um dos nossos projetos mais destacados é a Leitura Automática de Documentos, uma tecnologia de inteligência artificial que lê e interpreta até mesmo atestados manuscritos de forma autônoma, eliminando a necessidade de trabalho manual.

        Benefícios da nossa solução:    

        Simplificação e Precisão: Nossa tecnologia avançada minimiza erros e torna seus processos mais simples e ágeis.
        Agilidade e Escalabilidade: Nossa solução se adapta a volumes crescentes de atestados, garantindo eficiência e flexibilidade para o seu negócio.
        Explore como podemos ajudar a otimizar suas operações e impulsionar a inovação em sua empresa!
                                    
        Membros do Grupo:
                                    
        Victor Candile Monteiro Barbosa
        Vitor Blankenburg Soares Tavares
        Otávio Lira Neves
        Gustavo Candile Monteiro Barbosa
        Matheus Oliveira de Andrade
        """])
    elif intent == "info.projeto":
        response = format_response(["Claro, para saber mais sobre o projeto aqui está um link da apresentação com um video demonstrativo: https://app.decktopus.com/share/Py632j/1"])
    elif intent == "informacao_medicamento":
            nome_medicamento = data['sessionInfo']['parameters']['medicamento']  # Supondo que você tenha um parâmetro de medicamento
            informacao = buscar_informacao_medicamento(nome_medicamento)
            if informacao:
                response = format_response([informacao])
            else:
                response = format_response([f"Não consegui obter informações sobre o medicamento {nome_medicamento}."])

    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        return response
    else:
        return jsonify(["Erro na requisição"])

if __name__ == "__main__":
    app.run(debug=True)
