import os
import sys
import pandas as pd
import glob
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import unicodedata
import threading
import schedule
import time

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Variável global para armazenar os dados
df = None

def normalize_column(col):
    """Normaliza o nome da coluna para facilitar o mapeamento"""
    if pd.isna(col):
        return ""
    col = str(col).strip().lower()
    col = ''.join(c for c in unicodedata.normalize('NFD', col) if unicodedata.category(c) != 'Mn')
    # Mapeamento direto dos nomes reais da planilha
    if col in ['cod. item', 'cod item', 'codigo item', 'cod_item']:
        return 'numero da peca'
    if col in ['descric?o', 'descrição', 'descricao', 'descri']:
        return 'descricao'
    if col in ['estoque', 'quantidade', 'qtd']:
        return 'quantidade'
    if col in ['locacao', 'locação', 'localizacao', 'localização', 'local']:
        return 'localizacao'
    # Mapeamento flexível
    col = col.replace('numero', 'num').replace('nº', 'num').replace('peca', 'peca').replace('peça', 'peca')
    col = col.replace('descrição', 'descricao').replace('descri', 'descricao')
    col = col.replace('qtd', 'quantidade').replace('quant.', 'quantidade').replace('quant', 'quantidade')
    col = col.replace('localizacao', 'localizacao').replace('localização', 'localizacao')
    return col

def load_spreadsheets():
    """Carrega todas as planilhas Excel da pasta planilhas, aceitando nomes de colunas flexíveis e header na linha 3"""
    global df
    try:
        planilhas_dir = os.path.join(os.path.dirname(__file__), 'planilhas')
        logger.info(f"Procurando planilhas em: {planilhas_dir}")
        
        if not os.path.exists(planilhas_dir):
            logger.error(f"Diretório de planilhas não encontrado: {planilhas_dir}")
            return False
            
        excel_files = glob.glob(os.path.join(planilhas_dir, '*.xlsx'))
        logger.info(f"Arquivos Excel encontrados: {excel_files}")
        
        if not excel_files:
            logger.error("Nenhum arquivo Excel encontrado")
            return False
            
        all_data = []
        for file in excel_files:
            try:
                # Ler a planilha a partir da linha 3 (header=2)
                temp_df = pd.read_excel(file, engine='openpyxl', header=2)
                logger.info(f"Colunas encontradas em {os.path.basename(file)}: {temp_df.columns.tolist()}")
                
                # Normalizar nomes das colunas
                col_map = {}
                for col in temp_df.columns:
                    norm = normalize_column(col)
                    logger.info(f"Coluna original: '{col}' -> Normalizada: '{norm}'")
                    
                    if 'num' in norm and 'peca' in norm:
                        col_map[col] = 'Numero da Peca'
                        logger.info(f"Mapeando '{col}' -> 'Numero da Peca'")
                    elif 'descricao' in norm:
                        col_map[col] = 'Descricao'
                        logger.info(f"Mapeando '{col}' -> 'Descricao'")
                    elif 'quantidade' in norm:
                        col_map[col] = 'Quantidade'
                        logger.info(f"Mapeando '{col}' -> 'Quantidade'")
                    elif 'localizacao' in norm:
                        col_map[col] = 'Localizacao'
                        logger.info(f"Mapeando '{col}' -> 'Localizacao'")
                
                # Renomear colunas
                temp_df = temp_df.rename(columns=col_map)
                logger.info(f"Colunas após mapeamento: {temp_df.columns.tolist()}")
                
                # Verificar se as colunas necessárias existem
                required_columns = ['Numero da Peca', 'Descricao', 'Quantidade', 'Localizacao']
                missing_columns = [col for col in required_columns if col not in temp_df.columns]
                
                if missing_columns:
                    logger.error(f"Colunas faltando em {file}: {missing_columns}")
                    logger.error(f"Colunas disponíveis: {temp_df.columns.tolist()}")
                    continue
                
                # Adicionar nome do arquivo como fonte
                temp_df['Fonte'] = os.path.basename(file)
                
                # Limpar dados
                for col in temp_df.columns:
                    if temp_df[col].dtype == 'object':
                        temp_df[col] = temp_df[col].astype(str).str.strip()
                
                all_data.append(temp_df)
                logger.info(f"Carregado {file}: {len(temp_df)} registros")
                
            except Exception as e:
                logger.error(f"Erro ao ler {file}: {str(e)}")
                # Tentar ler sem engine específico
                try:
                    logger.info(f"Tentando ler {file} sem engine específico...")
                    temp_df = pd.read_excel(file)
                    logger.info(f"Sucesso! Colunas: {temp_df.columns.tolist()}")
                    
                    # Continuar com o processamento normal...
                    col_map = {}
                    for col in temp_df.columns:
                        norm = normalize_column(col)
                        if 'num' in norm and 'peca' in norm:
                            col_map[col] = 'Numero da Peca'
                        elif 'descricao' in norm:
                            col_map[col] = 'Descricao'
                        elif 'quantidade' in norm:
                            col_map[col] = 'Quantidade'
                        elif 'localizacao' in norm:
                            col_map[col] = 'Localizacao'
                    
                    temp_df = temp_df.rename(columns=col_map)
                    required_columns = ['Numero da Peca', 'Descricao', 'Quantidade', 'Localizacao']
                    missing_columns = [col for col in required_columns if col not in temp_df.columns]
                    
                    if missing_columns:
                        logger.error(f"Colunas faltando em {file}: {missing_columns}")
                        continue
                    
                    temp_df['Fonte'] = os.path.basename(file)
                    for col in temp_df.columns:
                        if temp_df[col].dtype == 'object':
                            temp_df[col] = temp_df[col].astype(str).str.strip()
                    
                    all_data.append(temp_df)
                    logger.info(f"Carregado {file}: {len(temp_df)} registros")
                    
                except Exception as e2:
                    logger.error(f"Erro também na segunda tentativa: {str(e2)}")
                    continue
        
        if not all_data:
            logger.error("Nenhum dado foi carregado das planilhas")
            return False
            
        # Combinar todos os DataFrames
        df = pd.concat(all_data, ignore_index=True)
        logger.info(f"Total de registros carregados: {len(df)}")
        logger.info(f"Colunas disponíveis: {df.columns.tolist()}")
        
        # Mostrar alguns exemplos de dados
        logger.info("\nExemplos de dados carregados:")
        for _, row in df.head().iterrows():
            logger.info(f"Peça: {row['Numero da Peca']}, Descrição: {row['Descricao']}")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro ao carregar planilhas: {str(e)}")
        return False

