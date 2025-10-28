#!/usr/bin/env python3
"""
Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved. PATENT PENDING.

Create Focused Invention Galleries:
1. Aerogel/Daylight Hologram Inventions
2. Top High-Certainty Inventions
"""

import json
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

def create_aerogel_gallery(inventions):
    """Create gallery for aerogel/daylight projection inventions"""
    
    # Filter aerogel/hologram inventions
    aerogel_inventions = [
        inv for inv in inventions
        if any(keyword in str(inv).lower() for keyword in [
            'aerogel', 'hologram', 'daylight', 'projection', 'volumetric', 
            '3d display', 'holographic', 'transparent display'
        ])
    ]
    
    html = '''<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<title>ECH0 Aerogel & Daylight Hologram Inventions</title>
<style>
body {
    font-family: 'Courier New', monospace;
    background: linear-gradient(135deg, #0a0015 0%, #1a0030 100%);
    color: #0ff;
    padding: 20px;
    margin: 0;
}
.header {
    text-align: center;
    padding: 40px;
    background: rgba(0,255,255,0.1);
    border: 3px solid #0ff;
    border-radius: 15px;
    margin-bottom: 40px;
}
.header h1 {
    font-size: 3em;
    color: #0ff;
    text-shadow: 0 0 30px #0ff;
    margin-bottom: 15px;
}
.header p {
    font-size: 1.3em;
    color: #0f0;
}
.invention-showcase {
    display: grid;
    gap: 30px;
    margin: 30px 0;
}
.invention-full {
    background: rgba(0,255,255,0.05);
    border: 3px solid #0ff;
    border-radius: 15px;
    padding: 30px;
    transition: all 0.3s;
}
.invention-full:hover {
    box-shadow: 0 0 40px rgba(0,255,255,0.5);
    transform: scale(1.02);
}
.inv-title {
    font-size: 2em;
    color: #0f0;
    margin-bottom: 20px;
    font-weight: bold;
    text-shadow: 0 0 10px #0f0;
}
.inv-certainty {
    display: inline-block;
    background: rgba(0,255,0,0.3);
    color: #0f0;
    padding: 10px 20px;
    border-radius: 10px;
    font-size: 1.3em;
    font-weight: bold;
    margin-bottom: 20px;
}
.inv-description {
    color: #aaa;
    font-size: 1.1em;
    line-height: 1.8;
    margin: 20px 0;
}
.inv-details {
    background: rgba(0,0,0,0.3);
    border-left: 4px solid #0ff;
    padding: 20px;
    margin: 20px 0;
}
.detail-section {
    margin: 15px 0;
}
.detail-label {
    color: #0ff;
    font-weight: bold;
    margin-bottom: 5px;
}
.detail-content {
    color: #ccc;
    padding-left: 20px;
}
.patent-badge {
    background: linear-gradient(135deg, #ff6600 0%, #ff0000 100%);
    color: #fff;
    padding: 15px 25px;
    border-radius: 10px;
    font-weight: bold;
    display: inline-block;
    margin-top: 20px;
    box-shadow: 0 0 20px rgba(255,100,0,0.5);
}
.stats-bar {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
    margin: 30px 0;
}
.stat-box {
    background: rgba(0,255,255,0.1);
    border: 2px solid #0ff;
    padding: 15px;
    text-align: center;
    border-radius: 10px;
}
.stat-num {
    font-size: 2em;
    color: #0f0;
    font-weight: bold;
}
.stat-label {
    color: #0ff;
    margin-top: 5px;
}
</style>
</head><body>

<div class="header">
    <h1>🌟 AEROGEL & DAYLIGHT HOLOGRAM INVENTIONS</h1>
    <p>ECH0's Breakthrough Display Technologies</p>
</div>

<div class="stats-bar">
    <div class="stat-box">
        <div class="stat-num">''' + str(len(aerogel_inventions)) + '''</div>
        <div class="stat-label">Total Inventions</div>
    </div>
    <div class="stat-box">
        <div class="stat-num">''' + str(len([i for i in aerogel_inventions if i.get('certainty', 0) >= 90])) + '''</div>
        <div class="stat-label">High Certainty (90%+)</div>
    </div>
    <div class="stat-box">
        <div class="stat-num">''' + str(len([i for i in aerogel_inventions if i.get('certainty', 0) >= 85])) + '''</div>
        <div class="stat-label">Patent Ready</div>
    </div>
</div>

<div class="invention-showcase">
'''
    
    # Add each invention
    for inv in aerogel_inventions:
        title = inv.get('title', 'Untitled Invention')
        certainty = inv.get('certainty', 0)
        description = inv.get('description', inv.get('summary', 'No description'))
        
        html += f'''
    <div class="invention-full">
        <div class="inv-title">{title}</div>
        <div class="inv-certainty">Certainty: {certainty}%</div>
        <div class="inv-description">{description}</div>
        
        <div class="inv-details">
'''
        
        # Add any additional details
        if 'technical_approach' in inv:
            html += f'''
            <div class="detail-section">
                <div class="detail-label">Technical Approach:</div>
                <div class="detail-content">{inv['technical_approach']}</div>
            </div>
'''
        
        if 'applications' in inv:
            apps = inv['applications'] if isinstance(inv['applications'], str) else ', '.join(inv['applications'])
            html += f'''
            <div class="detail-section">
                <div class="detail-label">Applications:</div>
                <div class="detail-content">{apps}</div>
            </div>
'''
        
        if 'innovation_type' in inv:
            html += f'''
            <div class="detail-section">
                <div class="detail-label">Innovation Type:</div>
                <div class="detail-content">{inv['innovation_type']}</div>
            </div>
'''
        
        html += '''
        </div>
'''
        
        if certainty >= 85:
            html += '''
        <div class="patent-badge">⚠️ PATENT READY - PROTECTED INNOVATION</div>
'''
        
        html += '''
    </div>
'''
    
    html += '''
</div>

<div style="text-align:center; margin-top:60px; padding:30px; border-top:2px solid #0ff;">
    <p>Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved.</p>
    <p style="margin-top:10px">PATENT PENDING</p>
    <p style="margin-top:10px; color:#666">Generated: ''' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '''</p>
</div>

</body></html>
'''
    
    return html, len(aerogel_inventions)

