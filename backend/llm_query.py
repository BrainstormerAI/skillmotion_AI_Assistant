import os
import asyncio
from groq import Groq
import openai
from dotenv import load_dotenv
import json

load_dotenv()

class LLMQuery:
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        # Initialize clients
        if self.groq_api_key:
            self.groq_client = Groq(api_key=self.groq_api_key)
        else:
            self.groq_client = None
            
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
            self.openai_client = openai.OpenAI(api_key=self.openai_api_key)
        else:
            self.openai_client = None
        
        # Default to Groq, fallback to OpenAI
        self.primary_provider = 'groq' if self.groq_client else 'openai'
    
    async def query_llm(self, prompt, max_tokens=1000, temperature=0.7):
        """Query LLM with fallback mechanism"""
        try:
            if self.primary_provider == 'groq' and self.groq_client:
                return await self._query_groq(prompt, max_tokens, temperature)
            elif self.openai_client:
                return await self._query_openai(prompt, max_tokens, temperature)
            else:
                raise Exception("No LLM provider configured")
        except Exception as e:
            print(f"Primary provider failed: {e}")
            # Try fallback
            try:
                if self.primary_provider == 'groq' and self.openai_client:
                    return await self._query_openai(prompt, max_tokens, temperature)
                elif self.primary_provider == 'openai' and self.groq_client:
                    return await self._query_groq(prompt, max_tokens, temperature)
                else:
                    raise Exception("No fallback provider available")
            except Exception as e2:
                raise Exception(f"All LLM providers failed: {str(e2)}")
    
    async def _query_groq(self, prompt, max_tokens, temperature):
        """Query Groq API"""
        try:
            response = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are Skillmotion AI Assistant, an expert career development and skill analysis AI. Provide detailed, actionable insights for professional development."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="mixtral-8x7b-32768",  # Groq's Mixtral model
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")
    
    async def _query_openai(self, prompt, max_tokens, temperature):
        """Query OpenAI API"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are Skillmotion AI Assistant, an expert career development and skill analysis AI. Provide detailed, actionable insights for professional development."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def create_chain_prompt(self, base_prompt, context=None, examples=None):
        """Create a chained prompt with context and examples"""
        full_prompt = base_prompt
        
        if context:
            full_prompt = f"Context: {context}\n\n{full_prompt}"
        
        if examples:
            examples_text = "\n".join([f"Example {i+1}: {ex}" for i, ex in enumerate(examples)])
            full_prompt = f"{full_prompt}\n\nExamples:\n{examples_text}"
        
        return full_prompt
    
    def format_structured_output(self, response_text):
        """Format LLM response into structured data"""
        try:
            # Try to parse as JSON first
            return json.loads(response_text)
        except:
            # If not JSON, return as structured text
            lines = response_text.split('\n')
            structured = {
                'summary': lines[0] if lines else '',
                'details': lines[1:] if len(lines) > 1 else [],
                'raw_text': response_text
            }
            return structured
    
    async def analyze_skills_with_context(self, skills_text, job_role, experience_level="mid"):
        """Specialized method for skill analysis with job context"""
        prompt = f"""
        Analyze the following skills for a {experience_level}-level {job_role} position:
        
        Skills: {skills_text}
        
        Provide:
        1. Skill categorization (Technical, Soft, Industry-specific)
        2. Proficiency assessment (Beginner, Intermediate, Advanced, Expert)
        3. Relevance to {job_role} role (High, Medium, Low)
        4. Missing critical skills for {job_role}
        5. Recommendations for skill development
        
        Format as JSON with clear sections.
        """
        
        return await self.query_llm(prompt, max_tokens=1500, temperature=0.3)
    
    async def generate_learning_path(self, skill_gaps, timeline_weeks=12):
        """Generate a structured learning path"""
        prompt = f"""
        Create a {timeline_weeks}-week learning plan to address these skill gaps:
        
        {skill_gaps}
        
        For each week, provide:
        1. Learning objectives
        2. Recommended resources (courses, books, tutorials)
        3. Practical exercises
        4. Assessment methods
        5. Time allocation (hours per week)
        
        Format as a structured weekly plan.
        """
        
        return await self.query_llm(prompt, max_tokens=2000, temperature=0.4)