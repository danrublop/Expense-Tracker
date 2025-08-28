# Ollama Setup Guide for AI Analysis

This guide will help you set up Ollama to enable the advanced AI analysis features in your Expense Logging Bot.

## What is Ollama?

Ollama is a local LLM server that allows you to run large language models (like Mistral) on your own machine, ensuring privacy and offline functionality.

## Prerequisites

- macOS, Linux, or Windows (WSL2)
- At least 8GB RAM (16GB recommended)
- 4GB free disk space

## Installation

### macOS
```bash
# Using Homebrew
brew install ollama

# Or download from https://ollama.ai
```

### Linux
```bash
# Download and install
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows
1. Download from https://ollama.ai
2. Install the downloaded executable
3. Or use WSL2 and follow Linux instructions

## Setting up Mistral Model

1. **Start Ollama service:**
   ```bash
   ollama serve
   ```

2. **Pull the Mistral model:**
   ```bash
   ollama pull mistral
   ```

3. **Verify installation:**
   ```bash
   ollama list
   ```

## Testing the Setup

1. **Test basic functionality:**
   ```bash
   ollama run mistral "Hello, how are you?"
   ```

2. **Test with your bot:**
   - Start your expense logging bot
   - Use `/analyze_monthly` or `/analyze_annual` commands
   - The bot should now be able to perform AI analysis

## Troubleshooting

### Common Issues

1. **"Failed to initialize AI analyzer"**
   - Ensure Ollama is running: `ollama serve`
   - Check if Mistral model is available: `ollama list`

2. **"Connection refused"**
   - Ollama service might not be running
   - Restart with: `ollama serve`

3. **"Model not found"**
   - Pull the model: `ollama pull mistral`
   - Wait for download to complete

4. **Out of memory errors**
   - Close other applications
   - Consider using a smaller model: `ollama pull mistral:7b-instruct`

### Performance Tips

1. **Use smaller models for faster responses:**
   ```bash
   ollama pull mistral:7b-instruct
   ```

2. **Adjust model parameters:**
   ```bash
   ollama run mistral --num-ctx 2048 --num-thread 4
   ```

3. **Monitor resource usage:**
   - Use Activity Monitor (macOS) or htop (Linux)
   - Ensure adequate RAM is available

## Advanced Configuration

### Custom Model Configuration

Create a `Modelfile` for custom settings:

```bash
# Create custom model
ollama create custom-mistral -f Modelfile

# Use custom model
ollama run custom-mistral
```

### Environment Variables

You can set these in your `.env` file:

```bash
# Optional: Specify different model
OLLAMA_MODEL=mistral:7b-instruct

# Optional: Set Ollama host (if running on different machine)
OLLAMA_HOST=http://192.168.1.100:11434
```

## Security Considerations

- **Local only**: Ollama runs entirely on your machine
- **No data sent to external servers**: All analysis is done locally
- **Model downloads**: Only the model weights are downloaded once
- **Network access**: Ollama doesn't require internet after initial setup

## Support

If you encounter issues:

1. Check Ollama logs: `ollama logs`
2. Restart Ollama service: `ollama serve`
3. Verify model installation: `ollama list`
4. Check system resources (RAM, disk space)

## Next Steps

Once Ollama is set up:

1. **Test monthly analysis**: `/analyze_monthly`
2. **Test annual analysis**: `/analyze_annual`
3. **Explore patterns**: Look for recurring expenses
4. **Review insights**: Check AI-generated recommendations

The AI analysis will now provide:
- ✅ Automatic expense categorization
- ✅ Pattern recognition (e.g., "matcha 20 times")
- ✅ Spending insights and recommendations
- ✅ Complete privacy (local processing)
- ✅ Flow-based analysis for accuracy
