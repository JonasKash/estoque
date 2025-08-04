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

def extrair_data_do_nome_arquivo(nome_arquivo):
    """Extrai a data do nome do arquivo da planilha"""
    # Padrões para extrair data do nome do arquivo
    padroes = [
        r'(\d{2})(\d{2})(\d{2,4})',  # DDMMYY ou DDMMYYYY
        r'(\d{2})-(\d{2})',  # DD-MM
        r'(\d{2})(\d{2})(\d{2})',  # DDMMYY
    ]
    
    nome_limpo = nome_arquivo.replace('ESTOQUE', '').replace('ARAXÁ', '').replace('ARAXA', '').replace('.xlsx', '').strip()
    
    for padrao in padroes:
        match = re.search(padrao, nome_limpo)
        if match:
            if len(match.groups()) == 3:
                dia, mes, ano = match.groups()
                if len(ano) == 2:
                    ano = '20' + ano
                return datetime(int(ano), int(mes), int(dia))
            elif len(match.groups()) == 2:
                dia, mes = match.groups()
                # Assumindo ano atual se não especificado
                ano_atual = datetime.now().year
                return datetime(ano_atual, int(mes), int(dia))
    
    # Se não conseguir extrair, usar data atual como fallback
    return datetime.now()

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
    """Cria índice para busca rápida de códigos"""
    global indice_codigos, indice_timestamp
    
    print("🔍 Criando índice de códigos...")
    indice_codigos = {}
    
    for arquivo, dados_planilha in dados_cache.items():
        data_arquivo = extrair_data_do_nome_arquivo(arquivo)
        
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
                    'data_arquivo': data_arquivo,
                    'arquivo_origem': arquivo
                })
    
    indice_timestamp = time.time()
    print(f"✅ Índice criado com {len(indice_codigos)} códigos únicos")

def processar_planilhas_inicializacao():
    """Processa todas as planilhas na inicialização do sistema de forma otimizada"""
    global dados_cache, cache_timestamp, dados_carregados
    
    print("🚀 INICIANDO CARREGAMENTO DO SISTEMA...")
    print("📊 Processando planilhas de forma otimizada...")
    
    # Verificar se a pasta de planilhas existe
    if not PLANILHAS_DIR.exists():
        print(f"❌ Pasta de planilhas não encontrada: {PLANILHAS_DIR}")
        return {}
    
    # Listar todas as planilhas disponíveis
    planilhas_disponiveis = list(PLANILHAS_DIR.glob("*.xlsx"))
    
    if not planilhas_disponiveis:
        print(f"❌ Nenhuma planilha encontrada em: {PLANILHAS_DIR}")
        return {}
    
    print(f"📁 Encontradas {len(planilhas_disponiveis)} planilhas...")
    
    dados_cache = {}
    total_itens = 0
    
    for i, arquivo in enumerate(planilhas_disponiveis, 1):
        try:
            print(f"📊 Processando ({i}/{len(planilhas_disponiveis)}): {arquivo.name}")
            
            # Processar planilha de forma otimizada
            dados_planilha = processar_planilha_otimizada(str(arquivo), arquivo.name)
            
            if dados_planilha:
                dados_cache[arquivo.name] = dados_planilha
                total_itens += len(dados_planilha)
                print(f"   ✅ {len(dados_planilha)} itens carregados")
            else:
                print(f"   ⚠️ Nenhum item válido encontrado")
            
        except Exception as e:
            print(f"❌ Erro ao processar {arquivo.name}: {e}")
            continue
    
    print(f"📊 Total de planilhas processadas: {len(dados_cache)}")
    print(f"📦 Total de itens carregados: {total_itens}")
    
    if total_itens == 0:
        print("❌ NENHUM ITEM CARREGADO! Verifique as planilhas.")
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
    """Busca uma peça específica usando índice otimizado"""
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
            # Ordenar por data (mais recente primeiro)
            pecas_ordenadas = sorted(pecas_encontradas, 
                                    key=lambda x: x['data_arquivo'], 
                                    reverse=True)
            
            # Pegar a última ocorrência (mais recente)
            ultima_peca = pecas_ordenadas[0]
            
            # Verificar se há mais de uma ocorrência para rastrear última modificação
            if len(pecas_ordenadas) > 1:
                ultima_modificacao = rastrear_ultima_modificacao(pecas_ordenadas)
            else:
                ultima_modificacao = ultima_peca['data_arquivo'].strftime('%d/%m/%Y')
            
            # Preparar resultado
            resultado = {
                'codigo': ultima_peca['codigo'],
                'nome': ultima_peca['nome'],
                'quantidade': ultima_peca['quantidade'],
                'localizacao': ultima_peca['localizacao'],
                'ultima_alteracao': ultima_modificacao,
                'arquivo_origem': ultima_peca['arquivo_origem']
            }
            
            return resultado
        
    except Exception as e:
        error_msg = f"Erro ao buscar peça: {str(e)}"
        print(f"❌ {error_msg}")
        import traceback
        traceback.print_exc()
        return {"erro": error_msg}

