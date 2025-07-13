"""
Content Creation Crew - CrewAI Multi-Agent System
A professional content creation team powered by AI agents working together.

This example demonstrates:
- Multi-agent collaboration using CrewAI
- Role-based task delegation
- Real-world business applications
- LLM-powered intelligent workflows
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed, using system environment variables")
except Exception as e:
    print(f"⚠️  Failed to load .env file: {e}")

# CrewAI imports
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# Set up LLM (prioritizes available API keys)
def get_llm():
    """Get the best available LLM based on environment variables"""
    
    # Check available API keys and their status
    available_llms = []
    
    if os.getenv('OPENAI_API_KEY'):
        available_llms.append("OpenAI (GPT-4o-mini)")
        try:
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
            print("✅ Using OpenAI GPT-4o-mini for content generation")
            return llm
        except Exception as e:
            print(f"⚠️  OpenAI API key found but failed to initialize: {e}")
    
    if os.getenv('ANTHROPIC_API_KEY'):
        available_llms.append("Anthropic (Claude-3-Sonnet)")
        try:
            llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.7)
            print("✅ Using Anthropic Claude-3-Sonnet for content generation")
            return llm
        except Exception as e:
            print(f"⚠️  Anthropic API key found but failed to initialize: {e}")
    
    if os.getenv('GROQ_API_KEY'):
        available_llms.append("Groq")
        try:
            from langchain_groq import ChatGroq
            llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0.7)
            print("✅ Using Groq Mixtral for content generation")
            return llm
        except Exception as e:
            print(f"⚠️  Groq API key found but failed to initialize: {e}")
    
    # Fallback to mock LLM for demo purposes
    print("⚠️  No LLM API keys available, using mock responses for demo")
    print(f"Available API keys detected: {', '.join(available_llms) if available_llms else 'None'}")
    
    from langchain_community.llms import FakeListLLM
    return FakeListLLM(responses=[
        "This is a mock response for demonstration purposes. Add API keys for real LLM functionality.",
        "Content research completed successfully using mock data.",
        "Article draft created with engaging introduction and conclusion - demo mode.",
        "Content edited and improved for clarity and flow - mock response.",
        "SEO optimization completed with targeted keywords - demo mode."
    ])

@dataclass
class ContentRequest:
    """Represents a content creation request"""
    topic: str
    content_type: str = "blog_post"  # blog_post, article, social_media, email
    target_audience: str = "general"
    tone: str = "professional"  # professional, casual, technical, creative
    word_count: int = 800
    keywords: List[str] = None
    request_id: str = None
    
    def __post_init__(self):
        if self.request_id is None:
            self.request_id = str(uuid.uuid4())
        if self.keywords is None:
            self.keywords = []

@dataclass 
class ContentResult:
    """Represents the final content creation result"""
    request_id: str
    topic: str
    research_summary: str
    draft_content: str
    edited_content: str
    seo_optimized_content: str
    seo_recommendations: str
    metadata: Dict[str, Any]
    created_at: str
    
class ContentCreationCrew:
    """Main class for the Content Creation Crew"""
    
    def __init__(self):
        self.llm = get_llm()
        self.search_tool = None
        self.scrape_tool = None
        
        # Initialize tools if API keys available
        if os.getenv('SERPER_API_KEY'):
            self.search_tool = SerperDevTool()
        if os.getenv('SERPER_API_KEY'):  # ScrapeWebsiteTool also needs some API access
            self.scrape_tool = ScrapeWebsiteTool()
        
        self._setup_agents()
    
    def _setup_agents(self):
        """Set up the specialized AI agents"""
        
        # Research Agent - Gathers information and insights
        self.researcher = Agent(
            role='Content Researcher',
            goal='Research comprehensive and accurate information about given topics',
            backstory="""You are an expert researcher with a knack for finding the most 
            relevant and up-to-date information. You excel at gathering insights from 
            multiple sources and synthesizing them into clear, actionable research summaries.""",
            tools=[self.search_tool, self.scrape_tool] if self.search_tool else [],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        
        # Writer Agent - Creates engaging content
        self.writer = Agent(
            role='Content Writer',
            goal='Create engaging, well-structured, and compelling content',
            backstory="""You are a skilled content writer with years of experience 
            creating engaging content across various formats. You have a talent for 
            translating complex information into accessible, compelling narratives 
            that resonate with target audiences.""",
            tools=[],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        
        # Editor Agent - Reviews and improves content
        self.editor = Agent(
            role='Content Editor',
            goal='Review, edit, and enhance content for clarity, flow, and impact',
            backstory="""You are a meticulous editor with an eye for detail and a 
            passion for perfection. You excel at improving content flow, clarity, 
            and engagement while maintaining the author's voice and intent.""",
            tools=[],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        
        # SEO Specialist Agent - Optimizes for search engines
        self.seo_specialist = Agent(
            role='SEO Specialist',
            goal='Optimize content for search engines while maintaining readability',
            backstory="""You are an SEO expert who understands the latest search 
            engine algorithms and best practices. You know how to naturally integrate 
            keywords and optimize content structure without sacrificing quality or readability.""",
            tools=[],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def create_content(self, request: ContentRequest) -> ContentResult:
        """Execute the full content creation workflow"""
        
        # Task 1: Research
        research_task = Task(
            description=f"""Research the topic '{request.topic}' for a {request.content_type} 
            targeting {request.target_audience}. Gather key information, statistics, trends, 
            and insights. Focus on finding recent, credible sources and unique angles.
            
            Target audience: {request.target_audience}
            Content type: {request.content_type}
            Desired tone: {request.tone}
            
            Provide a comprehensive research summary with key points, statistics, and insights.""",
            agent=self.researcher,
            expected_output="A comprehensive research summary with key findings, statistics, and insights about the topic."
        )
        
        # Task 2: Writing
        writing_task = Task(
            description=f"""Using the research findings, write a compelling {request.content_type} 
            about '{request.topic}'. The content should be approximately {request.word_count} words 
            and target {request.target_audience} with a {request.tone} tone.
            
            Requirements:
            - Engaging headline/title
            - Clear introduction that hooks the reader
            - Well-structured body with logical flow
            - Strong conclusion with call-to-action
            - Natural integration of key research points
            
            Write in {request.tone} tone for {request.target_audience} audience.""",
            agent=self.writer,
            expected_output=f"A complete {request.content_type} of approximately {request.word_count} words with engaging title, introduction, body, and conclusion.",
            context=[research_task]
        )
        
        # Task 3: Editing
        editing_task = Task(
            description=f"""Review and edit the written content to improve clarity, flow, 
            and engagement. Focus on:
            
            - Grammar and spelling accuracy
            - Sentence structure and readability
            - Logical flow and transitions
            - Consistency in tone and voice
            - Overall impact and engagement
            - Ensuring {request.word_count} word target is met
            
            Provide the edited version with improvements while maintaining the original intent.""",
            agent=self.editor,
            expected_output="A polished, edited version of the content with improved clarity, flow, and engagement.",
            context=[writing_task]
        )
        
        # Task 4: SEO Optimization
        seo_task = Task(
            description=f"""Optimize the edited content for search engines while maintaining 
            readability and quality. Focus on:
            
            Target keywords: {', '.join(request.keywords) if request.keywords else 'Generate relevant keywords'}
            
            - Natural keyword integration
            - Meta description (150-160 characters)
            - Optimized title and headings (H1, H2, H3)
            - Internal linking suggestions
            - SEO recommendations for improvement
            
            Provide both the SEO-optimized content and a list of SEO recommendations.""",
            agent=self.seo_specialist,
            expected_output="SEO-optimized content with meta description, optimized headings, and a list of SEO recommendations.",
            context=[editing_task]
        )
        
        # Create and execute the crew
        crew = Crew(
            agents=[self.researcher, self.writer, self.editor, self.seo_specialist],
            tasks=[research_task, writing_task, editing_task, seo_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the workflow
        result = crew.kickoff()
        
        # Parse results from each task
        research_summary = research_task.output.raw if hasattr(research_task, 'output') else "Research completed"
        draft_content = writing_task.output.raw if hasattr(writing_task, 'output') else "Draft created"
        edited_content = editing_task.output.raw if hasattr(editing_task, 'output') else "Content edited"
        seo_content = seo_task.output.raw if hasattr(seo_task, 'output') else "SEO optimization completed"
        
        # Create structured result
        content_result = ContentResult(
            request_id=request.request_id,
            topic=request.topic,
            research_summary=research_summary,
            draft_content=draft_content,
            edited_content=edited_content,
            seo_optimized_content=seo_content,
            seo_recommendations="SEO recommendations: Focus on target keywords, optimize meta tags, improve internal linking.",
            metadata={
                "content_type": request.content_type,
                "target_audience": request.target_audience,
                "tone": request.tone,
                "word_count": request.word_count,
                "keywords": request.keywords
            },
            created_at=datetime.now().isoformat()
        )
        
        return content_result

# Global crew instance
content_crew = ContentCreationCrew()

# Web API Functions (Auto-detected endpoints)

def get_environment_status() -> Dict[str, Any]:
    """
    Get the status of environment variables and API keys.
    
    Returns:
        Dict with environment status and available services
    """
    api_keys = {
        'OPENAI_API_KEY': bool(os.getenv('OPENAI_API_KEY')),
        'ANTHROPIC_API_KEY': bool(os.getenv('ANTHROPIC_API_KEY')),
        'GROQ_API_KEY': bool(os.getenv('GROQ_API_KEY')),
        'GOOGLE_API_KEY': bool(os.getenv('GOOGLE_API_KEY')),
        'SERPER_API_KEY': bool(os.getenv('SERPER_API_KEY')),
        'PINECONE_API_KEY': bool(os.getenv('PINECONE_API_KEY')),
        'FIREWORKS_API_KEY': bool(os.getenv('FIREWORKS_API_KEY')),
        'MISTRAL_API_KEY': bool(os.getenv('MISTRAL_API_KEY'))
    }
    
    # Determine which LLM will be used
    active_llm = "Mock LLM (Demo Mode)"
    if os.getenv('OPENAI_API_KEY'):
        active_llm = "OpenAI GPT-4o-mini"
    elif os.getenv('ANTHROPIC_API_KEY'):
        active_llm = "Anthropic Claude-3-Sonnet"
    elif os.getenv('GROQ_API_KEY'):
        active_llm = "Groq Mixtral"
    
    # Count available services
    available_keys = sum(api_keys.values())
    
    return {
        "success": True,
        "environment_loaded": True,
        "active_llm": active_llm,
        "api_keys_status": api_keys,
        "available_services": available_keys,
        "total_possible_services": len(api_keys),
        "web_search_enabled": bool(os.getenv('SERPER_API_KEY')),
        "recommendations": [
            "Add OPENAI_API_KEY for best content quality",
            "Add SERPER_API_KEY for web research capabilities", 
            "Add ANTHROPIC_API_KEY for Claude alternative"
        ] if available_keys < 3 else ["All major services configured!"],
        "status": "production" if available_keys >= 2 else "demo"
    }

def get_crew_info() -> Dict[str, Any]:
    """
    Get information about the Content Creation Crew and its capabilities.
    
    Returns:
        Dict with crew information, agents, and capabilities
    """
    return {
        "success": True,
        "crew_name": "Content Creation Crew",
        "description": "AI-powered multi-agent system for professional content creation",
        "agents": [
            {
                "role": "Content Researcher",
                "description": "Researches topics and gathers comprehensive information",
                "capabilities": ["web research", "data analysis", "source verification"]
            },
            {
                "role": "Content Writer", 
                "description": "Creates engaging, well-structured content",
                "capabilities": ["creative writing", "storytelling", "audience targeting"]
            },
            {
                "role": "Content Editor",
                "description": "Reviews and enhances content quality",
                "capabilities": ["proofreading", "flow optimization", "clarity improvement"]
            },
            {
                "role": "SEO Specialist",
                "description": "Optimizes content for search engines",
                "capabilities": ["keyword optimization", "meta tag creation", "SEO analysis"]
            }
        ],
        "supported_content_types": ["blog_post", "article", "social_media", "email"],
        "supported_tones": ["professional", "casual", "technical", "creative"],
        "workflow": [
            "1. Research: Gather comprehensive information about the topic",
            "2. Write: Create engaging, structured content",
            "3. Edit: Review and improve clarity and flow", 
            "4. Optimize: Apply SEO best practices"
        ]
    }

def get_content_types() -> Dict[str, Any]:
    """
    Get available content types and their descriptions.
    
    Returns:
        Dict with supported content types
    """
    content_types = {
        "blog_post": {
            "name": "Blog Post",
            "description": "Engaging blog articles for websites and personal blogs",
            "typical_length": "800-1200 words",
            "best_for": "Thought leadership, tutorials, news, opinions"
        },
        "article": {
            "name": "Article",
            "description": "In-depth articles for publications and magazines",
            "typical_length": "1000-2000 words", 
            "best_for": "Deep-dive analysis, research findings, comprehensive guides"
        },
        "social_media": {
            "name": "Social Media Post",
            "description": "Short-form content for social platforms",
            "typical_length": "50-300 words",
            "best_for": "Engagement, announcements, quick tips, viral content"
        },
        "email": {
            "name": "Email Content",
            "description": "Email newsletters and marketing content",
            "typical_length": "300-800 words",
            "best_for": "Newsletters, promotional content, customer communication"
        }
    }
    
    return {
        "success": True,
        "content_types": content_types,
        "total_types": len(content_types)
    }

def create_content_request(topic: str, content_type: str = "blog_post", 
                          target_audience: str = "general", tone: str = "professional",
                          word_count: int = 800, keywords: List[str] = None) -> Dict[str, Any]:
    """
    Create a new content creation request and execute the full workflow.
    
    Args:
        topic: The main topic/subject for the content
        content_type: Type of content (blog_post, article, social_media, email)
        target_audience: Target audience (general, technical, business, etc.)
        tone: Writing tone (professional, casual, technical, creative)
        word_count: Desired word count
        keywords: List of target keywords for SEO
    
    Returns:
        Dict with the complete content creation result
    """
    try:
        # Create content request
        request = ContentRequest(
            topic=topic,
            content_type=content_type,
            target_audience=target_audience,
            tone=tone,
            word_count=word_count,
            keywords=keywords or []
        )
        
        # Execute content creation workflow
        result = content_crew.create_content(request)
        
        return {
            "success": True,
            "request_id": result.request_id,
            "topic": result.topic,
            "research_summary": result.research_summary,
            "final_content": result.seo_optimized_content,
            "seo_recommendations": result.seo_recommendations,
            "metadata": result.metadata,
            "created_at": result.created_at,
            "workflow_completed": True
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Content creation failed. Please check your request parameters."
        }

def get_content_status(request_id: str) -> Dict[str, Any]:
    """
    Get the status of a content creation request.
    
    Args:
        request_id: The unique request identifier
        
    Returns:
        Dict with request status and details
    """
    # In a real implementation, this would check a database or cache
    return {
        "success": True,
        "request_id": request_id,
        "status": "completed",
        "message": "Content creation workflow completed successfully",
        "stages": {
            "research": "completed", 
            "writing": "completed",
            "editing": "completed",
            "seo_optimization": "completed"
        },
        "estimated_completion": "2-3 minutes",
        "last_updated": datetime.now().isoformat()
    }

def create_quick_content(topic: str, content_type: str = "blog_post") -> Dict[str, Any]:
    """
    Create content quickly with default settings for rapid prototyping.
    
    Args:
        topic: The main topic for the content
        content_type: Type of content to create
        
    Returns:
        Dict with the created content
    """
    try:
        # Use default settings for quick content creation
        request = ContentRequest(
            topic=topic,
            content_type=content_type,
            target_audience="general",
            tone="professional", 
            word_count=600,  # Shorter for quick creation
            keywords=[]
        )
        
        result = content_crew.create_content(request)
        
        return {
            "success": True,
            "topic": topic,
            "content_type": content_type,
            "content": result.seo_optimized_content,
            "quick_mode": True,
            "created_at": result.created_at,
            "request_id": result.request_id
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Quick content creation failed"
        }

def get_seo_analysis(content: str, target_keywords: List[str] = None) -> Dict[str, Any]:
    """
    Analyze content for SEO optimization opportunities.
    
    Args:
        content: The content text to analyze
        target_keywords: List of target keywords
        
    Returns:
        Dict with SEO analysis and recommendations
    """
    try:
        # Basic SEO analysis (in real implementation, would use more sophisticated tools)
        word_count = len(content.split())
        char_count = len(content)
        
        # Simple keyword density calculation
        keyword_analysis = {}
        if target_keywords:
            content_lower = content.lower()
            for keyword in target_keywords:
                count = content_lower.count(keyword.lower())
                density = (count / word_count) * 100 if word_count > 0 else 0
                keyword_analysis[keyword] = {
                    "count": count,
                    "density": round(density, 2)
                }
        
        # Generate recommendations
        recommendations = []
        if word_count < 300:
            recommendations.append("Consider increasing content length for better SEO performance")
        if not target_keywords:
            recommendations.append("Define target keywords for better optimization")
        if char_count > 0 and not content.strip().startswith('<h1>'):
            recommendations.append("Add proper heading structure with H1, H2, H3 tags")
        
        return {
            "success": True,
            "analysis": {
                "word_count": word_count,
                "character_count": char_count,
                "estimated_reading_time": f"{max(1, word_count // 200)} minutes",
                "keyword_analysis": keyword_analysis,
                "seo_score": min(100, max(0, 50 + len(recommendations) * -10))  # Simple scoring
            },
            "recommendations": recommendations,
            "analyzed_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "SEO analysis failed"
        }

def get_writing_tips(content_type: str, target_audience: str = "general") -> Dict[str, Any]:
    """
    Get writing tips and best practices for specific content types and audiences.
    
    Args:
        content_type: Type of content (blog_post, article, etc.)
        target_audience: Target audience
        
    Returns:
        Dict with writing tips and best practices
    """
    tips_database = {
        "blog_post": {
            "general": [
                "Start with a compelling headline that promises value",
                "Use short paragraphs (2-3 sentences) for better readability", 
                "Include subheadings to break up content",
                "End with a clear call-to-action",
                "Use bullet points and numbered lists"
            ],
            "technical": [
                "Define technical terms clearly",
                "Use code examples and diagrams",
                "Structure with clear step-by-step instructions",
                "Include troubleshooting sections"
            ]
        },
        "article": {
            "general": [
                "Research thoroughly with credible sources",
                "Create an outline before writing",
                "Use data and statistics to support points",
                "Include expert quotes and insights",
                "Fact-check all claims"
            ]
        },
        "social_media": {
            "general": [
                "Keep it concise and engaging",
                "Use relevant hashtags strategically",
                "Include visual elements when possible",
                "Ask questions to encourage engagement",
                "Post at optimal times for your audience"
            ]
        }
    }
    
    content_tips = tips_database.get(content_type, {})
    audience_tips = content_tips.get(target_audience, content_tips.get("general", []))
    
    return {
        "success": True,
        "content_type": content_type,
        "target_audience": target_audience,
        "tips": audience_tips,
        "general_best_practices": [
            "Know your audience and write for them",
            "Use active voice when possible", 
            "Edit ruthlessly - remove unnecessary words",
            "Read your content aloud to check flow",
            "Use strong, specific verbs instead of weak adjectives"
        ]
    } 