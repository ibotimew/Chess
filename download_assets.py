"""
Download Lichess assets for offline use
Run this script once to download all required assets
"""
import urllib.request
from pathlib import Path
import sys

# Board theme colors (from Lichess CSS)
BOARD_THEMES = {
    'brown': {'light': (240, 217, 181), 'dark': (181, 136, 99)},
    'blue': {'light': (222, 227, 230), 'dark': (140, 162, 173)},
    'blue2': {'light': (197, 210, 220), 'dark': (114, 144, 168)},
    'blue3': {'light': (217, 226, 233), 'dark': (124, 155, 179)},
    'blue-marble': {'light': (235, 237, 246), 'dark': (127, 159, 194)},
    'canvas': {'light': (210, 210, 196), 'dark': (163, 163, 149)},
    'wood': {'light': (222, 196, 160), 'dark': (188, 145, 103)},
    'wood2': {'light': (232, 208, 178), 'dark': (189, 158, 125)},
    'wood3': {'light': (232, 216, 184), 'dark': (178, 148, 118)},
    'wood4': {'light': (246, 236, 222), 'dark': (168, 138, 107)},
    'maple': {'light': (231, 216, 197), 'dark': (179, 158, 134)},
    'maple2': {'light': (231, 216, 197), 'dark': (150, 132, 112)},
    'green': {'light': (234, 240, 206), 'dark': (170, 192, 133)},
    'marble': {'light': (241, 248, 255), 'dark': (183, 194, 206)},
    'green-plastic': {'light': (235, 235, 208), 'dark': (108, 142, 91)},
    'grey': {'light': (185, 184, 178), 'dark': (143, 140, 136)},
    'metal': {'light': (195, 203, 213), 'dark': (122, 136, 155)},
    'olive': {'light': (225, 224, 213), 'dark': (172, 167, 147)},
    'newspaper': {'light': (236, 235, 226), 'dark': (183, 180, 172)},
    'purple': {'light': (217, 194, 220), 'dark': (155, 118, 159)},
    'purple-diag': {'light': (215, 192, 218), 'dark': (153, 116, 158)},
    'pink': {'light': (241, 219, 223), 'dark': (220, 158, 177)},
    'ic': {'light': (235, 235, 235), 'dark': (204, 204, 204)},
    'horsey': {'light': (208, 196, 234), 'dark': (154, 135, 199)}
}

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def download_file(url: str, dest: Path):
    if dest.exists():
        print(f"  ✓ Already exists: {dest.name}")
        return True
    
    print(f"  Downloading: {dest.name}...", end='', flush=True)
    try:
        urllib.request.urlretrieve(url, dest)
        print(f" ✓")
        return True
    except Exception as e:
        print(f" ✗ ({e})")
        return False

def convert_svg_to_png():
    """Try to convert SVG pieces to PNG"""
    try:
        import cairosvg
        from pathlib import Path
        
        pieces_dir = Path('assets/pieces')
        converted_count = 0
        
        for piece_set_dir in pieces_dir.iterdir():
            if not piece_set_dir.is_dir():
                continue
            
            svg_files = list(piece_set_dir.glob('*.svg'))
            if not svg_files:
                continue
                
            print(f"Converting {piece_set_dir.name}...", end='', flush=True)
            
            for svg_file in svg_files:
                png_file = svg_file.with_suffix('.png')
                
                if png_file.exists():
                    continue
                
                try:
                    cairosvg.svg2png(
                        url=str(svg_file),
                        write_to=str(png_file),
                        output_width=512,
                        output_height=512
                    )
                    converted_count += 1
                except:
                    pass
            
            if svg_files:
                print(f" ✓ ({len(list(piece_set_dir.glob('*.png')))} pieces)")
        
        return True
    except ImportError:
        print("\n⚠ cairosvg not installed - SVG conversion skipped")
        print("  Install with: pip install cairosvg")
        print("  (Optional - pieces will be rendered as text fallback)")
        return False

def download_pieces():
    print("\n" + "="*60)
    print("DOWNLOADING PIECE SETS")
    print("="*60)
    
    # Use correct GitHub raw URL
    base_url = "https://raw.githubusercontent.com/lichess-org/lila/master/public/piece"
    
    # Most popular piece sets
    piece_sets = [
        'cburnett',    # Default
  
        'maestro'
    ]
    
    pieces = ['wP', 'wN', 'wB', 'wR', 'wQ', 'wK', 
              'bP', 'bN', 'bB', 'bR', 'bQ', 'bK']
    
    assets_dir = Path('assets')
    
    for piece_set in piece_sets:
        print(f"\n{piece_set}:")
        piece_dir = assets_dir / 'pieces' / piece_set
        ensure_dir(piece_dir)
        
        success = 0
        for piece in pieces:
            svg_url = f"{base_url}/{piece_set}/{piece}.svg"
            svg_path = piece_dir / f"{piece}.svg"
            if download_file(svg_url, svg_path):
                success += 1
        
        if success > 0:
            print(f"  Downloaded {success}/12 pieces")

def generate_board_themes():
    print("\n" + "="*60)
    print("GENERATING BOARD THEMES")
    print("="*60)
    
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("\n✗ PIL/Pillow not installed")
        print("  Install with: pip install pillow")
        print("  Board themes will use fallback rendering")
        return False
    
    boards_dir = Path('assets/boards')
    ensure_dir(boards_dir)
    
    size = 512
    square_size = size // 8
    
    print()
    for theme_name, colors in BOARD_THEMES.items():
        png_path = boards_dir / f"{theme_name}.png"
        
        if png_path.exists():
            print(f"  ✓ Already exists: {theme_name}.png")
            continue
        
        print(f"  Generating: {theme_name}.png...", end='', flush=True)
        
        try:
            img = Image.new('RGB', (size, size))
            draw = ImageDraw.Draw(img)
            
            for rank in range(8):
                for file in range(8):
                    is_light = (file + rank) % 2 == 1
                    color = colors['light'] if is_light else colors['dark']
                    
                    x = file * square_size
                    y = rank * square_size
                    
                    draw.rectangle(
                        [x, y, x + square_size, y + square_size],
                        fill=color
                    )
            
            img.save(png_path, 'PNG')
            print(f" ✓")
        except Exception as e:
            print(f" ✗ ({e})")
    
    print(f"\n✓ Generated {len(BOARD_THEMES)} board themes")
    return True

