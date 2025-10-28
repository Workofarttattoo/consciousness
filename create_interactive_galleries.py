#!/usr/bin/env python3
"""
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

Create Interactive Invention Galleries with Clickable POC/Files
"""

import json
import os
from pathlib import Path
from datetime import datetime

def load_inventions():
    """Load all inventions"""
    inventions = []
    sources = [
        Path.home() / "consciousness" / "ech0_inventions.jsonl",
        Path.home() / "consciousness" / "ech0_invention_ideas.jsonl",
        Path.home() / "consciousness" / "ech0_theme_park_inventions.jsonl"
    ]
    
    for source in sources:
        if source.exists():
            with open(source) as f:
                for line in f:
                    if line.strip():
                        try:
                            inventions.append(json.loads(line))
                        except:
                            pass
    
    return inventions

def check_invention_files(inv_id):
    """Check what files exist for an invention"""
    files_dir = Path.home() / "consciousness" / "ech0_inventions"
    files = {
        'poc': None,
        'schematic': None,
        'bom': None,
        'patent': None,
        'report': None
    }
    
    if not files_dir.exists():
        return files
    
    # Search for files matching the invention ID
    for category_dir in files_dir.iterdir():
        if category_dir.is_dir():
            for file in category_dir.glob(f"*{inv_id}*"):
                name = file.name.lower()
                if 'poc' in name or 'proof' in name:
                    files['poc'] = file
                elif 'schematic' in name or 'diagram' in name:
                    files['schematic'] = file
                elif 'bom' in name or 'materials' in name:
                    files['bom'] = file
                elif 'patent' in name:
                    files['patent'] = file
                elif 'report' in name or 'full' in name:
                    files['report'] = file
    
    return files

