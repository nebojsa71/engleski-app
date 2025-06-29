#!/usr/bin/env python3
import json

encodings = ['utf-8', 'utf-16', 'cp1252', 'iso-8859-1']

for encoding in encodings:
    try:
        beginner = json.load(open('lessons.json', 'r', encoding=encoding))
        intermediate = json.load(open('lessons_intermediate.json', 'r', encoding=encoding))
        advanced = json.load(open('lessons_advanced.json', 'r', encoding=encoding))
        
        print(f"✅ Uspešno sa encoding: {encoding}")
        print(f"Beginner: {len(beginner)} lekcija")
        print(f"Intermediate: {len(intermediate)} lekcija")
        print(f"Advanced: {len(advanced)} lekcija")
        print(f"Ukupno: {len(beginner) + len(intermediate) + len(advanced)} lekcija")
        break
        
    except Exception as e:
        print(f"❌ Greška sa {encoding}: {e}")
        continue 