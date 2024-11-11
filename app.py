from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

class FluxoDeCaixa:
    def __init__(self):
        self.receitas = []
        self.despesas = []
        self.carregar_dados_iniciais("fluxo_caixa.txt")

    def carregar_dados_iniciais(self, arquivo):
        try:
            with open(arquivo, "r") as f:
                linhas = f.readlines()
                for linha in linhas:
                    tipo, descricao, valor = linha.strip().split(",")
                    valor = float(valor)
                    if tipo == "receita":
                        self.receitas.append({"descricao": descricao, "valor": valor})
                    elif tipo == "despesa":
                        self.despesas.append({"descricao": descricao, "valor": valor})
        except FileNotFoundError:
            print(f"Arquivo {arquivo} não encontrado. Iniciando sem dados pré-carregados.")

    def salvar_dados(self, arquivo):
        with open(arquivo, "w") as f:
            for receita in self.receitas:
                f.write(f"receita,{receita['descricao']},{receita['valor']}\n")
            for despesa in self.despesas:
                f.write(f"despesa,{despesa['descricao']},{despesa['valor']}\n")

    def adicionar_receita(self, descricao, valor):
        self.receitas.append({"descricao": descricao, "valor": valor})
        self.salvar_dados("fluxo_caixa.txt")

    def adicionar_despesa(self, descricao, valor):
        self.despesas.append({"descricao": descricao, "valor": valor})
        self.salvar_dados("fluxo_caixa.txt")

    def calcular_saldo(self):
        total_receitas = sum(receita["valor"] for receita in self.receitas)
        total_despesas = sum(despesa["valor"] for despesa in self.despesas)
        return total_receitas - total_despesas

    def obter_fluxo_de_caixa(self):
        return {
            "receitas": self.receitas,
            "despesas": self.despesas,
            "saldo": self.calcular_saldo()
        }

fluxo_de_caixa = FluxoDeCaixa()

# Endpoint para obter todas as transações e saldo
@app.route('/api/fluxo_caixa', methods=['GET'])
def get_fluxo_caixa():
    return jsonify(fluxo_de_caixa.obter_fluxo_de_caixa())

# Endpoint para adicionar uma receita
@app.route('/api/receita', methods=['POST'])
def add_receita():
    data = request.get_json()
    descricao = data.get("descricao")
    valor = data.get("valor")
    fluxo_de_caixa.adicionar_receita(descricao, valor)
    return jsonify({"message": "Receita adicionada com sucesso"}), 201

# Endpoint para adicionar uma despesa
@app.route('/api/despesa', methods=['POST'])
def add_despesa():
    data = request.get_json()
    descricao = data.get("descricao")
    valor = data.get("valor")
    fluxo_de_caixa.adicionar_despesa(descricao, valor)
    return jsonify({"message": "Despesa adicionada com sucesso"}), 201

if __name__ == '__main__':
    app.run(debug=True)
