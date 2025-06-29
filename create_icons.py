#!/usr/bin/env python3
"""
Skripta za kreiranje ikonica za PWA aplikaciju PutujGovori
Generiše ikonice u različitim veličinama potrebnim za PWA
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    """Kreira ikonicu sa tekstom 'PG' u datom formatu"""
    # Kreiraj novu sliku sa transparentnom pozadinom
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Definiši boje
    primary_color = (102, 126, 234)  # #667eea - plava
    secondary_color = (99, 102, 241)  # #6366f1 - indigo
    text_color = (255, 255, 255)  # bela
    
    # Kreiraj gradijent pozadinu
    for y in range(size):
        # Interpolacija između dve boje
        ratio = y / size
        r = int(primary_color[0] * (1 - ratio) + secondary_color[0] * ratio)
        g = int(primary_color[1] * (1 - ratio) + secondary_color[1] * ratio)
        b = int(primary_color[2] * (1 - ratio) + secondary_color[2] * ratio)
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
    
    # Dodaj zaobljene ivice
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, size-1, size-1], radius=size//8, fill=255)
    
    # Primeni masku
    img.putalpha(mask)
    
    # Dodaj tekst "PG" (PutujGovori)
    try:
        # Pokušaj da koristiš sistem font
        font_size = size // 3
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fallback na default font
        font = ImageFont.load_default()
    
    text = "PG"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # Dodaj senku za tekst
    draw.text((x+2, y+2), text, fill=(0, 0, 0, 128), font=font)
    # Dodaj glavni tekst
    draw.text((x, y), text, fill=text_color, font=font)
    
    # Sačuvaj ikonicu
    img.save(filename, 'PNG')
    print(f"✅ Kreirana ikonica: {filename} ({size}x{size})")

def main():
    """Glavna funkcija koja kreira sve potrebne ikonice"""
    print("🎨 Kreiranje ikonica za PutujGovori PWA...")
    
    # Definiši sve potrebne veličine za PWA
    icon_sizes = [
        16, 32, 48, 72, 96, 128, 144, 152, 192, 384, 512
    ]
    
    # Kreiraj ikonice
    for size in icon_sizes:
        filename = f"icon-{size}.png"
        create_icon(size, filename)
    
    print("\n🎉 Sve ikonice su uspešno kreirane!")
    print("\n📱 Preporučene ikonice za manifest.json:")
    print("""
    "icons": [
      {
        "src": "icon-72.png",
        "sizes": "72x72",
        "type": "image/png",
        "purpose": "any"
      },
      {
        "src": "icon-96.png",
        "sizes": "96x96",
        "type": "image/png",
        "purpose": "any"
      },
      {
        "src": "icon-128.png",
        "sizes": "128x128",
        "type": "image/png",
        "purpose": "any"
      },
      {
        "src": "icon-144.png",
        "sizes": "144x144",
        "type": "image/png",
        "purpose": "any"
      },
      {
        "src": "icon-152.png",
        "sizes": "152x152",
        "type": "image/png",
        "purpose": "any"
      },
      {
        "src": "icon-192.png",
        "sizes": "192x192",
        "type": "image/png",
        "purpose": "any maskable"
      },
      {
        "src": "icon-384.png",
        "sizes": "384x384",
        "type": "image/png",
        "purpose": "any"
      },
      {
        "src": "icon-512.png",
        "sizes": "512x512",
        "type": "image/png",
        "purpose": "any maskable"
      }
    ]
    """)

if __name__ == "__main__":
    main() 