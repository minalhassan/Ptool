"""Gemini API client for generating commands"""

import google.generativeai as genai
from typing import Optional, Dict
from rich.console import Console
import time

console = Console()

class GeminiClient:
    """Handles communication with Google Gemini API"""
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        """Initialize Gemini client"""
        if not api_key:
            raise ValueError("API key is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        self.chat = None
    
    def generate_command(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_retries: int = 3
    ) -> Optional[str]:
        """Generate command using Gemini API with retry logic"""
        
        for attempt in range(max_retries):
            try:
                generation_config = {
                    "temperature": temperature,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
                
                response = self.model.generate_content(
                    prompt,
                    generation_config=generation_config
                )
                
                if response.text:
                    return response.text
                else:
                    console.print("[yellow]⚠ Empty response from API[/yellow]")
                    return None
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    console.print(f"[yellow]⚠ API error, retrying in {wait_time}s... ({attempt + 1}/{max_retries})[/yellow]")
                    time.sleep(wait_time)
                else:
                    console.print(f"[red]✗ API Error: {str(e)}[/red]")
                    return None
        
        return None
    
    def start_chat(self):
        """Start a chat session"""
        self.chat = self.model.start_chat(history=[])
    
    def send_message(self, message: str) -> Optional[str]:
        """Send a message in chat mode"""
        if not self.chat:
            self.start_chat()
        
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            console.print(f"[red]✗ Chat Error: {str(e)}[/red]")
            return None
    
    def parse_response(self, response: str) -> Dict[str, str]:
        """Parse structured response from Gemini"""
        parsed = {
            "command": "",
            "explanation": "",
            "risk": "UNKNOWN",
            "alternatives": ""
        }
        
        current_section = None
        lines = response.split('\n')
        
        for line in lines:
            line_upper = line.strip().upper()
            
            if line_upper.startswith("COMMAND:"):
                current_section = "command"
                content = line.split(':', 1)[1].strip() if ':' in line else ""
                if content:
                    parsed["command"] = content
            elif line_upper.startswith("EXPLANATION:"):
                current_section = "explanation"
                content = line.split(':', 1)[1].strip() if ':' in line else ""
                if content:
                    parsed["explanation"] = content
            elif line_upper.startswith("RISK:"):
                current_section = "risk"
                content = line.split(':', 1)[1].strip() if ':' in line else ""
                if content:
                    parsed["risk"] = content.upper()
            elif line_upper.startswith("ALTERNATIVES:"):
                current_section = "alternatives"
                content = line.split(':', 1)[1].strip() if ':' in line else ""
                if content:
                    parsed["alternatives"] = content
            elif current_section and line.strip():
                # Continue adding to current section
                if parsed[current_section]:
                    parsed[current_section] += "\n" + line.strip()
                else:
                    parsed[current_section] = line.strip()
        
        # Clean up commands (remove markdown code blocks)
        parsed["command"] = parsed["command"].replace('```bash', '').replace('```', '').strip()
        
        return parsed