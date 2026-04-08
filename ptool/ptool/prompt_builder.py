"""Builds optimized prompts for Gemini API"""

from typing import Optional

class PromptBuilder:
    """Constructs structured prompts for penetration testing tasks"""
    
    SYSTEM_PROMPT = """You are an expert penetration tester and CTF player with deep knowledge of:
- Network security and reconnaissance
- Web application security
- Privilege escalation techniques
- Linux/Unix command line tools
- Common pentesting frameworks (Metasploit, Burp Suite, etc.)

Your responses must be precise, practical, and use real tools available in Kali Linux."""

    @staticmethod
    def build_command_prompt(
        task: str,
        target: Optional[str] = None,
        mode: str = "general",
        stealth: bool = False,
        fast: bool = False,
        verbose: bool = False,
        context: Optional[str] = None
    ) -> str:
        """Build a structured prompt for command generation"""
        
        # Base prompt
        prompt_parts = [
            f"Generate a precise Linux command for the following task: {task}",
        ]
        
        # Add target if provided
        if target:
            prompt_parts.append(f"\nTarget: {target}")
        
        # Add mode-specific instructions
        mode_instructions = {
            "recon": "Focus on reconnaissance and information gathering. Use tools like nmap, dig, whois, sublist3r.",
            "web": "Focus on web application testing. Use tools like gobuster, ffuf, nikto, burpsuite, sqlmap.",
            "privesc": "Focus on privilege escalation techniques. Use tools like linpeas, find, sudo -l.",
            "exploit": "Focus on exploitation techniques. Provide safe, educational examples.",
            "ctf": "Focus on CTF-specific techniques and creative solutions."
        }
        
        if mode in mode_instructions:
            prompt_parts.append(f"\nMode: {mode_instructions[mode]}")
        
        # Add flags
        flags = []
        if stealth:
            flags.append("stealth (use techniques to avoid detection)")
        if fast:
            flags.append("fast (optimize for speed)")
        if verbose:
            flags.append("verbose (detailed output)")
        
        if flags:
            prompt_parts.append(f"\nRequirements: {', '.join(flags)}")
        
        # Add context
        if context:
            prompt_parts.append(f"\nAdditional context: {context}")
        
        # Output format instructions
        prompt_parts.append("""

Provide your response in the following EXACT format:

COMMAND:
[The exact command to run]

EXPLANATION:
[Brief explanation of what the command does and why each flag is used]

RISK:
[LOW/MEDIUM/HIGH - potential risk level]

ALTERNATIVES:
[Alternative commands or approaches, if any]

Rules:
- Provide only one primary command (unless alternatives are needed)
- Use real tools available in Kali Linux
- Commands must be copy-paste ready
- Avoid unnecessary verbosity
- Consider safety and legality""")
        
        return "\n".join(prompt_parts)
    
    @staticmethod
    def build_explain_prompt(command: str) -> str:
        """Build a prompt to explain an existing command"""
        return f"""Explain the following penetration testing command in detail:

Command: {command}

Provide:
1. What the command does
2. Each flag/parameter explanation
3. Expected output
4. Risk level (LOW/MEDIUM/HIGH)
5. Common use cases
6. Potential issues or warnings"""

    @staticmethod
    def build_ctf_prompt(challenge: str, hints: Optional[str] = None) -> str:
        """Build a prompt for CTF challenges"""
        prompt = f"""Help solve this CTF challenge:

Challenge: {challenge}
"""
        if hints:
            prompt += f"\nHints: {hints}"
        
        prompt += """

Provide:
APPROACH:
[Step-by-step approach to solve this challenge]

COMMANDS:
[Specific commands to try]

TOOLS:
[Recommended tools]

TIPS:
[Additional tips and tricks]"""
        
        return prompt