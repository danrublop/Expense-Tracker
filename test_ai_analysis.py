#!/usr/bin/env python3
"""
Test script for the AI Analysis module.
This script tests the MistralAnalyzer functionality without requiring the full bot.
"""
import asyncio
import logging
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from bot.ai_analysis import MistralAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def test_ai_analysis():
    """Test the AI analysis functionality."""
    try:
        print("🤖 Testing AI Analysis Module...")
        print("=" * 50)
        
        # Test 1: Initialize analyzer
        print("\n1️⃣ Testing analyzer initialization...")
        try:
            analyzer = MistralAnalyzer()
            print("✅ Analyzer initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize analyzer: {e}")
            print("💡 Make sure Ollama is running: ollama serve")
            return
        
        # Test 2: Monthly analysis
        print("\n2️⃣ Testing monthly analysis...")
        try:
            print("⏳ Running monthly analysis (this may take a few minutes)...")
            result = analyzer.analyze_expenses('monthly')
            print("✅ Monthly analysis completed successfully")
            
            # Format and display results
            report = analyzer.format_analysis_report(result)
            print("\n📊 Monthly Analysis Report:")
            print("-" * 30)
            print(report)
            
        except Exception as e:
            print(f"❌ Monthly analysis failed: {e}")
            return
        
        # Test 3: Annual analysis
        print("\n3️⃣ Testing annual analysis...")
        try:
            print("⏳ Running annual analysis (this may take a few minutes)...")
            result = analyzer.analyze_expenses('annual')
            print("✅ Annual analysis completed successfully")
            
            # Format and display results
            report = analyzer.format_analysis_report(result)
            print("\n📊 Annual Analysis Report:")
            print("-" * 30)
            print(report)
            
        except Exception as e:
            print(f"❌ Annual analysis failed: {e}")
            return
        
        print("\n🎉 All tests completed successfully!")
        print("\n💡 You can now use these commands in your bot:")
        print("   /analyze_monthly - For monthly AI analysis")
        print("   /analyze_annual - For annual AI analysis")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        print(f"❌ Test failed: {e}")

def test_ollama_connection():
    """Test basic Ollama connection."""
    try:
        import ollama
        client = ollama.Client()
        
        # Test connection
        models = client.list()
        print(f"✅ Ollama connection successful")
        print(f"📋 Available models: {[m['name'] for m in models['models']]}")
        
        # Check if Mistral is available
        mistral_available = any('mistral' in m['name'] for m in models['models'])
        if mistral_available:
            print("✅ Mistral model is available")
        else:
            print("⚠️  Mistral model not found. Run: ollama pull mistral")
        
        return True
        
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print("💡 Make sure Ollama is running: ollama serve")
        return False

if __name__ == "__main__":
    print("🧪 AI Analysis Test Suite")
    print("=" * 50)
    
    # Test Ollama connection first
    if not test_ollama_connection():
        print("\n❌ Cannot proceed without Ollama connection")
        sys.exit(1)
    
    # Run the main test
    asyncio.run(test_ai_analysis())
