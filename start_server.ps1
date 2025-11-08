# PowerShell script to start Flask server with Gemini API key
$env:GEMINI_API_KEY="AIzaSyAx_kgy_uYyresWInzbHRHB_pQvmu6bEv0"
Write-Host "🚀 Starting Flask server with Gemini API key..." -ForegroundColor Green
Write-Host "📍 Server will be available at http://localhost:5000" -ForegroundColor Cyan
python app.py

