#!/bin/bash

# CrewAI Content Creation Agent - API Sequence Test Script
# This script demonstrates the full workflow of the CrewAI agent

set -euo pipefail

# Configuration
APP_URL="https://ai-content-crew.fly.dev"
TIMEOUT=120
OUTPUT_DIR="./api_test_output"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✅${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}❌${NC} $1"
}

log_step() {
    echo -e "${PURPLE}🔄${NC} $1"
}

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Function to make API calls with error handling
make_api_call() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    local description="$4"
    local output_file="$5"
    
    log_step "$description"
    
    local cmd="curl -s -w '\n%{http_code}' --max-time $TIMEOUT -X $method '$APP_URL$endpoint'"
    
    if [[ -n "$data" ]]; then
        cmd="$cmd -H 'Content-Type: application/json' -d '$data'"
    fi
    
    # Execute the curl command and capture response
    local response=$(eval "$cmd")
    local http_code=$(echo "$response" | tail -n1)
    local json_response=$(echo "$response" | head -n -1)
    
    # Save response to file
    echo "$json_response" > "$OUTPUT_DIR/$output_file"
    
    # Check HTTP status
    if [[ "$http_code" -eq 200 ]]; then
        log_success "Success (HTTP $http_code)"
        # Pretty print JSON if jq is available
        if command -v jq &> /dev/null; then
            echo "$json_response" | jq '.' > "$OUTPUT_DIR/$output_file.pretty"
        fi
    else
        log_warning "HTTP $http_code - Check $OUTPUT_DIR/$output_file for details"
    fi
    
    return $http_code
}

# Function to extract content from response
extract_content() {
    local file="$1"
    local key="$2"
    
    if command -v jq &> /dev/null; then
        jq -r "$key" "$OUTPUT_DIR/$file" 2>/dev/null || echo "Could not extract $key"
    else
        echo "Install jq for better JSON parsing"
    fi
}

