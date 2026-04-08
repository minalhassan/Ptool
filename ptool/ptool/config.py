"""Configuration management for PTool"""

import json
import os
from pathlib import Path
from typing import Optional
from rich.console import Console

console = Console()

class Config:
    """Manages PTool configuration"""
    
    CONFIG_DIR = Path.home() / ".ptool"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    HISTORY_FILE = CONFIG_DIR / "history.json"
    
    def __init__(self):
        self.config_dir = self.CONFIG_DIR
        self.config_file = self.CONFIG_FILE
        self.history_file = self.HISTORY_FILE
        self._ensure_config_dir()
    
    def _ensure_config_dir(self):
        """Create config directory if it doesn't exist"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.config_file.exists():
            self._write_config({"api_key": None, "default_model": "gemini-pro"})
        
        if not self.history_file.exists():
            self._write_history([])
    
    def _write_config(self, data: dict):
        """Write configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _read_config(self) -> dict:
        """Read configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            console.print(f"[red]Error reading config: {e}[/red]")
            return {}
    
    def _write_history(self, data: list):
        """Write history to file"""
        with open(self.history_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _read_history(self) -> list:
        """Read history from file"""
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except Exception:
            return []
    
    def set_api_key(self, api_key: str):
        """Set Gemini API key"""
        config = self._read_config()
        config["api_key"] = api_key
        self._write_config(config)
        console.print("[green]✓ API key saved successfully[/green]")
    
    def get_api_key(self) -> Optional[str]:
        """Get Gemini API key"""
        config = self._read_config()
        api_key = config.get("api_key") or os.getenv("GEMINI_API_KEY")
        return api_key
    
    def add_to_history(self, entry: dict):
        """Add command to history"""
        history = self._read_history()
        history.append(entry)
        # Keep only last 100 entries
        if len(history) > 100:
            history = history[-100:]
        self._write_history(history)
    
    def get_history(self, limit: int = 10) -> list:
        """Get command history"""
        history = self._read_history()
        return history[-limit:]
    
    def clear_history(self):
        """Clear command history"""
        self._write_history([])
        console.print("[green]✓ History cleared[/green]")