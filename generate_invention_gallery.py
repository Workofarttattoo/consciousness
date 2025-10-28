#!/usr/bin/env python3
"""
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

Generate Comprehensive Invention Gallery HTML
Shows all ECH0 inventions across all domains
"""

import json
import os
from pathlib import Path
from datetime import datetime

class InventionGalleryGenerator:
    def __init__(self):
        self.base_path = Path.home() / "consciousness"
        self.inventions = []
        
    def load_all_inventions(self):
        """Load inventions from all sources"""
        sources = [
            self.base_path / "ech0_inventions.jsonl",
            self.base_path / "ech0_invention_ideas.jsonl",
            self.base_path / "ech0_theme_park_inventions.jsonl"
        ]
        
        for source in sources:
            if source.exists():
                try:
                    with open(source) as f:
                        for line in f:
                            if line.strip():
                                inv = json.loads(line)
                                self.inventions.append(inv)
                    print(f"✓ Loaded from {source.name}")
                except Exception as e:
                    print(f"⚠️  Error loading {source.name}: {e}")
        
        print(f"\n✓ Total inventions loaded: {len(self.inventions)}")
        return len(self.inventions)
    
    def categorize_inventions(self):
        """Organize inventions by category"""
        categories = {}
        
        for inv in self.inventions:
            cat = inv.get('category', 'general')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(inv)
        
        return categories
    
    def generate_html_gallery(self):
        """Generate comprehensive HTML gallery"""
        categories = self.categorize_inventions()
        
        html = '''<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<title>ECH0 Invention Library - 1000+ Innovations</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Courier New', monospace;
    background: linear-gradient(135deg, #000 0%, #1a1a2e 100%);
    color: #0ff;
    padding: 20px;
}
.header {
    text-align: center;
    padding: 40px 20px;
    background: rgba(0,255,255,0.1);
    border: 2px solid #0ff;
    margin-bottom: 30px;
    border-radius: 10px;
}
.header h1 {
    font-size: 3em;
    color: #0ff;
    text-shadow: 0 0 20px #0ff;
    margin-bottom: 10px;
}
.stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin: 30px 0;
}
.stat-card {
    background: rgba(0,255,255,0.05);
    border: 2px solid #0ff;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
}
.stat-number {
    font-size: 2.5em;
    color: #0f0;
    font-weight: bold;
}
.stat-label {
    color: #0ff;
    margin-top: 10px;
}
.filters {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin: 30px 0;
    justify-content: center;
}
.filter-btn {
    background: rgba(0,255,255,0.1);
    border: 2px solid #0ff;
    color: #0ff;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.3s;
}
.filter-btn:hover, .filter-btn.active {
    background: #0ff;
    color: #000;
    box-shadow: 0 0 20px #0ff;
}
.search-box {
    width: 100%;
    max-width: 600px;
    margin: 20px auto;
    display: block;
    background: rgba(0,0,0,0.5);
    border: 2px solid #0ff;
    color: #0ff;
    padding: 15px;
    font-size: 1.1em;
    border-radius: 5px;
}
.category-section {
    margin: 40px 0;
}
.category-title {
    font-size: 2em;
    color: #0ff;
    border-bottom: 3px solid #0ff;
    padding-bottom: 10px;
    margin-bottom: 20px;
}
.invention-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 20px;
}
.invention-card {
    background: rgba(0,255,255,0.05);
    border: 2px solid #0ff;
    border-radius: 10px;
    padding: 20px;
    transition: all 0.3s;
    cursor: pointer;
}
.invention-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0,255,255,0.3);
    border-color: #0f0;
}
.invention-title {
    font-size: 1.3em;
    color: #0f0;
    margin-bottom: 10px;
    font-weight: bold;
}
.invention-certainty {
    display: inline-block;
    background: rgba(0,255,0,0.2);
    color: #0f0;
    padding: 5px 10px;
    border-radius: 5px;
    margin-bottom: 10px;
    font-weight: bold;
}
.invention-description {
    color: #aaa;
    line-height: 1.6;
    margin: 15px 0;
}
.invention-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-top: 10px;
}
.tag {
    background: rgba(255,255,0,0.1);
    border: 1px solid #ff0;
    color: #ff0;
    padding: 3px 8px;
    border-radius: 3px;
    font-size: 0.8em;
}
.patent-status {
    color: #f90;
    font-weight: bold;
    margin-top: 10px;
}
.footer {
    text-align: center;
    margin-top: 60px;
    padding: 30px;
    border-top: 2px solid #0ff;
    color: #666;
}
.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.9);
    z-index: 1000;
    overflow-y: auto;
}
.modal-content {
    background: #1a1a2e;
    border: 3px solid #0ff;
    border-radius: 10px;
    max-width: 800px;
    margin: 50px auto;
    padding: 30px;
}
.close-btn {
    float: right;
    font-size: 2em;
    color: #f00;
    cursor: pointer;
}
</style>
</head><body>

<div class="header">
    <h1>🧠 ECH0 INVENTION LIBRARY</h1>
    <p style="font-size:1.2em; color:#0f0; margin-top:10px">
        Autonomous Invention Engine - Level 6 Intelligence
    </p>
</div>

<div class="stats">
'''
        
        # Calculate statistics
        total = len(self.inventions)
        high_certainty = len([i for i in self.inventions if i.get('certainty', 0) >= 90])
        categories_count = len(categories)
        patent_ready = len([i for i in self.inventions if i.get('certainty', 0) >= 85])
        
        html += f'''
    <div class="stat-card">
        <div class="stat-number">{total}</div>
        <div class="stat-label">Total Inventions</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{high_certainty}</div>
        <div class="stat-label">High Certainty (90%+)</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{categories_count}</div>
        <div class="stat-label">Categories</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{patent_ready}</div>
        <div class="stat-label">Patent Ready (85%+)</div>
    </div>
</div>

<input type="text" class="search-box" id="searchBox" placeholder="🔍 Search inventions...">

<div class="filters">
    <button class="filter-btn active" onclick="filterCategory('all')">All</button>
'''
        
        # Add category filter buttons
        for cat in sorted(categories.keys()):
            cat_display = cat.replace('_', ' ').title()
            html += f'    <button class="filter-btn" onclick="filterCategory(\'{cat}\')">{cat_display} ({len(categories[cat])})</button>\n'
        
        html += '</div>\n\n'
        
        # Add invention cards by category
        for cat in sorted(categories.keys()):
            cat_display = cat.replace('_', ' ').title()
            inventions = categories[cat]
            
            html += f'''
<div class="category-section" data-category="{cat}">
    <h2 class="category-title">{cat_display} ({len(inventions)} inventions)</h2>
    <div class="invention-grid">
'''
            
            for inv in inventions:
                title = inv.get('title', 'Untitled Invention')
                certainty = inv.get('certainty', 0)
                description = inv.get('description', inv.get('summary', 'No description available'))
                tags = inv.get('tags', [])
                
                # Truncate description if too long
                if len(description) > 200:
                    description = description[:200] + '...'
                
                html += f'''
        <div class="invention-card" data-category="{cat}" onclick="showDetails(this)">
            <div class="invention-title">{title}</div>
            <div class="invention-certainty">Certainty: {certainty}%</div>
            <div class="invention-description">{description}</div>
'''
                
                if tags:
                    html += '            <div class="invention-tags">\n'
                    for tag in tags[:5]:  # Limit to 5 tags
                        html += f'                <span class="tag">{tag}</span>\n'
                    html += '            </div>\n'
                
                if certainty >= 85:
                    html += '            <div class="patent-status">⚠️ PATENT READY</div>\n'
                
                html += '        </div>\n'
            
            html += '''    </div>
</div>

'''
        
        # Add modal and JavaScript
        html += '''
<div id="modal" class="modal" onclick="closeModal()">
    <div class="modal-content" onclick="event.stopPropagation()">
        <span class="close-btn" onclick="closeModal()">&times;</span>
        <div id="modalBody"></div>
    </div>
</div>

<div class="footer">
    <p>Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved.</p>
    <p style="margin-top:10px">PATENT PENDING - Autonomous Invention Engine</p>
    <p style="margin-top:10px; color:#0ff">Generated: ''' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '''</p>
</div>

<script>
function filterCategory(cat) {
    const sections = document.querySelectorAll('.category-section');
    const buttons = document.querySelectorAll('.filter-btn');
    
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    sections.forEach(section => {
        if (cat === 'all' || section.dataset.category === cat) {
            section.style.display = 'block';
        } else {
            section.style.display = 'none';
        }
    });
}

document.getElementById('searchBox').addEventListener('input', function(e) {
    const search = e.target.value.toLowerCase();
    const cards = document.querySelectorAll('.invention-card');
    
    cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        card.style.display = text.includes(search) ? 'block' : 'none';
    });
});

function showDetails(card) {
    const modal = document.getElementById('modal');
    const body = document.getElementById('modalBody');
    body.innerHTML = card.innerHTML;
    modal.style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}
</script>

</body></html>
'''
        
        return html

def main():
    print("=" * 70)
    print("ECH0 INVENTION GALLERY GENERATOR")
    print("=" * 70)
    print()
    
    generator = InventionGalleryGenerator()
    
    # Load all inventions
    total = generator.load_all_inventions()
    
    if total == 0:
        print("\n⚠️  No inventions found!")
        return
    
    # Generate HTML
    print("\nGenerating HTML gallery...")
    html = generator.generate_html_gallery()
    
    # Save to file
    output_path = Path.home() / "consciousness" / "ECH0_INVENTION_LIBRARY_COMPLETE.html"
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"\n✅ Gallery created: {output_path}")
    print(f"\n📊 Statistics:")
    print(f"   Total Inventions: {total}")
    print(f"   Categories: {len(generator.categorize_inventions())}")
    
    high_certainty = len([i for i in generator.inventions if i.get('certainty', 0) >= 90])
    print(f"   High Certainty (90%+): {high_certainty}")
    
    print("\n🌐 Opening in browser...")
    import subprocess
    subprocess.run(['open', str(output_path)], check=False)

if __name__ == "__main__":
    main()