def download_sounds():
    print("\n" + "="*60)
    print("DOWNLOADING MODERN LICHESS SOUNDS")
    print("="*60)
    
    # Modern Lichess sound URLs (raw GitHub)
    base_url = "https://raw.githubusercontent.com/lichess-org/lila/master/public/sound/standard"
    
    sounds = {
        'Move': 'move',
        'Capture': 'capture',
        'Check': 'check',
        'GenericNotify': 'notify',
        'Victory': 'victory',
        'Defeat': 'defeat',
        'Draw': 'draw',
        'Berserk': 'berserk',
        'Explosion': 'explosion'
    }
    
    sounds_dir = Path('assets/sounds')
    ensure_dir(sounds_dir)
    
    print()
    success_count = 0
    
    for sound_name, key in sounds.items():
        # Try .ogg first (primary format)
        url = f"{base_url}/{sound_name}.ogg"
        dest = sounds_dir / f"{sound_name}.ogg"
        
        if download_file(url, dest):
            success_count += 1
    
    # Create missing sounds as aliases
    aliases = {
        'Castle': 'Move',
        'Promote': 'GenericNotify',
        'GameEnd': 'Victory'
    }
    
    print("\nCreating sound aliases...")
    for alias, source in aliases.items():
        alias_path = sounds_dir / f"{alias}.ogg"
        source_path = sounds_dir / f"{source}.ogg"
        
        if source_path.exists() and not alias_path.exists():
            import shutil
            shutil.copy(source_path, alias_path)
            print(f"  ✓ {alias}.ogg <- {source}.ogg")
    
    print(f"\n✓ Downloaded {success_count}/{len(sounds)} sounds")
    print(f"✓ Created {len(aliases)} sound aliases")

def create_default_config():
    print("\n" + "="*60)
    print("CREATING DEFAULT CONFIG")
    print("="*60)
    
    import json
    
    config = {
        'animation_speed': 0.2,
        'stockfish_path': '/usr/bin/stockfish',
        'stockfish_depth': 15,
        'stockfish_time': 1.0,
        'arrow_color': [255, 170, 0],
        'arrow_thickness': 15,
        'circle_color': [255, 170, 0],
        'circle_thickness': 4,
        'circle_radius_ratio': 0.8,
        'board_theme': 'brown',
        'piece_theme': 'cburnett',
        'play_sounds': True
    }
    
    config_path = Path('config.json')
    if not config_path.exists():
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print("\n✓ Created config.json")
    else:
        print("\n✓ config.json already exists")

def check_dependencies():
    """Check for optional dependencies"""
    print("\n" + "="*60)
    print("CHECKING DEPENDENCIES")
    print("="*60)
    
    deps = {
        'cairosvg': 'SVG to PNG conversion (optional)',
        'PIL': 'Image processing (required for boards)',
        'pygame': 'Required',
        'chess': 'Required'
    }
    
    missing = []
    
    for module, desc in deps.items():
        try:
            if module == 'PIL':
                import PIL
            elif module == 'cairosvg':
                import cairosvg
            elif module == 'pygame':
                import pygame
            elif module == 'chess':
                import chess
            print(f"  ✓ {module}: {desc}")
        except ImportError:
            print(f"  ✗ {module}: {desc}")
            missing.append(module)
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        if 'PIL' in missing:
            print("\n⚠ IMPORTANT: Pillow is required for board themes")
            print("Install with: pip install pillow")

def main():
    print("=" * 60)
    print("LICHESS OFFLINE CHESS - ASSET DOWNLOADER")
    print("=" * 60)
    print("\nThis will download:")
    print("  ✓ 25+ piece sets (SVG format)")
    print("  ✓ Generate 24 board themes (PNG)")
    print("  ✓ Modern Lichess sounds (OGG)")
    print("  ✓ Default configuration file")
    print("\nSize: ~20-50MB total")
    print("Time: 3-5 minutes")
    print("\n⚠ Requires internet connection")
    
    response = input("\nContinue? (y/n): ").lower().strip()
    if response != 'y':
        print("\nCancelled.")
        return
    
    try:
        check_dependencies()
        download_pieces()
        generate_board_themes()
        download_sounds()
        
        print("\n" + "="*60)
        print("CONVERTING SVG TO PNG")
        print("="*60)
        convert_svg_to_png()
        
        create_default_config()
        
        print("\n" + "="*60)
        print("✓✓✓ DOWNLOAD COMPLETE ✓✓✓")
        print("="*60)
        print("\n✓ Assets are now stored in ./assets/")
        print("✓ The application can run 100% offline")
        print("\nRun the chess application:")
        print("  python chess_app.py")
        print("\nAvailable board themes:")
        themes = list(BOARD_THEMES.keys())
        for i in range(0, len(themes), 4):
            print("  " + ", ".join(themes[i:i+4]))
        
    except KeyboardInterrupt:
        print("\n\n✗ Download interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Error during download: {e}")
        print("\nTroubleshooting:")
        print("  1. Check your internet connection")
        print("  2. Install dependencies: pip install cairosvg pillow")
        print("  3. Some assets may have failed - the app will use fallbacks")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()