# Main test sequence
main() {
    echo -e "${BLUE}🚀 CrewAI Content Creation Agent - API Sequence Test${NC}"
    echo "================================================="
    echo "Target URL: $APP_URL"
    echo "Output Directory: $OUTPUT_DIR"
    echo "Timeout: ${TIMEOUT}s"
    echo ""
    
    # Step 1: Health Check
    log_step "Step 1: Health Check"
    if make_api_call "GET" "/" "" "Checking if service is running" "01_health_check.json"; then
        log_success "Service is running"
    else
        log_error "Service is not accessible"
        exit 1
    fi
    echo ""
    
    # Step 2: Environment Status
    log_step "Step 2: Environment Status"
    make_api_call "GET" "/get-environment-status" "" "Checking API key availability" "02_env_status.json"
    
    # Check if running in demo mode
    if command -v jq &> /dev/null; then
        demo_mode=$(jq -r '.demo_mode // false' "$OUTPUT_DIR/02_env_status.json")
        if [[ "$demo_mode" == "true" ]]; then
            log_warning "Running in demo mode - responses will be mocked"
        else
            log_success "Production mode - real AI responses enabled"
        fi
    fi
    echo ""
    
    # Step 3: Get System Information
    log_step "Step 3: System Information"
    make_api_call "GET" "/get-crew-info" "" "Getting CrewAI agents info" "03_crew_info.json"
    make_api_call "GET" "/get-content-types" "" "Getting available content types" "04_content_types.json"
    make_api_call "GET" "/get-content-genres" "" "Getting available content genres" "05_content_genres.json"
    make_api_call "GET" "/get-agent-capabilities" "" "Getting agent capabilities" "06_agent_capabilities.json"
    echo ""
    
    # Step 4: Generate Content (Main Workflow)
    log_step "Step 4: Content Generation (Main Workflow)"
    local content_request='{
        "topic": "10 Essential Python Libraries for Data Science in 2024",
        "content_type": "blog_post",
        "target_audience": "data scientists and Python developers",
        "tone": "professional and informative",
        "word_count": 1200,
        "keywords": ["python", "data science", "libraries", "pandas", "numpy", "matplotlib", "machine learning"]
    }'
    
    make_api_call "POST" "/generate-content" "$content_request" "Generating content with all 4 agents" "07_generated_content.json"
    
    # Extract and display the generated content
    if [[ -f "$OUTPUT_DIR/07_generated_content.json" ]]; then
        log_info "Generated content preview:"
        content_preview=$(extract_content "07_generated_content.json" '.data.content // .content' | head -c 200)
        echo -e "${YELLOW}$content_preview...${NC}"
    fi
    echo ""
    
    # Step 5: SEO Optimization
    log_step "Step 5: SEO Optimization"
    local seo_request='{
        "content": "Python has become the go-to language for data science due to its simplicity and powerful libraries. In this comprehensive guide, we will explore the essential Python libraries that every data scientist should know in 2024.",
        "target_keywords": ["python", "data science", "libraries", "2024"],
        "target_audience": "data scientists"
    }'
    
    make_api_call "POST" "/optimize-content-seo" "$seo_request" "Optimizing content for SEO" "08_seo_optimization.json"
    echo ""
    
    # Step 6: Performance Analysis
    log_step "Step 6: Performance Analysis"
    local analysis_request='{
        "content": "Data science is rapidly evolving, and staying updated with the latest Python libraries is crucial for success. This article covers the most important libraries you need to know.",
        "metrics": ["readability", "engagement", "seo_score", "technical_depth"],
        "target_audience": "data scientists"
    }'
    
    make_api_call "POST" "/analyze-content-performance" "$analysis_request" "Analyzing content performance" "09_performance_analysis.json"
    echo ""
    
    # Step 7: Alternative Content Request
    log_step "Step 7: Alternative Content Request"
    local alt_request='{
        "title": "Machine Learning Algorithms Explained Simply",
        "content_type": "tutorial",
        "target_audience": "beginners",
        "urgency": "medium",
        "special_requirements": "Include practical examples and avoid complex mathematical formulas"
    }'
    
    make_api_call "POST" "/create-content-request" "$alt_request" "Creating alternative content request" "10_alt_content_request.json"
    echo ""
    
    # Step 8: Get Content Templates
    log_step "Step 8: Content Templates"
    make_api_call "GET" "/get-content-templates" "" "Getting available content templates" "11_content_templates.json"
    echo ""
    
    # Summary
    echo -e "${GREEN}🎉 Test Sequence Complete!${NC}"
    echo "================================="
    echo "📁 All responses saved to: $OUTPUT_DIR"
    echo ""
    echo "📊 Results Summary:"
    
    # Count successful responses
    success_count=0
    total_count=$(ls "$OUTPUT_DIR"/*.json | wc -l)
    
    for file in "$OUTPUT_DIR"/*.json; do
        if [[ -f "$file" ]]; then
            if command -v jq &> /dev/null; then
                status=$(jq -r '.status // "unknown"' "$file" 2>/dev/null)
                if [[ "$status" == "success" ]]; then
                    ((success_count++))
                fi
            fi
        fi
    done
    
    echo "   ✅ Successful responses: $success_count/$total_count"
    echo ""
    
    # Show useful commands
    echo "💡 Useful Commands:"
    echo "   View all responses: ls -la $OUTPUT_DIR"
    echo "   Pretty print JSON: cat $OUTPUT_DIR/07_generated_content.json | jq ."
    echo "   View content: cat $OUTPUT_DIR/07_generated_content.json | jq -r '.data.content // .content'"
    echo ""
    
    # Show next steps
    echo "🚀 Next Steps:"
    echo "   1. Review the generated content in $OUTPUT_DIR/07_generated_content.json"
    echo "   2. Check SEO optimization suggestions in $OUTPUT_DIR/08_seo_optimization.json"
    echo "   3. Analyze performance metrics in $OUTPUT_DIR/09_performance_analysis.json"
    echo "   4. Add API keys to .env file for production-quality responses"
    echo ""
    
    # Integration example
    echo "🔗 Integration Example:"
    echo "   # Extract generated content"
    echo "   CONTENT=\$(cat $OUTPUT_DIR/07_generated_content.json | jq -r '.data.content // .content')"
    echo "   echo \"\$CONTENT\" > my_blog_post.md"
    echo ""
}

# Error handling
trap 'log_error "Script interrupted"; exit 1' INT TERM

# Check dependencies
check_deps() {
    if ! command -v curl &> /dev/null; then
        log_error "curl is required but not installed"
        exit 1
    fi
    
    if ! command -v jq &> /dev/null; then
        log_warning "jq is not installed - JSON formatting will be limited"
        log_info "Install jq for better output: brew install jq (macOS) or apt-get install jq (Ubuntu)"
    fi
}

# Parse command line arguments
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo "CrewAI Content Creation Agent - API Sequence Test"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --help, -h    Show this help message"
    echo "  --url URL     Use custom API URL (default: $APP_URL)"
    echo "  --timeout N   Set timeout in seconds (default: $TIMEOUT)"
    echo "  --output DIR  Set output directory (default: $OUTPUT_DIR)"
    echo ""
    echo "Examples:"
    echo "  $0"
    echo "  $0 --url https://my-app.fly.dev --timeout 60"
    echo "  $0 --output ./my_test_results"
    exit 0
fi

# Parse options
while [[ $# -gt 0 ]]; do
    case $1 in
        --url)
            APP_URL="$2"
            shift 2
            ;;
        --timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Run the test
check_deps
main

echo -e "${GREEN}✨ Test completed successfully!${NC}" 