def search_stock(query):
    """Busca no estoque pelo número da peça, descrição ou localização"""
    if df is None or df.empty:
        logger.error("DataFrame vazio ou não inicializado")
        return []
    
    try:
        query = str(query).strip().upper()
        logger.info(f"Buscando por: {query}")
        
        # Buscar em todas as colunas relevantes
        results = []
        
        # Busca por número da peça
        peca_matches = df[df['Numero da Peca'].str.contains(query, case=False, na=False)]
        if not peca_matches.empty:
            results.extend(peca_matches.to_dict('records'))
            logger.info(f"Encontrados {len(peca_matches)} resultados por número da peça")
        
        # Busca por descrição
        desc_matches = df[df['Descricao'].str.contains(query, case=False, na=False)]
        if not desc_matches.empty:
            results.extend(desc_matches.to_dict('records'))
            logger.info(f"Encontrados {len(desc_matches)} resultados por descrição")
        
        # Busca por localização
        loc_matches = df[df['Localizacao'].str.contains(query, case=False, na=False)]
        if not loc_matches.empty:
            results.extend(loc_matches.to_dict('records'))
            logger.info(f"Encontrados {len(loc_matches)} resultados por localização")
        
        # Remover duplicatas
        seen = set()
        unique_results = []
        for result in results:
            key = (result['Numero da Peca'], result['Descricao'], result['Localizacao'])
            if key not in seen:
                seen.add(key)
                unique_results.append(result)
        
        logger.info(f"Total de resultados únicos: {len(unique_results)}")
        return unique_results[:20]  # Limitar a 20 resultados
        
    except Exception as e:
        logger.error(f"Erro durante a busca: {str(e)}")
        return []

