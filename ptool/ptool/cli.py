"""CLI interface using Typer"""

import typer
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt
from enum import Enum

from .config import Config
from .gemini_client import GeminiClient
from .prompt_builder import PromptBuilder
from .executor import CommandExecutor
from .utils import (
    display_command_result,
    display_history,
    display_templates,
    copy_to_clipboard,
    format_timestamp,
    print_banner
)
from .templates import list_templates, get_template

app = typer.Typer(help="AI-Powered Penetration Testing CLI Tool")
console = Console()
config = Config()

class Mode(str, Enum):
    """Available modes"""
    recon = "recon"
    web = "web"
    exploit = "exploit"
    privesc = "privesc"
    ctf = "ctf"
    general = "general"

# Global state
executor = CommandExecutor()

@app.command()
def setup(
    api_key: str = typer.Option(None, "--api-key", "-k", help="Gemini API key")
):
    """Setup PTool configuration"""
    print_banner()
    
    if not api_key:
        api_key = Prompt.ask("Enter your Gemini API key", password=True)
    
    config.set_api_key(api_key)
    console.print("[green]✓ PTool configured successfully![/green]")
    console.print("\n[cyan]Try: ptool generate --help[/cyan]")

@app.command()
def generate(
    task: str = typer.Argument(..., help="Task description or goal"),
    target: Optional[str] = typer.Option(None, "--target", "-t", help="Target IP/domain"),
    mode: Mode = typer.Option(Mode.general, "--mode", "-m", help="Operation mode"),
    stealth: bool = typer.Option(False, "--stealth", "-s", help="Use stealth techniques"),
    fast: bool = typer.Option(False, "--fast", "-f", help="Optimize for speed"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    context: Optional[str] = typer.Option(None, "--context", "-c", help="Additional context"),
    execute: bool = typer.Option(False, "--execute", "-e", help="Execute command after generation"),
    copy: bool = typer.Option(False, "--copy", help="Copy command to clipboard"),
    explain: bool = typer.Option(True, "--explain/--no-explain", help="Show explanation")
):
    """Generate penetration testing commands"""
    
    # Check API key
    api_key = config.get_api_key()
    if not api_key:
        console.print("[red]✗ API key not configured. Run 'ptool setup' first.[/red]")
        raise typer.Exit(1)
    
    # Initialize client
    try:
        client = GeminiClient(api_key)
    except Exception as e:
        console.print(f"[red]✗ Failed to initialize Gemini client: {e}[/red]")
        raise typer.Exit(1)
    
    # Build prompt
    console.print("[cyan]► Generating command...[/cyan]")
    prompt = PromptBuilder.build_command_prompt(
        task=task,
        target=target,
        mode=mode.value,
        stealth=stealth,
        fast=fast,
        verbose=verbose,
        context=context
    )
    
    # Generate command
    response = client.generate_command(prompt)
    
    if not response:
        console.print("[red]✗ Failed to generate command[/red]")
        raise typer.Exit(1)
    
    # Parse response
    parsed = client.parse_response(response)
    
    # Display result
    display_command_result(parsed, show_full=explain)
    
    # Copy to clipboard
    if copy and parsed.get("command"):
        if copy_to_clipboard(parsed["command"]):
            console.print("\n[green]✓ Command copied to clipboard[/green]")
    
    # Save to history
    config.add_to_history({
        "timestamp": format_timestamp(),
        "task": task,
        "target": target or "N/A",
        "mode": mode.value,
        "command": parsed.get("command", ""),
        "risk": parsed.get("risk", "UNKNOWN")
    })
    
    # Execute if requested
    if execute and parsed.get("command"):
        console.print()
        executor.execute(parsed["command"])

@app.command()
def recon(
    target: str = typer.Argument(..., help="Target IP/domain"),
    task: str = typer.Option("reconnaissance", "--task", help="Specific recon task"),
    fast: bool = typer.Option(False, "--fast", "-f", help="Fast scan"),
    stealth: bool = typer.Option(False, "--stealth", "-s", help="Stealth mode"),
    execute: bool = typer.Option(False, "--execute", "-e", help="Execute command")
):
    """Reconnaissance mode"""
    
    full_task = f"{task} on {target}"
    
    ctx = typer.Context(generate)
    ctx.invoke(
        generate,
        task=full_task,
        target=target,
        mode=Mode.recon,
        fast=fast,
        stealth=stealth,
        execute=execute
    )

@app.command()
def web(
    target: str = typer.Argument(..., help="Target URL/domain"),
    task: str = typer.Option("web application testing", "--task", help="Specific web task"),
    execute: bool = typer.Option(False, "--execute", "-e", help="Execute command")
):
    """Web application testing mode"""
    
    full_task = f"{task} on {target}"
    
    ctx = typer.Context(generate)
    ctx.invoke(
        generate,
        task=full_task,
        target=target,
        mode=Mode.web,
        execute=execute
    )

@app.command()
def ctf(
    challenge: str = typer.Argument(..., help="CTF challenge description"),
    hints: Optional[str] = typer.Option(None, "--hints", "-h", help="Challenge hints"),
):
    """CTF helper mode"""
    
    api_key = config.get_api_key()
    if not api_key:
        console.print("[red]✗ API key not configured. Run 'ptool setup' first.[/red]")
        raise typer.Exit(1)
    
    client = GeminiClient(api_key)
    
    console.print("[cyan]► Analyzing CTF challenge...[/cyan]")
    prompt = PromptBuilder.build_ctf_prompt(challenge, hints)
    
    response = client.generate_command(prompt)
    
    if response:
        console.print("\n" + response)
    else:
        console.print("[red]✗ Failed to analyze challenge[/red]")

@app.command()
def explain(
    command: str = typer.Argument(..., help="Command to explain")
):
    """Explain a penetration testing command"""
    
    api_key = config.get_api_key()
    if not api_key:
        console.print("[red]✗ API key not configured. Run 'ptool setup' first.[/red]")
        raise typer.Exit(1)
    
    client = GeminiClient(api_key)
    
    console.print("[cyan]► Analyzing command...[/cyan]")
    prompt = PromptBuilder.build_explain_prompt(command)
    
    response = client.generate_command(prompt)
    
    if response:
        console.print("\n" + response)
    else:
        console.print("[red]✗ Failed to explain command[/red]")

@app.command()
def history(
    limit: int = typer.Option(10, "--limit", "-n", help="Number of entries to show"),
    clear: bool = typer.Option(False, "--clear", help="Clear history")
):
    """Show or clear command history"""
    
    if clear:
        config.clear_history()
        return
    
    history_entries = config.get_history(limit)
    display_history(history_entries)

@app.command()
def templates(
    category: Optional[str] = typer.Argument(None, help="Template category"),
    use: Optional[str] = typer.Option(None, "--use", "-u", help="Use template (format: category:name)"),
    target: Optional[str] = typer.Option(None, "--target", "-t", help="Target for template")
):
    """List or use predefined templates"""
    
    all_templates = list_templates()
    
    if use:
        # Use template
        if ":" not in use:
            console.print("[red]✗ Template format should be 'category:name'[/red]")
            raise typer.Exit(1)
        
        cat, name = use.split(":", 1)
        template = get_template(cat, name, target or "")
        
        if not template:
            console.print(f"[red]✗ Template '{use}' not found[/red]")
            raise typer.Exit(1)
        
        console.print(f"\n[green]Template: {cat}:{name}[/green]")
        console.print(f"[yellow]Description: {template['description']}[/yellow]")
        console.print(f"\n[cyan]Command:[/cyan]\n{template['command']}")
        
        if copy_to_clipboard(template['command']):
            console.print("\n[green]✓ Command copied to clipboard[/green]")
    else:
        # List templates
        display_templates(all_templates, category)

@app.command()
def execute(
    command: str = typer.Argument(..., help="Command to execute"),
    no_confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation")
):
    """Execute a command with safety checks"""
    
    executor.execute(command, require_confirmation=not no_confirm)

@app.callback()
def main(
    version: bool = typer.Option(False, "--version", help="Show version")
):
    """
    PTool - AI-Powered Penetration Testing CLI
    
    Generate and execute penetration testing commands using AI.
    """
    if version:
        from . import __version__
        console.print(f"PTool version {__version__}")
        raise typer.Exit()