@echo off
echo ========================================
echo    Sistema de Consulta de Estoque
echo    com Assistente de IA
echo ========================================
echo.
echo Iniciando o sistema completo...
echo.

echo [1/3] Verificando dependências...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Instale o Python primeiro.
    pause
    exit /b 1
)

node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js não encontrado! Instale o Node.js primeiro.
    pause
    exit /b 1
)

echo ✅ Dependências verificadas!
echo.

echo [2/3] Instalando dependências Python...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Erro ao instalar dependências Python!
    pause
    exit /b 1
)

echo ✅ Dependências Python instaladas!
echo.

echo [3/3] Instalando dependências Node.js...
npm install
if errorlevel 1 (
    echo ❌ Erro ao instalar dependências Node.js!
    pause
    exit /b 1
)

echo ✅ Dependências Node.js instaladas!
echo.

echo ========================================
echo    Sistema Pronto!
echo ========================================
echo.
echo 🚀 Iniciando backend e frontend...
echo.
echo 📋 Instruções:
echo    1. O backend será iniciado em http://localhost:5000
echo    2. O frontend será iniciado em http://localhost:5173
echo    3. Clique no balão de chat para usar o assistente de IA
echo.
echo 💡 Dicas:
echo    - Use "python test_chat.py" para testar o chat
echo    - Use "python test_api.py" para testar a API
echo    - Pressione Ctrl+C para parar os servidores
echo.

echo Iniciando backend em nova janela...
start "Backend - Sistema de Estoque" cmd /k "python main.py"

echo Aguardando backend inicializar...
timeout /t 5 /nobreak >nul

echo Iniciando frontend...
npm run dev

pause 