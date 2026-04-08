"""Predefined templates for common penetration testing tasks"""

TEMPLATES = {
    "recon": {
        "port_scan": {
            "description": "Quick port scan",
            "command": "nmap -sV -T4 {target}",
            "tools": ["nmap"]
        },
        "full_scan": {
            "description": "Comprehensive port scan",
            "command": "nmap -sS -sV -sC -O -p- -T4 {target}",
            "tools": ["nmap"]
        },
        "dns_enum": {
            "description": "DNS enumeration",
            "command": "dig {target} ANY +noall +answer",
            "tools": ["dig"]
        },
        "subdomain_enum": {
            "description": "Subdomain enumeration",
            "command": "sublist3r -d {target}",
            "tools": ["sublist3r"]
        }
    },
    "web": {
        "dir_bruteforce": {
            "description": "Directory brute forcing",
            "command": "gobuster dir -u http://{target} -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt",
            "tools": ["gobuster"]
        },
        "ffuf_dirs": {
            "description": "Fast directory fuzzing",
            "command": "ffuf -u http://{target}/FUZZ -w /usr/share/wordlists/dirb/common.txt",
            "tools": ["ffuf"]
        },
        "nikto_scan": {
            "description": "Web vulnerability scan",
            "command": "nikto -h http://{target}",
            "tools": ["nikto"]
        },
        "wpscan": {
            "description": "WordPress security scan",
            "command": "wpscan --url http://{target} --enumerate u,p,t",
            "tools": ["wpscan"]
        }
    },
    "exploit": {
        "sqli_test": {
            "description": "SQL injection testing",
            "command": "sqlmap -u 'http://{target}' --batch --dbs",
            "tools": ["sqlmap"]
        },
        "xss_test": {
            "description": "XSS vulnerability testing",
            "command": "dalfox url http://{target}",
            "tools": ["dalfox"]
        }
    },
    "privesc": {
        "linpeas": {
            "description": "Linux privilege escalation check",
            "command": "curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh",
            "tools": ["curl"]
        },
        "suid_find": {
            "description": "Find SUID binaries",
            "command": "find / -perm -4000 -type f 2>/dev/null",
            "tools": ["find"]
        }
    }
}

def get_template(category: str, template_name: str, target: str = "") -> dict:
    """Get a template by category and name"""
    if category in TEMPLATES and template_name in TEMPLATES[category]:
        template = TEMPLATES[category][template_name].copy()
        if target:
            template["command"] = template["command"].format(target=target)
        return template
    return None

def list_templates(category: str = None) -> dict:
    """List all templates or templates in a category"""
    if category:
        return TEMPLATES.get(category, {})
    return TEMPLATES