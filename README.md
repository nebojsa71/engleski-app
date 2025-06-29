# Engleski za putovanja - English Learning App

Aplikacija za učenje engleskog jezika namenjena putnicima. Aplikacija je napravljena kao PWA (Progressive Web App) i radi offline.

## Funkcionalnosti

- **Tri nivoa lekcija**: Osnovni, srednji i napredni nivo
- **Lekcije**: Različite teme kao što su pozdrav, restoran, aerodrom, hotel, kupovina
- **Frazni učenje**: Svaka lekcija sadrži korisne fraze na engleskom i srpskom
- **Fonetska transkripcija**: Pomoć pri izgovoru
- **Audio reprodukcija**: Mogućnost slušanja izgovora (koristi Web Speech API)
- **Kvizovi**: Testiranje znanja sa 5 pitanja po lekciji
- **Praćenje napretka**: Vizuelni prikaz napretka kroz lekcije
- **Offline funkcionalnost**: Radi bez interneta nakon prvog učitavanja

## Nivoi lekcija

### Osnovni nivo (Beginner)
- Jednostavne fraze i osnovni vokabular
- Temeljne situacije putovanja
- 15 lekcija sa 8 fraza svaka

### Srednji nivo (Intermediate)
- Kompleksnije rečenice i gramatika
- Napredniji vokabular i situacije
- 15 lekcija sa 8 fraza svaka

### Napredni nivo (Advanced)
- Sofisticirani jezik i akademski termini
- Profesionalne i formalne situacije
- 15 lekcija sa 8 fraza svaka

## Kako koristiti

1. Otvorite `index.html` u web browseru
2. Izaberite nivo (Osnovni, Srednji, Napredni)
3. Kliknite na lekciju da je proširite
4. Pregledajte fraze i kliknite "Listen" za audio
5. Kliknite "Kviz" da testirate svoje znanje
6. Završite kviz sa 4/5 tačnih odgovora da označite lekciju kao završenu

## Instalacija kao PWA

1. Otvorite aplikaciju u Chrome/Edge
2. Kliknite na ikonu instalacije u adresnoj traci
3. Izaberite "Instaliraj aplikaciju"
4. Aplikacija će se pojaviti kao obična aplikacija

## Struktura fajlova

- `index.html` - Glavna HTML stranica
- `lessons.json` - Podaci o lekcijama osnovnog nivoa
- `lessons_intermediate.json` - Podaci o lekcijama srednjeg nivoa
- `lessons_advanced.json` - Podaci o lekcijama naprednog nivoa
- `manifest.json` - PWA manifest
- `service-worker.js` - Service worker za offline funkcionalnost
- `icon-192.png` / `icon-512.png` - Ikone za PWA

## Tehnologije

- HTML5
- CSS3
- Vanilla JavaScript
- Web Speech API
- Service Workers
- Local Storage

## Podržani browseri

- Chrome (preporučeno)
- Edge
- Firefox
- Safari (ograničena podrška za audio)

## Napomene

- Audio funkcionalnost zahteva HTTPS u produkciji
- Service worker se registruje automatski
- Podaci o napretku se čuvaju u localStorage
- Aplikacija radi offline nakon prvog učitavanja

## Razvoj

Za lokalni razvoj:
1. Klonirajte repozitorijum
2. Otvorite `index.html` u browseru
3. Za testiranje PWA funkcionalnosti, koristite lokalni server

```bash
# Koristeći Python
python -m http.server 8000

# Koristeći Node.js
npx serve .
```

## Licenca

MIT License