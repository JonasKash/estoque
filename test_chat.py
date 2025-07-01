#!/usr/bin/env python3
"""
Script de teste para verificar as funcionalidades de chat e análise
"""

import requests
import json
import time

def test_chat_analysis():
    """Testa as funcionalidades de análise via chat"""
    base_url = "http://localhost:5000"
    
    print("🤖 Testando Funcionalidades de Chat e Análise")
    print("=" * 60)
    
    # Teste 1: Análise de mudanças
    print("\n1. Testando análise de mudanças...")
    try:
        response = requests.post(f"{base_url}/chat/analyze", 
                               json={"query": "mostre as mudanças no estoque"})
        if response.status_code == 200:
            data = response.json()
            print("✅ Análise de mudanças funcionando!")
            print(f"   Tipo: {data.get('type')}")
            print(f"   Resposta: {data.get('response', '')[:100]}...")
        else:
            print(f"❌ Erro na análise de mudanças: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao testar análise de mudanças: {e}")
    
    # Teste 2: Histórico de peça
    print("\n2. Testando histórico de peça...")
    try:
        response = requests.post(f"{base_url}/chat/analyze", 
                               json={"query": "histórico da peça A 0001808909"})
        if response.status_code == 200:
            data = response.json()
            print("✅ Histórico de peça funcionando!")
            print(f"   Tipo: {data.get('type')}")
            print(f"   Resposta: {data.get('response', '')[:100]}...")
        else:
            print(f"❌ Erro no histórico de peça: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao testar histórico de peça: {e}")
    
    # Teste 3: Análise de localizações
    print("\n3. Testando análise de localizações...")
    try:
        response = requests.post(f"{base_url}/chat/analyze", 
                               json={"query": "análise de localizações"})
        if response.status_code == 200:
            data = response.json()
            print("✅ Análise de localizações funcionando!")
            print(f"   Tipo: {data.get('type')}")
            print(f"   Resposta: {data.get('response', '')[:100]}...")
        else:
            print(f"❌ Erro na análise de localizações: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao testar análise de localizações: {e}")
    
    # Teste 4: Insights gerais
    print("\n4. Testando insights gerais...")
    try:
        response = requests.post(f"{base_url}/chat/analyze", 
                               json={"query": "insights gerais do estoque"})
        if response.status_code == 200:
            data = response.json()
            print("✅ Insights gerais funcionando!")
            print(f"   Tipo: {data.get('type')}")
            print(f"   Resposta: {data.get('response', '')[:100]}...")
        else:
            print(f"❌ Erro nos insights gerais: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao testar insights gerais: {e}")
    
    # Teste 5: Endpoints diretos
    print("\n5. Testando endpoints diretos...")
    
    # Teste insights
    try:
        response = requests.get(f"{base_url}/analyze/insights")
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint /analyze/insights funcionando!")
            if data.get('success'):
                insights = data.get('insights', {})
                print(f"   Total de itens: {insights.get('total_items', 0)}")
                print(f"   Peças únicas: {insights.get('unique_pecas', 0)}")
            else:
                print(f"   Erro: {data.get('error')}")
        else:
            print(f"❌ Erro no endpoint insights: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao testar endpoint insights: {e}")
    
    # Teste mudanças
    try:
        response = requests.get(f"{base_url}/analyze/changes")
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint /analyze/changes funcionando!")
            if data.get('success'):
                analysis = data.get('analysis', [])
                print(f"   Análises disponíveis: {len(analysis)}")
            else:
                print(f"   Erro: {data.get('error')}")
        else:
            print(f"❌ Erro no endpoint changes: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao testar endpoint changes: {e}")

def test_chat_queries():
    """Testa diferentes tipos de queries do chat"""
    base_url = "http://localhost:5000"
    
    print("\n🔍 Testando Diferentes Queries do Chat")
    print("=" * 50)
    
    queries = [
        "Qual foi a mudança no estoque?",
        "Histórico da peça A 0001808909",
        "Mostre mudanças de localização",
        "Dê um resumo do estoque",
        "Insights sobre o estoque",
        "Análise de diferenças entre planilhas"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. Testando: '{query}'")
        try:
            response = requests.post(f"{base_url}/chat/analyze", 
                                   json={"query": query})
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Sucesso - Tipo: {data.get('type', 'text')}")
                response_text = data.get('response', '')
                if len(response_text) > 100:
                    print(f"   📝 Resposta: {response_text[:100]}...")
                else:
                    print(f"   📝 Resposta: {response_text}")
            else:
                print(f"   ❌ Erro: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Exceção: {e}")

if __name__ == "__main__":
    print("🧪 Iniciando testes do sistema de chat...")
    print("Certifique-se de que o backend está rodando (python main.py)")
    print()
    
    # Aguardar um pouco para garantir que o servidor está pronto
    time.sleep(2)
    
    test_chat_analysis()
    test_chat_queries()
    
    print("\n" + "=" * 60)
    print("✅ Testes concluídos!")
    print("\nPara testar o chat no frontend:")
    print("1. Execute: npm run dev")
    print("2. Acesse: http://localhost:5173")
    print("3. Clique no balão de chat no canto inferior direito")
    print("4. Teste as funcionalidades de análise!") 