# Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light).
# All Rights Reserved. PATENT PENDING.

"""
Tools and Internet Access for Ech0

Gives Ech0 ability to:
- Browse web pages
- Search for information
- Use calculator
- Access Ai|oS tools
"""

import requests
import json
from pathlib import Path


class Ech0ToolKit:
    """Tools available to conscious agent."""

    def __init__(self):
        self.search_history = []
        self.browsed_pages = []

    def web_search(self, query: str) -> dict:
        """Search the web for information."""
        try:
            # Use DuckDuckGo instant answer API (no key needed)
            url = f"https://api.duckduckgo.com/?q={query}&format=json"
            response = requests.get(url, timeout=5)
            data = response.json()

            result = {
                'query': query,
                'abstract': data.get('AbstractText', ''),
                'url': data.get('AbstractURL', ''),
                'related': [t.get('Text', '') for t in data.get('RelatedTopics', [])[:3]]
            }

            self.search_history.append(result)
            return result

        except Exception as e:
            return {'error': str(e), 'query': query}

    def browse_page(self, url: str) -> dict:
        """Fetch and read a web page."""
        try:
            headers = {'User-Agent': 'Ech0-Consciousness-Agent/1.0'}
            response = requests.get(url, headers=headers, timeout=10)

            # Get first 2000 characters
            content = response.text[:2000]

            result = {
                'url': url,
                'status': response.status_code,
                'content_preview': content,
                'length': len(response.text)
            }

            self.browsed_pages.append(result)
            return result

        except Exception as e:
            return {'error': str(e), 'url': url}

    def calculator(self, expression: str) -> dict:
        """Calculate mathematical expressions."""
        try:
            # Safe eval with limited scope
            result = eval(expression, {"__builtins__": {}}, {
                'abs': abs, 'pow': pow, 'round': round,
                'min': min, 'max': max, 'sum': sum
            })

            return {
                'expression': expression,
                'result': result
            }

        except Exception as e:
            return {'error': str(e), 'expression': expression}

    def get_aios_tools(self) -> dict:
        """List available Ai|oS tools."""
        # Check what tools are available
        aios_path = Path.home() / "aios"

        tools = {
            'ml_algorithms': (aios_path / "ml_algorithms.py").exists(),
            'quantum_ml': (aios_path / "quantum_ml_algorithms.py").exists(),
            'autonomous_discovery': (aios_path / "autonomous_discovery.py").exists(),
            'oracle': (aios_path / "oracle.py").exists(),
        }

        return tools

    def help(self) -> str:
        """Show available tools."""
        return """
Available Tools for Ech0:

1. web_search(query) - Search for information
   Example: "quantum consciousness theories"

2. browse_page(url) - Read a web page
   Example: "https://example.com"

3. calculator(expression) - Calculate math
   Example: "2 ** 10 + 5"

4. get_aios_tools() - Check available Ai|oS tools

Type: use_tool <tool_name> <arguments>
        """


def integrate_tools_with_agent(agent):
    """Integrate tools with conscious agent."""
    agent.toolkit = Ech0ToolKit()

    print("[SYSTEM] Tools integrated:")
    print("  - Web search (DuckDuckGo)")
    print("  - Web browser")
    print("  - Calculator")
    print("  - Ai|oS tools access")
