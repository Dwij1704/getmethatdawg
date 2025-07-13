# CrewAI Content Creation Agent - Postman Collection

This directory contains a comprehensive Postman collection for testing the CrewAI Content Creation Agent API.

## Quick Import

1. **Download the collection file**: `CrewAI_Content_Agent_Postman_Collection.json`
2. **Open Postman**
3. **Click "Import"** in the top left
4. **Select "Upload Files"**
5. **Choose the JSON file** and click "Import"

## Collection Overview

The collection includes **10 endpoints** organized by functionality:

### 📊 **System Status**
- **Health Check** - Verify service is running
- **Get Environment Status** - Check API key availability
- **Get Crew Info** - View CrewAI agents and capabilities

### 📝 **Content Creation**
- **Create Content Request** - Main workflow (Research → Write → Edit → SEO)
- **Create Quick Content** - Fast content generation with defaults
- **Create Content** - Alternative endpoint
- **Get Content Status** - Check request status

### 🔍 **Content Analysis**
- **Get Content Types** - Available content formats
- **Get SEO Analysis** - Content optimization analysis
- **Get Writing Tips** - Best practices for content types

## Environment Variables

The collection uses a **baseUrl** variable set to: `https://ai-contentgen-crew.fly.dev`

To change this:
1. Go to **Collection Settings** → **Variables**
2. Update the **baseUrl** value
3. Save the collection

## Sample Requests

### 🚀 **Quick Start: Create Content**
```json
POST /create-content-request
{
  "topic": "The Future of AI in Healthcare",
  "content_type": "blog_post",
  "target_audience": "healthcare professionals", 
  "tone": "professional",
  "word_count": 1200,
  "keywords": ["AI", "healthcare", "machine learning"]
}
```

### 🔍 **Check System Status**
```json
GET /get-environment-status
```

### 📊 **Analyze Content**
```json
POST /get-seo-analysis
{
  "content": "Your content here...",
  "target_keywords": ["python", "programming", "data science"]
}
```

## Built-in Tests

Each request includes automatic tests:
- ✅ **Status Code** - Verifies 200 OK responses
- ✅ **Response Time** - Ensures < 2000ms response times
- ✅ **JSON Format** - Validates response structure
- ✅ **Success Field** - Checks for success indicators

## Response Examples

All requests include sample responses showing:
- Success scenarios with realistic data
- Proper JSON structure
- Expected field names and types
- Error handling examples

## Usage Tips

### 🎯 **Content Creation Workflow**
1. **Check Status** - Verify API keys are available
2. **Get Content Types** - Choose appropriate format
3. **Create Content** - Generate with CrewAI agents
4. **Analyze SEO** - Optimize generated content

### ⚡ **Quick Testing**
- Use **"Send"** button to test individual endpoints
- Use **"Runner"** to test multiple requests in sequence
- Enable **"Auto-follow redirects"** for better testing

### 📋 **Variables & Environments**
- Create **environments** for different deployments
- Use **{{baseUrl}}** for easy URL switching
- Set **request_id** variables for status checking

## Expected Response Times

- **Simple GET requests**: < 500ms
- **Content generation**: 30-60 seconds (real AI processing)
- **SEO analysis**: < 2 seconds
- **Status checks**: < 1 second

## Content Types Supported

- **blog_post** - 800-1200 words
- **article** - 1000-2000 words  
- **social_media** - 50-300 words
- **email** - 300-800 words

## Troubleshooting

### Common Issues:
- **503 Service Unavailable** - Service is starting up (wait 30 seconds)
- **Timeout errors** - Content generation takes time (increase timeout)
- **Demo mode responses** - Add API keys for real AI content

### Debug Steps:
1. Check **Console** for detailed error messages
2. Verify **baseUrl** is correct
3. Ensure **Content-Type** headers are set
4. Test **Health Check** endpoint first

## Integration Examples

### Python
```python
import requests
response = requests.post(
    'https://ai-contentgen-crew.fly.dev/create-content-request',
    json={"topic": "Your topic", "content_type": "blog_post"}
)
```

### cURL
```bash
curl -X POST https://ai-contentgen-crew.fly.dev/create-content-request \
  -H "Content-Type: application/json" \
  -d '{"topic": "Your topic", "content_type": "blog_post"}'
```

## Collection Features

- ✅ **Complete API Coverage** - All 10 endpoints included
- ✅ **Pre-configured Headers** - Content-Type automatically set
- ✅ **Sample Data** - Realistic request examples
- ✅ **Response Examples** - Expected output formats
- ✅ **Automatic Tests** - Built-in validation
- ✅ **Environment Variables** - Easy URL management
- ✅ **Documentation** - Detailed descriptions

## Support

- **API Documentation**: `API_USAGE_GUIDE.md`
- **Environment Setup**: `ENVIRONMENT_SETUP.md`
- **Live Demo**: `demo_api_workflow.sh`
- **Full Test Suite**: `test_api_sequence.sh`

Import this collection and start testing your CrewAI Content Creation Agent in minutes! 🚀 