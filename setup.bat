@echo off
echo ========================================
echo Presentation Generator Setup
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo.
    echo Creating .env file from template...
    copy env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and add your API keys!
    echo - For OpenAI: Set OPENAI_API_KEY=your_key_here
    echo - For Ollama: Set LLM_PROVIDER=ollama
    echo.
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the server, run:
echo   python -m src.main
echo.
echo Or use uvicorn directly:
echo   uvicorn src.main:app --reload
echo.
pause