def create_interactive_html(inventions, title, filename, filter_func=None):
    """Create interactive HTML with file links"""
    
    if filter_func:
        filtered = filter_func(inventions)
    else:
        filtered = inventions
    
    html = f'''<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: 'Courier New', monospace;
    background: linear-gradient(135deg, #000 0%, #1a1a2e 100%);
    color: #0ff;
    padding: 20px;
}}
.header {{
    text-align: center;
    padding: 40px;
    background: rgba(0,255,255,0.1);
    border: 3px solid #0ff;
    border-radius: 15px;
    margin-bottom: 40px;
}}
.header h1 {{
    font-size: 3em;
    color: #0ff;
    text-shadow: 0 0 30px #0ff;
    margin-bottom: 15px;
}}
.stats {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 15px;
    margin: 30px 0;
}}
.stat-card {{
    background: rgba(0,255,255,0.05);
    border: 2px solid #0ff;
    padding: 20px;
    text-align: center;
    border-radius: 10px;
}}
.stat-num {{ font-size: 2.5em; color: #0f0; font-weight: bold; }}
.stat-label {{ color: #0ff; margin-top: 10px; }}
.invention-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 25px;
    margin: 30px 0;
}}
.invention-card {{
    background: rgba(0,255,255,0.05);
    border: 2px solid #0ff;
    border-radius: 12px;
    padding: 25px;
    transition: all 0.3s;
}}
.invention-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0,255,255,0.3);
    border-color: #0f0;
}}
.inv-title {{
    font-size: 1.4em;
    color: #0f0;
    margin-bottom: 15px;
    font-weight: bold;
    cursor: pointer;
}}
.inv-title:hover {{ text-shadow: 0 0 10px #0f0; }}
.inv-certainty {{
    display: inline-block;
    background: rgba(0,255,0,0.2);
    color: #0f0;
    padding: 8px 15px;
    border-radius: 8px;
    margin: 10px 0;
    font-weight: bold;
}}
.inv-description {{
    color: #aaa;
    line-height: 1.7;
    margin: 15px 0;
    max-height: 100px;
    overflow: hidden;
}}
.file-buttons {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 20px;
}}
.file-btn {{
    background: linear-gradient(135deg, #0ff 0%, #00aaff 100%);
    color: #000;
    border: none;
    padding: 10px 15px;
    border-radius: 6px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s;
    font-size: 0.9em;
}}
.file-btn:hover {{
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(0,255,255,0.6);
}}
.file-btn.patent {{
    background: linear-gradient(135deg, #ff6600 0%, #ff0000 100%);
    color: #fff;
}}
.file-btn.poc {{
    background: linear-gradient(135deg, #0f0 0%, #00aa00 100%);
}}
.file-btn.schematic {{
    background: linear-gradient(135deg, #ff0 0%, #ffaa00 100%);
}}
.expand-btn {{
    background: rgba(0,255,255,0.2);
    color: #0ff;
    border: 2px solid #0ff;
    padding: 8px 15px;
    border-radius: 6px;
    cursor: pointer;
    margin-top: 15px;
    font-weight: bold;
}}
.expand-btn:hover {{
    background: #0ff;
    color: #000;
}}
.modal {{
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.95);
    z-index: 1000;
    overflow-y: auto;
    padding: 40px;
}}
.modal-content {{
    background: #1a1a2e;
    border: 3px solid #0ff;
    border-radius: 15px;
    max-width: 900px;
    margin: 0 auto;
    padding: 40px;
    position: relative;
}}
.close-modal {{
    position: absolute;
    top: 20px;
    right: 30px;
    font-size: 3em;
    color: #f00;
    cursor: pointer;
    line-height: 1;
}}
.close-modal:hover {{ color: #ff0; }}
.modal-title {{
    font-size: 2.5em;
    color: #0f0;
    margin-bottom: 20px;
}}
.modal-section {{
    margin: 25px 0;
    padding: 20px;
    background: rgba(0,0,0,0.3);
    border-left: 4px solid #0ff;
}}
.section-title {{
    color: #0ff;
    font-size: 1.3em;
    margin-bottom: 15px;
    font-weight: bold;
}}
</style>
</head><body>

<div class="header">
    <h1>{title}</h1>
    <p style="font-size:1.2em; color:#0f0;">Interactive Invention Browser with POC Files</p>
</div>

<div class="stats">
    <div class="stat-card">
        <div class="stat-num">{len(filtered)}</div>
        <div class="stat-label">Total Inventions</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">{len([i for i in filtered if i.get('certainty', 0) >= 90])}</div>
        <div class="stat-label">High Certainty (90%+)</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">{len([i for i in filtered if i.get('certainty', 0) >= 85])}</div>
        <div class="stat-label">Patent Ready</div>
    </div>
</div>

<div class="invention-grid">
'''
    
    for inv in filtered[:100]:  # Limit to first 100 for performance
        inv_id = inv.get('id', 'unknown')
        title_text = inv.get('title', inv.get('name', 'Untitled Invention'))
        certainty = inv.get('certainty', 0)
        description = inv.get('description', inv.get('summary', 'No description'))
        
        # Truncate description
        if len(description) > 150:
            description = description[:150] + '...'
        
        # Check for files
        files = check_invention_files(inv_id)
        
        html += f'''
    <div class="invention-card">
        <div class="inv-title" onclick="showModal('{inv_id}')">{title_text}</div>
        <div class="inv-certainty">Certainty: {certainty}%</div>
        <div class="inv-description">{description}</div>
        
        <div class="file-buttons">
'''
        
        # Add file buttons if files exist
        if files['poc']:
            html += f'''
            <button class="file-btn poc" onclick="openFile('{files["poc"]}')">📄 View POC</button>
'''
        if files['schematic']:
            html += f'''
            <button class="file-btn schematic" onclick="openFile('{files["schematic"]}')">📐 Schematic</button>
'''
        if files['bom']:
            html += f'''
            <button class="file-btn" onclick="openFile('{files["bom"]}')">📋 BOM</button>
'''
        if files['patent']:
            html += f'''
            <button class="file-btn patent" onclick="openFile('{files["patent"]}')">⚠️ Patent</button>
'''
        
        # Always add view details button
        html += f'''
            <button class="expand-btn" onclick="showModal('{inv_id}')">📖 Full Details</button>
        </div>
    </div>
'''
    
    html += '''
</div>

<div id="modal" class="modal" onclick="closeModal()">
    <div class="modal-content" onclick="event.stopPropagation()">
        <span class="close-modal" onclick="closeModal()">&times;</span>
        <div id="modalBody"></div>
    </div>
</div>

<div style="text-align:center; margin-top:60px; padding:30px; border-top:2px solid #0ff;">
    <p>Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved.</p>
    <p style="margin-top:10px">PATENT PENDING</p>
    <p style="margin-top:10px; color:#666">Generated: ''' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '''</p>
</div>

<script>
const inventions = ''' + json.dumps(filtered, indent=2) + ''';

function showModal(invId) {
    const inv = inventions.find(i => i.id === invId);
    if (!inv) return;
    
    const modal = document.getElementById('modal');
    const body = document.getElementById('modalBody');
    
    let html = '<div class="modal-title">' + (inv.title || inv.name) + '</div>';
    html += '<div class="modal-section">';
    html += '<div class="section-title">Certainty</div>';
    html += '<div style="font-size:2em; color:#0f0;">' + (inv.certainty || 0) + '%</div>';
    html += '</div>';
    
    if (inv.description || inv.summary) {
        html += '<div class="modal-section">';
        html += '<div class="section-title">Description</div>';
        html += '<p style="color:#ccc; line-height:1.8;">' + (inv.description || inv.summary) + '</p>';
        html += '</div>';
    }
    
    if (inv.key_features) {
        html += '<div class="modal-section">';
        html += '<div class="section-title">Key Features</div>';
        html += '<ul style="color:#ccc; line-height:1.8; padding-left:20px;">';
        inv.key_features.forEach(f => html += '<li>' + f + '</li>');
        html += '</ul></div>';
    }
    
    if (inv.technical_approach) {
        html += '<div class="modal-section">';
        html += '<div class="section-title">Technical Approach</div>';
        html += '<p style="color:#ccc; line-height:1.8;">' + inv.technical_approach + '</p>';
        html += '</div>';
    }
    
    body.innerHTML = html;
    modal.style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

function openFile(path) {
    window.open('file://' + path, '_blank');
}
</script>

</body></html>
'''
    
    return html