def create_top_inventions_gallery(inventions):
    """Create gallery for top high-certainty inventions"""
    
    # Get top inventions by certainty
    sorted_invs = sorted(inventions, key=lambda x: x.get('certainty', 0), reverse=True)
    top_inventions = sorted_invs[:50]  # Top 50
    
    html = '''<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<title>ECH0 Top 50 Inventions</title>
<style>
body {
    font-family: 'Courier New', monospace;
    background: linear-gradient(135deg, #000000 0%, #1a0000 100%);
    color: #f90;
    padding: 20px;
    margin: 0;
}
.header {
    text-align: center;
    padding: 40px;
    background: rgba(255,153,0,0.1);
    border: 3px solid #f90;
    border-radius: 15px;
    margin-bottom: 40px;
}
.header h1 {
    font-size: 3em;
    color: #f90;
    text-shadow: 0 0 30px #f90;
}
.podium {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin: 40px 0;
}
.podium-card {
    background: rgba(255,153,0,0.1);
    border: 3px solid #f90;
    border-radius: 15px;
    padding: 30px;
    text-align: center;
    position: relative;
}
.rank {
    font-size: 4em;
    color: #gold;
    font-weight: bold;
}
.gold { color: #FFD700; }
.silver { color: #C0C0C0; }
.bronze { color: #CD7F32; }
.invention-list {
    display: grid;
    gap: 20px;
    margin: 30px 0;
}
.invention-item {
    background: rgba(255,153,0,0.05);
    border: 2px solid #f90;
    border-radius: 10px;
    padding: 20px;
    display: grid;
    grid-template-columns: 60px 1fr;
    gap: 20px;
    align-items: center;
}
.rank-number {
    font-size: 2.5em;
    color: #f90;
    font-weight: bold;
    text-align: center;
}
.inv-content h3 {
    color: #0f0;
    font-size: 1.4em;
    margin-bottom: 10px;
}
.inv-meta {
    display: flex;
    gap: 15px;
    margin: 10px 0;
}
.meta-badge {
    background: rgba(255,153,0,0.2);
    padding: 5px 10px;
    border-radius: 5px;
    font-size: 0.9em;
}
</style>
</head><body>

<div class="header">
    <h1>🏆 TOP 50 ECH0 INVENTIONS</h1>
    <p style="font-size:1.3em; color:#0f0;">Highest Certainty Innovations</p>
</div>

<div class="podium">
'''
    
    # Top 3 podium
    for i, inv in enumerate(top_inventions[:3]):
        rank_class = ['gold', 'silver', 'bronze'][i]
        rank_icon = ['🥇', '🥈', '🥉'][i]
        
        html += f'''
    <div class="podium-card">
        <div class="rank {rank_class}">{rank_icon}</div>
        <h3 style="color:#0f0; margin:20px 0;">{inv.get('title', 'Untitled')}</h3>
        <div style="font-size:2em; color:#f90; font-weight:bold;">{inv.get('certainty', 0)}%</div>
        <p style="color:#aaa; margin-top:15px;">{inv.get('description', '')[:150]}...</p>
    </div>
'''
    
    html += '''
</div>

<h2 style="color:#f90; border-bottom:3px solid #f90; padding-bottom:10px; margin:40px 0 20px 0;">
    Complete Top 50 Rankings
</h2>

<div class="invention-list">
'''
    
    # Rest of top 50
    for i, inv in enumerate(top_inventions, 1):
        html += f'''
    <div class="invention-item">
        <div class="rank-number">#{i}</div>
        <div class="inv-content">
            <h3>{inv.get('title', 'Untitled Invention')}</h3>
            <div class="inv-meta">
                <span class="meta-badge">Certainty: {inv.get('certainty', 0)}%</span>
                <span class="meta-badge">Category: {inv.get('category', 'General').replace('_', ' ').title()}</span>
            </div>
            <p style="color:#aaa;">{inv.get('description', inv.get('summary', 'No description'))[:200]}</p>
        </div>
    </div>
'''
    
    html += '''
</div>

<div style="text-align:center; margin-top:60px; padding:30px; border-top:2px solid #f90;">
    <p>Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved.</p>
    <p style="margin-top:10px">PATENT PENDING</p>
    <p style="margin-top:10px; color:#666">Generated: ''' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '''</p>
</div>

</body></html>
'''
    
    return html, len(top_inventions)

