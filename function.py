import json
import random

# Carregar os CIDs do arquivo JSON
def carregar_cids() -> json:
    try:
        with open('cid10.json', encoding='utf-8') as f:
            cids = json.load(f)
            # Verifica se o arquivo contém uma lista de CIDs
            if isinstance(cids, list):
                # Retorna 10 exemplos aleatórios da lista de CIDs
                return cids
            else:
                print("Formato de dados inesperado. Esperava-se uma lista.")
                return []
    except FileNotFoundError:
        print("Arquivo de CID não encontrado.")
        return {}