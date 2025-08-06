from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from datetime import datetime
import re
from pathlib import Path
import time
import pickle

app = Flask(__name__)

# Configuração da pasta de planilhas
PLANILHAS_DIR = Path(__file__).parent / "planilhas"

# Cache otimizado - carregado na inicialização
dados_cache = {}
cache_timestamp = 0
CACHE_DURATION = 3600  # 1 hora
CACHE_FILE = "cache_dados.pkl"

# Índice para busca rápida - carregado na inicialização
indice_codigos = {}
indice_timestamp = 0

# Flag para indicar se os dados foram carregados
dados_carregados = False



def safe_str(value):
    """Converte valor para string de forma segura"""
    if value is None:
        return ""
    try:
        return str(value).strip()
    except:
        return ""

def is_valid_codigo(codigo):
    """Verifica se o código é válido (não é cabeçalho ou vazio)"""
    if not codigo or codigo == "":
        return False
    
    # Lista de palavras que indicam cabeçalho
    header_words = [
        'código', 'codigo', 'cód', 'cod', 'data', 'geração', 'geracao',
        'item', 'descrição', 'descricao', 'quantidade', 'qtd', 'localização',
        'localizacao', 'local', 'nome', 'peça', 'peca', 'estoque', 'preco'
    ]
    
    codigo_lower = codigo.lower()
    for word in header_words:
        if word in codigo_lower:
            return False
    
    return True

def normalizar_codigo(codigo):
    """Normaliza o código removendo espaços e padronizando formato"""
    if not codigo:
        return ""
    
    # Converter para string e remover espaços
    codigo_limpo = safe_str(codigo).strip()
    
    # Remover todos os espaços do código
    codigo_sem_espacos = codigo_limpo.replace(" ", "").replace("  ", "")
    
    # Converter para maiúsculo
    codigo_normalizado = codigo_sem_espacos.upper()
    
    return codigo_normalizado

def carregar_cache():
    """Carrega cache do arquivo se existir"""
    global dados_cache, cache_timestamp, indice_codigos, indice_timestamp, dados_carregados
    
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'rb') as f:
                cache_data = pickle.load(f)
                dados_cache = cache_data.get('dados', {})
                cache_timestamp = cache_data.get('timestamp', 0)
                indice_codigos = cache_data.get('indice', {})
                indice_timestamp = cache_data.get('indice_timestamp', 0)
                dados_carregados = True
                print("✅ Cache carregado do arquivo - Sistema pronto para uso!")
                return True
    except Exception as e:
        print(f"❌ Erro ao carregar cache: {e}")
    
    return False

def salvar_cache():
    """Salva cache no arquivo"""
    try:
        cache_data = {
            'dados': dados_cache,
            'timestamp': cache_timestamp,
            'indice': indice_codigos,
            'indice_timestamp': indice_timestamp
        }
        with open(CACHE_FILE, 'wb') as f:
            pickle.dump(cache_data, f)
        print("💾 Cache salvo no arquivo")
    except Exception as e:
        print(f"❌ Erro ao salvar cache: {e}")

def processar_planilha_otimizada(caminho_arquivo, nome_arquivo):
    """Processa uma planilha de forma otimizada usando pandas"""
    try:
        print(f"📄 Processando: {nome_arquivo}")
        
        # Ler planilha com pandas (muito mais rápido)
        df = pd.read_excel(caminho_arquivo, header=None, engine='openpyxl')
        
        # Encontrar linha do cabeçalho (procurar nas primeiras 5 linhas)
        linha_cabecalho = 2  # Padrão baseado na análise
        
        # Verificar se a linha 3 tem cabeçalhos válidos
        if linha_cabecalho < len(df):
            headers = df.iloc[linha_cabecalho].astype(str).tolist()
            header_text = ' '.join(headers).lower()
            
            if 'cod' in header_text and ('item' in header_text or 'descric' in header_text):
                linha_cabecalho = 2
            else:
                linha_cabecalho = 3
        
        # Definir colunas baseado na estrutura conhecida
        col_codigo = 0  # Coluna A
        col_nome = 1    # Coluna B  
        col_quantidade = 2  # Coluna C
        col_localizacao = 4  # Coluna E
        
        # Ler dados a partir da linha do cabeçalho + 1
        dados_planilha = []
        
        for idx in range(linha_cabecalho + 1, len(df)):
            try:
                row = df.iloc[idx]
                
                # Extrair valores das colunas
                codigo = safe_str(row.iloc[col_codigo])
                nome = safe_str(row.iloc[col_nome])
                quantidade = safe_str(row.iloc[col_quantidade])
                localizacao = safe_str(row.iloc[col_localizacao])
                
                # Validar código
                if is_valid_codigo(codigo):
                    dados_planilha.append({
                        'codigo': codigo,
                        'nome': nome,
                        'quantidade': quantidade,
                        'localizacao': localizacao
                    })
                    
            except Exception as e:
                # Ignorar erros de linha individual
                continue
        
        print(f"   ✅ {len(dados_planilha)} itens processados")
        return dados_planilha
        
    except Exception as e:
        print(f"❌ Erro ao processar {nome_arquivo}: {e}")
        return []