def rastrear_ultima_modificacao(pecas_encontradas):
    """Rastreia a última modificação real da peça comparando todas as ocorrências"""
    try:
        if len(pecas_encontradas) == 1:
            # Se só aparece em uma planilha, é a primeira vez
            data = pecas_encontradas[0]['data_arquivo']
            if data:
                return data.strftime('%d/%m/%Y')
            else:
                return datetime.now().strftime('%d/%m/%Y')
        
        # Ordenar por data (mais antiga primeiro)
        pecas_ordenadas = sorted(pecas_encontradas, key=lambda x: x['data_arquivo'] if x['data_arquivo'] else datetime.min)
        
        # Comparar cada versão com a anterior para detectar mudanças
        ultima_modificacao = pecas_ordenadas[0]['data_arquivo'] or datetime.now()  # Data da primeira aparição
        
        for i in range(1, len(pecas_ordenadas)):
            peca_atual = pecas_ordenadas[i]
            peca_anterior = pecas_ordenadas[i-1]
            
            # Verificar se houve mudança em qualquer campo
            mudanca_detectada = (
                peca_atual['quantidade'] != peca_anterior['quantidade'] or
                peca_atual['localizacao'] != peca_anterior['localizacao'] or
                peca_atual['nome'] != peca_anterior['nome']
            )
            
            if mudanca_detectada:
                ultima_modificacao = peca_atual['data_arquivo'] or datetime.now()
        
        return ultima_modificacao.strftime('%d/%m/%Y')
    except Exception as e:
        print(f"Erro ao rastrear última modificação: {e}")
        return datetime.now().strftime('%d/%m/%Y')

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
    """Endpoint para listar as planilhas disponíveis (apenas para debug)"""
    planilhas = []
    if PLANILHAS_DIR.exists():
        for arquivo in PLANILHAS_DIR.glob("*.xlsx"):
            data_arquivo = extrair_data_do_nome_arquivo(arquivo.name)
            if not data_arquivo:
                data_arquivo = datetime.fromtimestamp(arquivo.stat().st_mtime)
            
            planilhas.append({
                'nome': arquivo.name,
                'data': data_arquivo.strftime('%d/%m/%Y'),
                'tamanho': arquivo.stat().st_size
            })
    
    return jsonify(planilhas)

@app.route('/api/debug/<codigo>')
def debug_codigo(codigo):
    """Endpoint para debug - mostra onde um código específico aparece"""
    try:
        if not dados_carregados:
            processar_planilhas_inicializacao()
        
        codigo_busca = normalizar_codigo(codigo)
        
        if codigo_busca in indice_codigos:
            resultados = []
            for ocorrencia in indice_codigos[codigo_busca]:
                resultados.append({
                    'arquivo': ocorrencia['arquivo_origem'],
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
    """Endpoint para verificar status do cache e índice"""
    return jsonify({
        'dados_carregados': dados_carregados,
        'cache_planilhas': len(dados_cache),
        'indice_codigos': len(indice_codigos),
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

if __name__ == '__main__':
    # Inicializar sistema na startup
    inicializar_sistema()
    app.run(debug=True, host='0.0.0.0', port=5000) 