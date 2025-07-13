# CrewAI Content Creation Agent - API Usage Guide

This guide shows you how to use the deployed CrewAI agent to create high-quality content using a sequence of API calls.

## Prerequisites

1. **Deploy the Agent**:
   ```bash
   # From the storytelling_agent directory
   getmethatdawg deploy ai_content_crew.py --auto-detect
   ```

2. **Set up Environment Variables** (for real AI responses):
   Create a `.env` file in the same directory:
   ```bash
   # Required: At least one API key
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   
   # Optional: Model preferences
   OPENAI_MODEL_NAME=gpt-4o-mini
   ANTHROPIC_MODEL_NAME=claude-3-sonnet-20240229
   GROQ_MODEL_NAME=mixtral-8x7b-32768
   ```

## API Endpoints Overview

Your deployed agent will have these endpoints available:

- **GET /get-crew-info** - Get information about the CrewAI agents
- **GET /get-environment-status** - Check which API keys are available
- **POST /create-content-request** - Create a new content generation request
- **GET /get-content-types** - Get available content types
- **GET /get-content-genres** - Get available content genres
- **POST /generate-content** - Generate content using CrewAI
- **GET /get-agent-capabilities** - Get detailed agent capabilities
- **POST /analyze-content-performance** - Analyze content performance metrics
- **POST /optimize-content-seo** - Optimize content for SEO
- **GET /get-content-templates** - Get available content templates

## Step-by-Step Usage Sequence

### 1. Check System Status

First, verify your deployment and API keys:

```bash
# Check if the service is running
curl https://ai-content-crew.fly.dev/

# Check which API keys are available
curl https://ai-content-crew.fly.dev/get-environment-status
```

### 2. Explore Available Options

```bash
# Get information about the CrewAI agents
curl https://ai-content-crew.fly.dev/get-crew-info

# Get available content types
curl https://ai-content-crew.fly.dev/get-content-types

# Get available content genres
curl https://ai-content-crew.fly.dev/get-content-genres

# Get agent capabilities
curl https://ai-content-crew.fly.dev/get-agent-capabilities
```

### 3. Generate Content (Main Workflow)

This is the primary endpoint that orchestrates all 4 AI agents:

```bash
# Generate a blog post about AI
curl -X POST https://ai-content-crew.fly.dev/generate-content \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "The Future of Artificial Intelligence in Healthcare",
    "content_type": "blog_post",
    "target_audience": "healthcare professionals",
    "tone": "professional",
    "word_count": 1500,
    "keywords": ["AI", "healthcare", "machine learning", "diagnosis", "treatment"]
  }'
```

### 4. Create Content Request (Alternative Approach)

For more control over the process:

```bash
# Create a content request
curl -X POST https://ai-content-crew.fly.dev/create-content-request \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Top 10 Python Libraries for Data Science",
    "content_type": "listicle",
    "target_audience": "data scientists",
    "urgency": "high",
    "special_requirements": "Include code examples and practical use cases"
  }'
```

### 5. SEO Optimization

Optimize existing content for better search engine performance:

```bash
# Optimize content for SEO
curl -X POST https://ai-content-crew.fly.dev/optimize-content-seo \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your existing content here...",
    "target_keywords": ["python", "data science", "machine learning"],
    "target_audience": "developers"
  }'
```

### 6. Performance Analysis

Analyze content performance:

```bash
# Analyze content performance
curl -X POST https://ai-content-crew.fly.dev/analyze-content-performance \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your content here...",
    "metrics": ["readability", "engagement", "seo_score"],
    "target_audience": "general"
  }'
```

## Real-World Example Workflow

Here's a complete example of using the API to create a blog post:

```bash
# 1. Check system status
echo "🔍 Checking system status..."
curl -s https://ai-content-crew.fly.dev/get-environment-status | jq

# 2. Get available content types
echo "📝 Getting content types..."
curl -s https://ai-content-crew.fly.dev/get-content-types | jq

# 3. Generate content with all 4 agents
echo "🤖 Generating content with CrewAI..."
curl -X POST https://ai-content-crew.fly.dev/generate-content \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "10 Best Practices for Python Development",
    "content_type": "blog_post",
    "target_audience": "software developers",
    "tone": "educational",
    "word_count": 1200,
    "keywords": ["python", "best practices", "development", "coding"]
  }' | jq

# 4. Optimize the generated content for SEO
echo "🔍 Optimizing for SEO..."
curl -X POST https://ai-content-crew.fly.dev/optimize-content-seo \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your generated content from step 3...",
    "target_keywords": ["python", "best practices", "development"],
    "target_audience": "developers"
  }' | jq
```

## Response Format

All endpoints return JSON responses with this structure:

```json
{
  "status": "success",
  "message": "Content generated successfully",
  "data": {
    "content": "Generated content here...",
    "metadata": {
      "word_count": 1200,
      "estimated_reading_time": "5 minutes",
      "seo_score": 85
    }
  },
  "agents_used": ["Content Researcher", "Content Writer", "Content Editor", "SEO Specialist"],
  "processing_time": "45 seconds"
}
```

## Error Handling

The API handles errors gracefully:

```json
{
  "status": "error",
  "message": "No API keys available - running in demo mode",
  "data": null,
  "demo_mode": true
}
```

## Performance Notes

- **With API Keys**: Full AI-powered content generation (30-60 seconds per request)
- **Demo Mode**: Instant mock responses with realistic structure
- **Rate Limits**: Respect the underlying AI service rate limits
- **Timeouts**: Requests may timeout after 2 minutes for complex content

## Tips for Best Results

1. **Be Specific**: Provide detailed topic descriptions and requirements
2. **Set Clear Audience**: Define your target audience for better content relevance
3. **Use Keywords**: Include relevant keywords for better SEO optimization
4. **Choose Appropriate Tone**: Select the right tone for your audience
5. **Optimize Length**: Specify word count based on your content goals

## Demo Mode vs Production

- **Demo Mode**: Returns realistic but fake content instantly
- **Production Mode**: Uses real AI models for authentic content generation
- **Hybrid Mode**: Falls back to demo mode if API keys are unavailable

## Troubleshooting

1. **503 Service Unavailable**: The service is starting up (wait 30 seconds)
2. **Timeout Errors**: Content generation is taking too long (try shorter content)
3. **Demo Mode**: Add API keys to your .env file for real AI responses
4. **Rate Limit Errors**: Wait between requests to respect API limits

## Integration Examples

### Python
```python
import requests

response = requests.post(
    'https://ai-content-crew.fly.dev/generate-content',
    json={
        "topic": "Machine Learning Fundamentals",
        "content_type": "tutorial",
        "target_audience": "beginners",
        "word_count": 800
    }
)
content = response.json()
```

### JavaScript
```javascript
const response = await fetch('https://ai-content-crew.fly.dev/generate-content', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        topic: 'React Best Practices',
        content_type: 'guide',
        target_audience: 'developers',
        word_count: 1000
    })
});
const content = await response.json();
```

### cURL with Authentication (if needed)
```bash
curl -X POST https://ai-content-crew.fly.dev/generate-content \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_token_here" \
  -d '{"topic": "Your topic here"}'
```

This guide should help you get started with using the CrewAI Content Creation Agent effectively! 