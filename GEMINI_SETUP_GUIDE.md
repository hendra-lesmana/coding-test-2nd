# Google Gemini API Setup Guide

This guide will help you set up Google Gemini API for the RAG-based Financial Q&A System.

## Why Google Gemini?

✅ **Free Tier**: Generous free quota (15 requests per minute, 1 million tokens per day)
✅ **High Quality**: Excellent performance comparable to GPT-4
✅ **Fast**: Quick response times
✅ **Reliable**: Stable API with good uptime
✅ **Easy Setup**: Simple API key generation

## Step 1: Get Your Google Gemini API Key

### 1.1 Visit Google AI Studio
Go to: https://aistudio.google.com/app/apikey

### 1.2 Sign In
- Sign in with your Google account
- If you don't have one, create a free Google account

### 1.3 Create API Key
1. Click "Create API Key"
2. Select "Create API key in new project" (recommended)
3. Copy the generated API key
4. **Important**: Save this key securely - you won't be able to see it again

### 1.4 Enable Required APIs (if prompted)
- The system will automatically enable the necessary APIs
- This may take a few moments

## Step 2: Configure the System

### 2.1 Add API Key to Environment
Edit `backend\.env` file:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

### 2.2 Install Required Dependencies
```bash
cd backend
venv\Scripts\activate
pip install google-generativeai langchain-google-genai
```

Or use the installation script:
```bash
install_dependencies.bat
```

## Step 3: Start the System

### 3.1 Start Backend
```bash
cd backend
venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Or use:
```bash
start_backend.bat
```

### 3.2 Start Frontend
```bash
cd frontend
npm run dev
```

Or use:
```bash
start_frontend.bat
```

## Step 4: Test the System

1. **Open Browser**: Go to http://localhost:3000
2. **Upload PDF**: Drag and drop your financial statement
3. **Ask Questions**: Use the chat interface
4. **Get AI Responses**: Receive intelligent answers powered by Gemini

## Gemini Models Available

### Gemini 1.5 Flash (Default)
- **Best for**: Fast responses, general Q&A
- **Speed**: Very fast
- **Cost**: Free tier available
- **Use case**: Perfect for this financial Q&A system

### Gemini 1.5 Pro
- **Best for**: Complex analysis, detailed responses
- **Speed**: Moderate
- **Cost**: Higher usage limits
- **Use case**: Advanced financial analysis

To change models, edit `backend\.env`:
```
LLM_MODEL=gemini-1.5-pro
```

## Free Tier Limits

Google Gemini offers generous free limits:
- **Requests**: 15 per minute
- **Tokens**: 1 million per day
- **Rate limit**: 1 request per second

This is more than enough for development and testing!

## Troubleshooting

### "API key not valid"
- Double-check your API key in `backend\.env`
- Ensure there are no extra spaces or characters
- Try generating a new API key

### "Quota exceeded"
- You've hit the free tier limits
- Wait for the quota to reset (daily/monthly)
- Consider upgrading to paid tier if needed

### "Module not found: langchain_google_genai"
```bash
pip install langchain-google-genai google-generativeai
```

### "Authentication error"
- Ensure your Google account has access to AI Studio
- Try signing out and back in to AI Studio
- Check if your API key is still active

## Advantages Over OpenAI

| Feature | Google Gemini | OpenAI |
|---------|---------------|---------|
| Free Tier | Very generous | Limited |
| Setup | Simple | Requires payment setup |
| Performance | Excellent | Excellent |
| Rate Limits | 15/min | 3/min (free) |
| Daily Tokens | 1M free | Limited free |

## Sample Questions to Try

Once set up, try these questions with your financial PDF:

- "What is the total revenue for this year?"
- "How did operating expenses change compared to last year?"
- "What are the main sources of income?"
- "Analyze the cash flow situation"
- "What are the biggest cost categories?"
- "Calculate the profit margin"

## Production Considerations

For production use:
1. **Monitor Usage**: Keep track of API calls
2. **Error Handling**: Implement retry logic
3. **Rate Limiting**: Respect API limits
4. **Caching**: Cache responses when appropriate
5. **Backup**: Consider fallback to local models

## Getting Help

If you encounter issues:
1. Check the [Google AI documentation](https://ai.google.dev/docs)
2. Verify your API key is correct
3. Ensure all dependencies are installed
4. Check the backend logs for error messages

The Google Gemini integration provides excellent AI capabilities with a generous free tier, making it perfect for this financial Q&A system!
