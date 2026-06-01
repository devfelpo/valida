from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)
CLIENTES = 'dados/clientes.json'
EMPRESAS = 'dados/empresas.json'
HISTORICOS = 'dados/historicos.json'
RELATORIOS = 'dados/relatorios.json'
VALIDACOES = 'dados/validacoes.json'
app.json.sort_keys = False

def proximo_id(lista):
  if not lista:
    return 1
  return max(item.get('id') for item in lista) + 1
def carregar(arquivo):
  with open(arquivo, 'r', encoding='utf-8') as f:
    return json.load(f)
  
def salvar(arquivo, dados):
  with open(arquivo, 'w', encoding='utf-8') as f:
    json.dump(dados, f, indent=4, ensure_ascii=False)

@app.get('/clientes')
def getClientes():
  clientes = carregar(CLIENTES)
  return jsonify(clientes), 200

@app.get('/clientes/<int:id>')
def getClientesById(id):
  clientes = carregar(CLIENTES)
  for cliente in clientes:
    mesmo_id = cliente.get('id') == id
    if mesmo_id:
      return jsonify(cliente),200
  return jsonify({'erro': 'Cliente não encontrado'}), 404

@app.get('/clientes/cpf/<cpf>')
def getClientesByCpf(cpf):
  clientes = carregar(CLIENTES)
  for cliente in clientes:
    mesmo_cpf = cliente.get('cpf') == cpf
    if mesmo_cpf:
      return jsonify(cliente),200
  return jsonify({'erro': 'Cpf não encontrado'}), 404

@app.post('/clientes')
def createClientes():
  clientes = carregar(CLIENTES)
  dados = request.json
  campos = [
    ('nome', str, True),
    ('cpf', str, True),
    ('data_nascimento', str, True),
    ('digital', dict, True)
    ]
  for campo, tipo, obrigatorio in campos:
    valor = dados.get(campo)
    if obrigatorio and(campo not in dados or valor == ''):
      return jsonify({'erro': f'{campo} é obrigatorio'}), 400
    if campo in dados and not isinstance(valor, tipo):
      return jsonify({'erro': f'{campo} apenas recebe {tipo.__name__}'}), 422
  resposta = {
    'id': proximo_id(clientes),
    'nome': dados.get('nome'),
    'cpf': dados.get('cpf'),
    'data_nascimento': dados.get('data_nascimento'),
    'digital': dados.get('digital')
  } 
  clientes.append(resposta)
  salvar(CLIENTES, clientes)
  return jsonify(resposta), 201

@app.put('/clientes/<int:id>')
def updateClientes(id):
  clientes = carregar(CLIENTES)
  dados = request.json
  for cliente in clientes:
    mesmo_id = cliente.get('id') == id
    if mesmo_id:
      cliente.update(dados)
      salvar(CLIENTES, clientes)
      return jsonify({'mensagem': "Atualizado com sucesso"}), 200
  return jsonify({'erro': 'Cliente não encontrado'}), 404

@app.delete('/clientes/<int:id>')
def removeClientes(id):
  clientes = carregar(CLIENTES)
  for cliente in clientes:
    mesmo_id = cliente.get('id') == id
    if mesmo_id:
      clientes.remove(cliente)
      salvar(CLIENTES, clientes)
      return jsonify({'mensagem': 'Cliente deletado com sucesso'}), 204
  return jsonify({'erro': 'Cliente não encontrado'}), 404

@app.get('/empresas')
def getEmpresas():
  empresas = carregar(EMPRESAS)
  return jsonify(empresas),200

@app.get('/empresas/<int:id>')
def getEmpresasById(id):
  empresas = carregar(EMPRESAS)
  for empresa in empresas:
    mesmo_id = empresa.get('id') == id
    if mesmo_id:
      return jsonify(empresa), 200
  return jsonify({'erro': 'Empresa não encontrada'}), 404

