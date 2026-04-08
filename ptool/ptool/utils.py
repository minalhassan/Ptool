"""Utility functions for PTool"""

import pyperclip
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from datetime import datetime
from typing import Dict, Optional

console = Console()

def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard"""
    try:
        pyperclip.copy(text)
        return True
    except Exception as e:
        console.print(f"[yellow]⚠ Could not copy to clipboard: {e}[/yellow]")
        return False

def display_command_result(parsed: Dict[str, str], show_full: bool = True):
    """Display formatted command result"""
    
    # Command
    if parsed.get("command"):
        syntax = Syntax(parsed["command"], "bash", theme="monokai", line_numbers=False)
        console.print(Panel(
            syntax,
            title="[bold green]Command[/bold green]",
            border_style="green"
        ))
    
    # Explanation
    if show_full and parsed.get("explanation"):
        console.print(Panel(
            parsed["explanation"],
            title="[bold cyan]Explanation[/bold cyan]",
            border_style="cyan"
        ))
    
    # Risk level
    if parsed.get("risk"):
        risk = parsed["risk"].upper()
        risk_colors = {
            "LOW": "green",
            "MEDIUM": "yellow",
            "HIGH": "red"
        }
        color = risk_colors.get(risk, "white")
        console.print(f"\n[{color}]Risk Level: {risk}[/{color}]")
    
    # Alternatives
    if show_full and parsed.get("alternatives"):
        console.print(Panel(
            parsed["alternatives"],
            title="[bold magenta]Alternatives[/bold magenta]",
            border_style="magenta"
        ))

def display_history(history: list):
    """Display command history"""
    if not history:
        console.print("[yellow]No history found[/yellow]")
        return
    
    table = Table(title="Command History", show_header=True, header_style="bold cyan")
    table.add_column("#", style="dim", width=4)
    table.add_column("Timestamp", style="cyan", width=20)
    table.add_column("Task", style="green")
    table.add_column("Command", style="yellow")
    
    for idx, entry in enumerate(history, 1):
        timestamp = entry.get("timestamp", "Unknown")
        task = entry.get("task", "N/A")
        command = entry.get("command", "N/A")
        
        # Truncate command if too long
        if len(command) > 50:
            command = command[:47] + "..."
        
        table.add_row(str(idx), timestamp, task, command)
    
    console.print(table)

def display_templates(templates: dict, category: Optional[str] = None):
    """Display available templates"""
    if category:
        if category not in templates:
            console.print(f"[red]Category '{category}' not found[/red]")
            return
        
        templates = {category: templates[category]}
    
    for cat_name, cat_templates in templates.items():
        table = Table(title=f"{cat_name.upper()} Templates", show_header=True, header_style="bold cyan")
        table.add_column("Name", style="green")
        table.add_column("Description", style="yellow")
        table.add_column("Tools", style="magenta")
        
        for name, template in cat_templates.items():
            tools = ", ".join(template.get("tools", []))
            table.add_row(name, template.get("description", ""), tools)
        
        console.print(table)
        console.print()

def format_timestamp() -> str:
    """Get formatted timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def print_banner():
    """Print PTool banner"""
    banner = """
[bold cyan]
╔═══════════════════════════════════════════════════╗
║                                                   ║
║   ██████╗ ████████╗ ██████╗  ██████╗ ██╗         ║
║   ██╔══██╗╚══██╔══╝██╔═══██╗██╔═══██╗██║         ║
║   ██████╔╝   ██║   ██║   ██║██║   ██║██║         ║
║   ██╔═══╝    ██║   ██║   ██║██║   ██║██║         ║
║   ██║        ██║   ╚██████╔╝╚██████╔╝███████╗    ║
║   ╚═╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝    ║
║                                                   ║
║      AI-Powered Penetration Testing CLI          ║
║                 Version 1.0.0                     ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
[/bold cyan]
"""
    console.print(banner)