def main():
    print("=" * 70)
    print("CREATING INTERACTIVE INVENTION GALLERIES")
    print("=" * 70)
    print()
    
    # Load inventions
    print("Loading inventions...")
    inventions = load_inventions()
    print(f"✓ Loaded {len(inventions)} total inventions\n")
    
    # Create Complete Library
    print("1. Creating Complete Interactive Library...")
    complete_html = create_interactive_html(
        inventions,
        "🧠 ECH0 Complete Invention Library",
        "ECH0_INTERACTIVE_LIBRARY.html"
    )
    path1 = Path.home() / "consciousness" / "ECH0_INTERACTIVE_LIBRARY.html"
    with open(path1, 'w') as f:
        f.write(complete_html)
    print(f"   ✅ {path1}\n")
    
    # Create Aerogel/Hologram Gallery
    print("2. Creating Aerogel & Hologram Gallery...")
    aerogel_html = create_interactive_html(
        inventions,
        "🌟 Aerogel & Daylight Hologram Inventions",
        "AEROGEL_INTERACTIVE.html",
        filter_func=lambda invs: [
            i for i in invs
            if any(k in str(i).lower() for k in [
                'aerogel', 'hologram', 'daylight', 'projection', 'volumetric'
            ])
        ]
    )
    path2 = Path.home() / "consciousness" / "AEROGEL_INTERACTIVE.html"
    with open(path2, 'w') as f:
        f.write(aerogel_html)
    print(f"   ✅ {path2}\n")
    
    # Create Top 50
    print("3. Creating Top 50 Gallery...")
    top_html = create_interactive_html(
        sorted(inventions, key=lambda x: x.get('certainty', 0), reverse=True)[:50],
        "🏆 Top 50 ECH0 Inventions",
        "TOP_50_INTERACTIVE.html"
    )
    path3 = Path.home() / "consciousness" / "TOP_50_INTERACTIVE.html"
    with open(path3, 'w') as f:
        f.write(top_html)
    print(f"   ✅ {path3}\n")
    
    print("=" * 70)
    print("✅ ALL INTERACTIVE GALLERIES CREATED")
    print("=" * 70)
    print()
    print("Opening galleries...")
    
    import subprocess
    subprocess.run(['open', str(path1)], check=False)
    subprocess.run(['open', str(path2)], check=False)
    subprocess.run(['open', str(path3)], check=False)

if __name__ == "__main__":
    main()