@app.post('/empresas')
def createEmpresas():
  empresas = carregar(EMPRESAS)
  dados = request.json
  campos = [
    ('razao_social', str, True),
    ('nome_fantasia', str, True),
    ('cnpj', str, True),
    ('endereco', dict, True),
    ('dados_titular', dict, True)
    ]
  for campo, tipo, obrigatorio in campos:
    valor = dados.get(campo)
    if obrigatorio and (campo not in dados or valor == ''):
      return jsonify({'erro': f'{campo} é obrigatório'}), 422
    if campo in dados and not isinstance(valor, tipo):
      return jsonify({'erro': f'{campo} apenas recebe {tipo.__name__}'}), 422
  resposta = {
    'id': proximo_id(empresas),
    'razao_social': dados.get('razao_social'),
    'nome_fantasia': dados.get('nome_fantasia'),
    'cnpj': dados.get('cnpj'),
    'endereco': dados.get('endereco'),
    'dados_titular': dados.get('dados_titular')
  }
  empresas.append(resposta)
  salvar(EMPRESAS, empresas)
  return jsonify(resposta), 201

@app.put('/empresas/<int:id>')
def updateEmpresas(id):
  empresas = carregar(EMPRESAS)
  dados = request.json
  for empresa in empresas:
    mesmo_id = empresa.get('id') == id
    if mesmo_id:
      empresa.update(dados)
      salvar(EMPRESAS, empresas), 200
      return jsonify({'mensagem': "Atualizado com sucesso"}), 200
  return jsonify({'erro': 'Empresa não encontrada'}), 404

@app.delete('/empresas/<int:id>')
def removeEmpresas(id):
  empresas = carregar(EMPRESAS)
  for empresa in empresas:
    mesmo_id = empresa.get('id') == id
    if mesmo_id:
      empresas.remove(empresa), 204
  return jsonify({'erro': 'Empresa não encontrada'}), 404

@app.get('/historicos')
def getHistoricos():
  historicos = carregar(HISTORICOS)
  return jsonify(historicos),200

@app.get('/historicos/<int:id>')
def getHistoricosById(id):
  historicos = carregar(HISTORICOS)
  for historico in historicos:
    mesmo_id = historico.get('id') == id
    if mesmo_id:
      return jsonify(historico), 200
  return jsonify({'erro': 'Histórico não encontrado'}), 404

@app.get('/historicos/empresa/<int:id_empresa>')
def getHistoricoByEmpresa(id_empresa):
  historicos = carregar(HISTORICOS)

  filtrado = [a for a in historicos if a.get('id_empresa') == id_empresa]
  if not filtrado:
    return jsonify({'erro': 'Nenhum historico encontrado'}),422
  return jsonify(filtrado),200

@app.get('/historicos/cpf/<cpf>')
def getHistoricoByCpf(cpf):
  cpf = str(cpf)
  if not isinstance(cpf, str):
    return jsonify({'erro': f'{cpf} deve ser {str.__name__}'}), 422
  historicos = carregar(HISTORICOS)
  for historico in historicos:
    mesmo_cpf = historico.get('cpf') == cpf
    if mesmo_cpf:
      return jsonify(historico), 200
  return jsonify({'erro': 'Historico não encontrado'}),422

@app.get('/relatorios/empresa/<int:id_empresa>')
def getRelatorioByEmpresa(id_empresa):
  historicos = carregar(HISTORICOS)

  filtrado = [a for a in historicos if a.get('id_empresa') == id_empresa]
  if not filtrado:
    return jsonify({'erro': 'Relatorio não encontrado'}), 404
  
  return jsonify(filtrado), 200

@app.get('/relatorios/empresa/<int:id_empresa>/aprovados')
def getRelatorioByEmpresaWhereAprovados(id_empresa):
  historicos = carregar(HISTORICOS)
  filtrado = [a for a in historicos if a.get('id_empresa') == id_empresa and a.get('resultado') == 'aprovado']
  if not filtrado:
    return jsonify({'erro': 'Nenhum historico encontrado'}),422
  resposta = {
    'id_empresa': id_empresa,
    'tipo_relatorio': 'aprovados',
    'quantidade': len(filtrado),
    'aprovados': filtrado
  }
  return jsonify(resposta), 200

@app.get('/relatorios/empresa/<id_empresa>/reprovados')
def getRelatorioByEmpresaWhereReprovados(id_empresa):
  historicos = carregar(HISTORICOS)
  filtrado = [a for a in historicos if a.get('id_empresa') == id_empresa and a.get('resultado') == 'reprovado']
  if not filtrado:
    return jsonify({'erro': 'Nenhum historico encontrado'}),422
  resposta = {
    'id_empresa': id_empresa,
    'tipo_relatorio': 'reprovado',
    'quantidade': len(filtrado),
    'reprovados': filtrado
  }
  return jsonify(resposta), 200