@app.route('/stats', methods=['GET'])
def get_stats():
    """Endpoint para obter estatísticas do estoque"""
    try:
        if df is None or df.empty:
            return jsonify({
                'total_items': 0,
                'total_quantity': 0,
                'unique_locations': 0,
                'message': 'Nenhum dado carregado'
            })
        
        # Calcular estatísticas
        total_items = len(df)
        
        # Converter quantidade para numérico, tratando valores não numéricos
        try:
            df['Quantidade_Numeric'] = pd.to_numeric(df['Quantidade'], errors='coerce')
            total_quantity = int(df['Quantidade_Numeric'].sum())
        except:
            total_quantity = 0
        
        unique_locations = len(df['Localizacao'].unique())
        
        stats = {
            'total_items': total_items,
            'total_quantity': total_quantity,
            'unique_locations': unique_locations,
            'message': 'Estatísticas carregadas com sucesso'
        }
        
        logger.info(f"Estatísticas calculadas: {stats}")
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Erro ao calcular estatísticas: {str(e)}")
        return jsonify({
            'error': str(e),
            'total_items': 0,
            'total_quantity': 0,
            'unique_locations': 0,
            'message': 'Erro ao calcular estatísticas'
        }), 500

@app.route('/search', methods=['POST'])
def search():
    """Endpoint de busca"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        logger.info(f"Recebida busca por: {query}")
        
        if not query:
            return jsonify({
                'query': '',
                'results': [],
                'total': 0,
                'message': 'Por favor, digite um termo para buscar'
            })
        
        results = search_stock(query)
        
        response = {
            'query': query,
            'results': results,
            'total': len(results),
            'message': 'Não foi encontrado essa peça nas planilhas.' if len(results) == 0 else f'Encontrados {len(results)} resultados'
        }
        
        logger.info(f"Enviando resposta: {response}")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Erro na busca: {str(e)}")
        return jsonify({
            'error': str(e),
            'query': query if 'query' in locals() else '',
            'results': [],
            'total': 0,
            'message': 'Ocorreu um erro ao realizar a busca'
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de verificação de saúde do sistema"""
    try:
        status = {
            'status': 'ok',
            'data_loaded': df is not None and not df.empty,
            'total_files': len(glob.glob(os.path.join(os.path.dirname(__file__), 'planilhas', '*.xlsx'))),
            'total_items': len(df) if df is not None and not df.empty else 0,
            'columns': df.columns.tolist() if df is not None and not df.empty else []
        }
        return jsonify(status)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/', methods=['GET'])
def index():
    """Endpoint raiz para verificar se o servidor está funcionando"""
    return jsonify({
        'message': 'Sistema de Consulta de Estoque - API funcionando!',
        'endpoints': {
            'health': '/health',
            'stats': '/stats',
            'search': '/search (POST)'
        }
    })

def schedule_reload():
    def job():
        global df
        print('Recarregando planilhas automaticamente às 19:00...')
        load_spreadsheets()
    schedule.every().day.at('19:00').do(job)
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == '__main__':
    # Carregar dados ao iniciar
    if load_spreadsheets():
        logger.info("Sistema iniciado com sucesso!")
        logger.info("Servidor rodando em: http://localhost:5000")
        logger.info("Endpoints disponíveis:")
        logger.info("  - GET  / (informações)")
        logger.info("  - GET  /health (status do sistema)")
        logger.info("  - GET  /stats (estatísticas)")
        logger.info("  - POST /search (busca no estoque)")
    else:
        logger.error("Erro ao carregar dados. Verifique os logs acima.")
    # Iniciar agendamento em thread separada
    t = threading.Thread(target=schedule_reload, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=5000, debug=True)