Write-Output "Setting up Jarvis AI Assistant..."

# Install backend dependencies
Write-Output "Installing backend dependencies..."
Set-Location backend
pip install -r requirements.txt

# Install frontend dependencies
Write-Output "Installing frontend dependencies..."
Set-Location ../ui
pip install -r requirements.txt

Write-Output "Setup complete!"
Write-Output ""
Write-Output "To run the application:"
Write-Output "1. Start the backend: cd backend; uvicorn app:app --reload"
Write-Output "2. In another terminal, start the frontend: cd ui; streamlit run chat_ui.py"
Write-Output ""
Write-Output "Then open your browser to http://localhost:8501 to use the chat interface."