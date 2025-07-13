#!/bin/bash

# CrewAI Content Generation - Complete API Workflow Demo
# This script demonstrates the full capabilities of the deployed CrewAI agent

set -euo pipefail

APP_URL="https://ai-contentgen-crew.fly.dev"

echo "🚀 CrewAI Content Creation Agent - Complete Workflow Demo"
echo "======================================================"
echo "App URL: $APP_URL"
echo ""

# Step 1: Health Check
echo "1. 🩺 Health Check"
curl -s "$APP_URL/" | jq '.status'
echo ""

# Step 2: Environment Status
echo "2. 🔍 Environment Status"
curl -s "$APP_URL/get-environment-status" | jq '.active_llm, .available_services, .status'
echo ""

# Step 3: Crew Information
echo "3. 🤖 CrewAI Agents"
curl -s "$APP_URL/get-crew-info" | jq '.agents[].role'
echo ""

# Step 4: Content Generation (Main Feature)
echo "4. 📝 Generating Content: 'Best Python Libraries for AI'"
echo "   (This will take 30-60 seconds with real AI agents...)"
CONTENT_RESPONSE=$(curl -s -X POST "$APP_URL/create-content-request" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Top 5 Python Libraries for AI and Machine Learning",
    "content_type": "blog_post",
    "target_audience": "Python developers",
    "tone": "professional",
    "word_count": 600,
    "keywords": ["python", "AI", "machine learning", "libraries"]
  }')

echo "   ✅ Content Generated Successfully!"
echo "   📊 Word Count: $(echo "$CONTENT_RESPONSE" | jq '.final_content' | wc -w)"
echo "   🎯 Topic: $(echo "$CONTENT_RESPONSE" | jq -r '.topic')"
echo "   📝 Content Type: $(echo "$CONTENT_RESPONSE" | jq -r '.metadata.content_type')"
echo ""

# Step 5: SEO Analysis
echo "5. 🔍 SEO Analysis"
curl -s -X POST "$APP_URL/get-seo-analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Python offers powerful libraries for AI development including TensorFlow, PyTorch, and scikit-learn for machine learning applications.",
    "target_keywords": ["python", "AI", "machine learning", "libraries"]
  }' | jq '.analysis.seo_score, .recommendations'
echo ""

# Step 6: Available Content Types
echo "6. 📄 Available Content Types"
curl -s "$APP_URL/get-content-types" | jq '.content_types | keys'
echo ""

echo "🎉 Demo Complete!"
echo ""
echo "💡 Key Features Demonstrated:"
echo "   ✅ Multi-agent AI collaboration (4 specialized agents)"
echo "   ✅ Real-time content generation with OpenAI GPT-4o-mini"
echo "   ✅ SEO optimization and analysis"
echo "   ✅ Professional content creation workflow"
echo "   ✅ Production-ready API with 10 endpoints"
echo ""
echo "🔗 Try it yourself:"
echo "   curl -X POST $APP_URL/create-content-request \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"topic\": \"Your topic here\", \"content_type\": \"blog_post\"}'"
echo ""
echo "📚 Full API documentation: API_USAGE_GUIDE.md" 