def criar_indice_codigos():
    """Cria índice para busca rápida de códigos da planilha estoque.xlsx"""
    global indice_codigos, indice_timestamp
    
    print("🔍 Criando índice de códigos...")
    indice_codigos = {}
    
    # Agora só temos uma planilha: estoque.xlsx
    if "estoque.xlsx" in dados_cache:
        dados_planilha = dados_cache["estoque.xlsx"]
        
        for item in dados_planilha:
            codigo = safe_str(item.get('codigo')).strip().upper()
            if codigo and is_valid_codigo(codigo):
                # Normalizar código para o índice
                codigo_normalizado = normalizar_codigo(codigo)
                
                if codigo_normalizado not in indice_codigos:
                    indice_codigos[codigo_normalizado] = []
                
                indice_codigos[codigo_normalizado].append({
                    'codigo': item.get('codigo'),
                    'nome': item.get('nome', ''),
                    'quantidade': item.get('quantidade', ''),
                    'localizacao': item.get('localizacao', ''),
                    'data_arquivo': datetime.now(),  # Data atual já que é uma única planilha
                    'arquivo_origem': 'estoque.xlsx'
                })
    
    indice_timestamp = time.time()
    print(f"✅ Índice criado com {len(indice_codigos)} códigos únicos")

def processar_planilhas_inicializacao():
    """Processa apenas a planilha estoque.xlsx na inicialização do sistema"""
    global dados_cache, cache_timestamp, dados_carregados
    
    print("🚀 INICIANDO CARREGAMENTO DO SISTEMA...")
    print("📊 Processando planilha estoque.xlsx...")
    
    # Verificar se a pasta de planilhas existe
    if not PLANILHAS_DIR.exists():
        print(f"❌ Pasta de planilhas não encontrada: {PLANILHAS_DIR}")
        return {}
    
    # Caminho específico para a planilha estoque.xlsx
    arquivo_estoque = PLANILHAS_DIR / "estoque.xlsx"
    
    if not arquivo_estoque.exists():
        print(f"❌ Planilha estoque.xlsx não encontrada em: {PLANILHAS_DIR}")
        return {}
    
    print(f"📁 Processando planilha: estoque.xlsx")
    
    dados_cache = {}
    total_itens = 0
    
    try:
        print(f"📊 Processando: estoque.xlsx")
        
        # Processar planilha de forma otimizada
        dados_planilha = processar_planilha_otimizada(str(arquivo_estoque), "estoque.xlsx")
        
        if dados_planilha:
            dados_cache["estoque.xlsx"] = dados_planilha
            total_itens += len(dados_planilha)
            print(f"   ✅ {len(dados_planilha)} itens carregados")
        else:
            print(f"   ⚠️ Nenhum item válido encontrado")
        
    except Exception as e:
        print(f"❌ Erro ao processar estoque.xlsx: {e}")
    
    print(f"📊 Total de itens carregados: {total_itens}")
    
    if total_itens == 0:
        print("❌ NENHUM ITEM CARREGADO! Verifique a planilha estoque.xlsx.")
        return {}
    
    # Atualizar cache
    cache_timestamp = time.time()
    dados_carregados = True
    
    # Criar índice para busca rápida
    criar_indice_codigos()
    
    # Salvar cache no arquivo
    salvar_cache()
    
    print("🎉 SISTEMA CARREGADO COM SUCESSO!")
    print("⚡ Todas as buscas agora serão instantâneas!")
    
    return dados_cache

