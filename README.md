# sabrina
an educational website for middle school students

## AI integration

This project includes a simple AI helper (`ai_feedback.py`) that calls a Generative AI service (originally configured for Google's Gemini). To use the real API set the environment variable `GEMINI_API_KEY` with your key.

For local development or testing without an API key, you can enable mock mode which returns canned, deterministic responses:

- Set environment variable `AI_MOCK=1` OR pass the literal api_key `'MOCK'` to the functions in `ai_feedback.py`.

Example (PowerShell):

```powershell
$Env:AI_MOCK = '1'
python test_ai_feedback.py
```

Notes:
- If you want to use a different provider in future, the file checks `AI_PROVIDER` and can be extended.
- Keep your real API keys out of source control. Use environment variables or a secrets manager.
