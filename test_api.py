#!/usr/bin/env python3
"""
Script de teste para verificar se a API está funcionando
"""

import requests
import json
import time

def test_api():
    """Testa os endpoints da API"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testando API do Sistema de Estoque")
    print("=" * 50)
    
    # Teste 1: Endpoint raiz
    print("\n1. Testando endpoint raiz...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Endpoint raiz funcionando!")
            print(f"   Resposta: {response.json()}")
        else:
            print(f"❌ Erro no endpoint raiz: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False
    
    # Teste 2: Health check
    print("\n2. Testando health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check funcionando!")
            print(f"   Status: {data.get('status')}")
            print(f"   Dados carregados: {data.get('data_loaded')}")
            print(f"   Total de arquivos: {data.get('total_files')}")
            print(f"   Total de itens: {data.get('total_items')}")
        else:
            print(f"❌ Erro no health check: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro no health check: {e}")
    
    # Teste 3: Estatísticas
    print("\n3. Testando estatísticas...")
    try:
        response = requests.get(f"{base_url}/stats")
        if response.status_code == 200:
            data = response.json()
            print("✅ Estatísticas funcionando!")
            print(f"   Total de itens: {data.get('total_items')}")
            print(f"   Quantidade total: {data.get('total_quantity')}")
            print(f"   Localizações únicas: {data.get('unique_locations')}")
        else:
            print(f"❌ Erro nas estatísticas: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro nas estatísticas: {e}")
    
    # Teste 4: Busca
    print("\n4. Testando busca...")
    try:
        # Teste com um termo genérico
        search_data = {"query": "filtro"}
        response = requests.post(f"{base_url}/search", json=search_data)
        if response.status_code == 200:
            data = response.json()
            print("✅ Busca funcionando!")
            print(f"   Query: {data.get('query')}")
            print(f"   Total de resultados: {data.get('total')}")
            print(f"   Mensagem: {data.get('message')}")
            
            # Mostrar alguns resultados se houver
            results = data.get('results', [])
            if results:
                print(f"   Primeiro resultado:")
                first_result = results[0]
                print(f"     - Número da peça: {first_result.get('Numero da Peca')}")
                print(f"     - Descrição: {first_result.get('Descricao')}")
                print(f"     - Quantidade: {first_result.get('Quantidade')}")
                print(f"     - Localização: {first_result.get('Localizacao')}")
        else:
            print(f"❌ Erro na busca: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro na busca: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Teste concluído!")
    print("\nPara testar o frontend:")
    print("1. Certifique-se de que o backend está rodando (python main.py)")
    print("2. Em outro terminal, rode: npm run dev")
    print("3. Acesse: http://localhost:5173")

if __name__ == "__main__":
    test_api() 