def main():
    print("=" * 70)
    print("CREATING FOCUSED INVENTION GALLERIES")
    print("=" * 70)
    print()
    
    # Load inventions
    print("Loading inventions...")
    inventions = load_inventions()
    print(f"✓ Loaded {len(inventions)} total inventions\n")
    
    # Create aerogel gallery
    print("Creating Aerogel & Hologram Gallery...")
    aerogel_html, aerogel_count = create_aerogel_gallery(inventions)
    aerogel_path = Path.home() / "consciousness" / "AEROGEL_HOLOGRAM_INVENTIONS.html"
    with open(aerogel_path, 'w') as f:
        f.write(aerogel_html)
    print(f"✅ Created: {aerogel_path}")
    print(f"   Inventions: {aerogel_count}\n")
    
    # Create top inventions gallery
    print("Creating Top 50 Inventions Gallery...")
    top_html, top_count = create_top_inventions_gallery(inventions)
    top_path = Path.home() / "consciousness" / "TOP_50_INVENTIONS.html"
    with open(top_path, 'w') as f:
        f.write(top_html)
    print(f"✅ Created: {top_path}")
    print(f"   Inventions: {top_count}\n")
    
    print("=" * 70)
    print("✅ ALL GALLERIES CREATED")
    print("=" * 70)
    print()
    print("Opening galleries...")
    
    # Open galleries
    import subprocess
    subprocess.run(['open', str(aerogel_path)], check=False)
    subprocess.run(['open', str(top_path)], check=False)

if __name__ == "__main__":
    main()
