"""Safe command execution with user confirmation"""

import subprocess
import shlex
from typing import Optional, Tuple
from rich.console import Console
from rich.prompt import Confirm
from rich.panel import Panel
import re

console = Console()

class CommandExecutor:
    """Safely executes penetration testing commands"""
    
    DANGEROUS_PATTERNS = [
        r'rm\s+-rf\s+/',
        r'mkfs\.',
        r'dd\s+if=.*of=/dev/',
        r':(){ :|:& };:',  # Fork bomb
        r'chmod\s+-R\s+777\s+/',
        r'shutdown',
        r'reboot',
        r'init\s+0',
    ]
    
    def __init__(self):
        self.last_output = None
    
    def is_dangerous(self, command: str) -> Tuple[bool, Optional[str]]:
        """Check if command matches dangerous patterns"""
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return True, f"Matches dangerous pattern: {pattern}"
        return False, None
    
    def validate_command(self, command: str) -> Tuple[bool, Optional[str]]:
        """Validate command before execution"""
        if not command or not command.strip():
            return False, "Empty command"
        
        # Check for dangerous patterns
        is_dangerous, reason = self.is_dangerous(command)
        if is_dangerous:
            return False, f"⚠️  DANGEROUS COMMAND DETECTED: {reason}"
        
        # Check if command exists
        cmd_parts = shlex.split(command)
        if not cmd_parts:
            return False, "Invalid command format"
        
        return True, None
    
    def execute(
        self,
        command: str,
        timeout: int = 300,
        require_confirmation: bool = True
    ) -> Tuple[bool, str]:
        """Execute command with safety checks"""
        
        # Validate command
        valid, error = self.validate_command(command)
        if not valid:
            console.print(f"[red]✗ {error}[/red]")
            return False, error
        
        # Show command
        console.print(Panel(
            f"[cyan]{command}[/cyan]",
            title="[yellow]Command to Execute[/yellow]",
            border_style="yellow"
        ))
        
        # Check for dangerous patterns
        is_dangerous, reason = self.is_dangerous(command)
        if is_dangerous:
            console.print(f"[red]⚠️  WARNING: {reason}[/red]")
        
        # Ask for confirmation
        if require_confirmation:
            if not Confirm.ask("Do you want to execute this command?", default=False):
                console.print("[yellow]⊗ Execution cancelled[/yellow]")
                return False, "Execution cancelled by user"
        
        # Execute command
        try:
            console.print("[cyan]► Executing...[/cyan]")
            
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            try:
                stdout, stderr = process.communicate(timeout=timeout)
                
                if process.returncode == 0:
                    console.print("[green]✓ Command executed successfully[/green]\n")
                    if stdout:
                        console.print("[white]Output:[/white]")
                        console.print(stdout)
                    self.last_output = stdout
                    return True, stdout
                else:
                    console.print(f"[red]✗ Command failed with exit code {process.returncode}[/red]\n")
                    if stderr:
                        console.print("[red]Error:[/red]")
                        console.print(stderr)
                    return False, stderr
                    
            except subprocess.TimeoutExpired:
                process.kill()
                error_msg = f"Command timed out after {timeout} seconds"
                console.print(f"[red]✗ {error_msg}[/red]")
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Execution error: {str(e)}"
            console.print(f"[red]✗ {error_msg}[/red]")
            return False, error_msg
    
    def execute_pipe(self, commands: list, timeout: int = 300) -> Tuple[bool, str]:
        """Execute piped commands"""
        full_command = " | ".join(commands)
        return self.execute(full_command, timeout=timeout)