def buscar_peca(codigo_busca, timeout=30):
    """Busca uma peça específica usando índice otimizado da planilha estoque.xlsx"""
    try:
        print(f"🔍 Buscando código: {codigo_busca}")
        
        # Normalizar código de busca (remover espaços)
        codigo_busca_normalizado = normalizar_codigo(codigo_busca)
        print(f"🔍 Código normalizado: '{codigo_busca_normalizado}'")
        
        # Verificar se os dados estão carregados
        if not dados_carregados:
            print("⚠️ Dados não carregados, carregando agora...")
            processar_planilhas_inicializacao()
        
        # Busca direta no índice
        if codigo_busca_normalizado in indice_codigos:
            print(f"✅ ENCONTRADO! {len(indice_codigos[codigo_busca_normalizado])} ocorrências")
            pecas_encontradas = indice_codigos[codigo_busca_normalizado]
        else:
            # Busca parcial se não encontrar exato
            print("🔍 Tentando busca parcial...")
            pecas_encontradas = []
            for codigo, ocorrencias in indice_codigos.items():
                # Normalizar código do índice para comparação
                codigo_indice_normalizado = normalizar_codigo(codigo)
                
                # Buscar por código que contenha a busca ou vice-versa
                if (codigo_busca_normalizado in codigo_indice_normalizado or 
                    codigo_indice_normalizado in codigo_busca_normalizado):
                    pecas_encontradas.extend(ocorrencias)
                    print(f"   ✅ ENCONTRADO (parcial)! Código: '{codigo}' - {len(ocorrencias)} ocorrências")
        
        if not pecas_encontradas:
            return {"erro": f"Peça com código {codigo_busca} não encontrada"}
        else:
            # Como agora temos apenas uma planilha, pegamos a primeira ocorrência
            peca = pecas_encontradas[0]
            
            # Preparar resultado
            resultado = {
                'codigo': peca['codigo'],
                'nome': peca['nome'],
                'quantidade': peca['quantidade'],
                'localizacao': peca['localizacao'],
                'ultima_alteracao': datetime.now().strftime('%d/%m/%Y'),  # Data atual
                'arquivo_origem': 'estoque.xlsx'
            }
            
            return resultado
        
    except Exception as e:
        error_msg = f"Erro ao buscar peça: {str(e)}"
        print(f"❌ {error_msg}")
        import traceback
        traceback.print_exc()
        return {"erro": error_msg}



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    codigo = request.form.get('codigo', '').strip()
    
    if not codigo:
        return jsonify({'erro': 'Por favor, digite um código para buscar'})
    
    resultado = buscar_peca(codigo)
    
    if resultado:
        return jsonify(resultado)
    else:
        return jsonify({'erro': 'Peça não encontrada'})

@app.route('/api/planilhas')
def listar_planilhas():
    """Endpoint para listar a planilha disponível (apenas para debug)"""
    planilhas = []
    arquivo_estoque = PLANILHAS_DIR / "estoque.xlsx"
    
    if arquivo_estoque.exists():
        data_arquivo = datetime.fromtimestamp(arquivo_estoque.stat().st_mtime)
        
        planilhas.append({
            'nome': 'estoque.xlsx',
            'data': data_arquivo.strftime('%d/%m/%Y'),
            'tamanho': arquivo_estoque.stat().st_size
        })
    
    return jsonify(planilhas)

@app.route('/api/debug/<codigo>')
def debug_codigo(codigo):
    """Endpoint para debug - mostra onde um código específico aparece na planilha estoque.xlsx"""
    try:
        if not dados_carregados:
            processar_planilhas_inicializacao()
        
        codigo_busca = normalizar_codigo(codigo)
        
        if codigo_busca in indice_codigos:
            resultados = []
            for ocorrencia in indice_codigos[codigo_busca]:
                resultados.append({
                    'arquivo': 'estoque.xlsx',
                    'data': ocorrencia['data_arquivo'].strftime('%d/%m/%Y'),
                    'encontrados': [{
                        'codigo': ocorrencia['codigo'],
                        'nome': ocorrencia['nome'],
                        'quantidade': ocorrencia['quantidade'],
                        'localizacao': ocorrencia['localizacao']
                    }]
                })
            
            return jsonify({
                'codigo_buscado': codigo_busca,
                'resultados': resultados
            })
        else:
            return jsonify({
                'codigo_buscado': codigo_busca,
                'resultados': []
            })
    except Exception as e:
        return jsonify({'erro': str(e)})

@app.route('/api/status')
def status():
    """Endpoint para verificar status do cache e índice da planilha estoque.xlsx"""
    return jsonify({
        'dados_carregados': dados_carregados,
        'planilha_atual': 'estoque.xlsx',
        'total_itens': len(indice_codigos),
        'cache_timestamp': cache_timestamp,
        'indice_timestamp': indice_timestamp
    })

def inicializar_sistema():
    """Inicializa o sistema carregando todos os dados"""
    print("🚀 INICIANDO SISTEMA DE ESTOQUE...")
    
    # Tentar carregar cache primeiro
    if not carregar_cache():
        print("📊 Cache não encontrado, processando planilhas...")
        processar_planilhas_inicializacao()
    else:
        # Recriar índice se necessário
        if not indice_codigos:
            criar_indice_codigos()
    
    print("✅ Sistema pronto para uso!")

# Inicializa o sistema assim que o Gunicorn importa o arquivo.
# ESTA É A CORREÇÃO CRUCIAL.
inicializar_sistema()

if __name__ == '__main__':
    # Este bloco agora só serve para testes locais, não para o Gunicorn.
    app.run(debug=True, host='0.0.0.0', port=5000)