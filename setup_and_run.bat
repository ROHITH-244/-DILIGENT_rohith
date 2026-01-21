@echo off
echo Setting up Jarvis AI Assistant...

echo Installing backend dependencies...
cd backend
pip install -r requirements.txt

echo.
echo Installing frontend dependencies...
cd ..\ui
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo To run the application:
echo 1. Start the backend: cd backend ^&^& uvicorn app:app --reload
echo 2. In another terminal, start the frontend: cd ui ^&^& streamlit run chat_ui.py
echo.
echo Then open your browser to http://localhost:8501 to use the chat interface.
pause