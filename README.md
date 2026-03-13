# Pan Babula – Soundboard 🍺

Interaktivní soundboard s legendárními hláškami Pana Babuly ze seriálu **Hospoda** (Česká televize).

**[babula.cz](https://babula.cz)**

## Co to je

Webová stránka, kde si kliknutím na dlaždici přehrajete ikonické hlášky Pana Babuly. Každou hlášku lze sdílet přímým odkazem. Stránka funguje i offline jako nainstalovaná aplikace (PWA).

## Funkce

- Přehrávání hlášek kliknutím na dlaždice
- Sdílení jednotlivých hlášek přes URL (`?play=009`)
- Zvuková vizualizace (waveform animace) při přehrávání
- Instalace jako aplikace na iOS, Android i desktop (PWA)
- Offline podpora díky Service Workeru
- Responzivní grid (4 sloupce → 2 na mobilu)
- Plynulé animace při načtení a scrollování
- Odpočítávání do dalšího přidání nových hlášek (live countdown)

## Technologie

- **Vanilla HTML/CSS/JS** – žádný framework, žádný build step
- **GitHub Pages** – hosting a automatický deploy
- **PWA** – manifest + Service Worker pro offline a instalaci
- **Google Fonts** – Space Mono, Syne
- **Google Analytics** – sledování návštěvnosti (GA4)

## Struktura projektu

```
├── index.html              # Celá aplikace (HTML + CSS + JS)
├── Audio_files/             # 107 MP3 hlášek
├── sw.js                    # Service Worker (offline)
├── manifest.json            # PWA manifest
├── icon.svg                 # Ikona aplikace
├── babula.jpg               # Hlavní obrázek
├── qr_platba.png            # QR kód pro platbu
├── CNAME                    # Vlastní doména (babula.cz)
├── Nazvy_hlasek.md          # Přehled hlášek a jejich názvů
└── .github/
    ├── workflows/
    │   ├── static.yml       # Deploy na GitHub Pages (push → main)
    │   └── add-quotes.yml   # Automatické přidávání hlášek (cron)
    └── scripts/
        └── add_quotes.py    # Skript pro přidání nových hlášek
```

## Automatické přidávání hlášek

Každé 3 dny GitHub Actions automaticky přidá 4 nové hlášky ze složky `Audio_files/` na web:

1. Skript `.github/scripts/add_quotes.py` najde hlášky, které ještě nejsou na webu
2. Přidá další 4 do pole `sounds` v `index.html`
3. Název na dlaždici odvodí z názvu souboru
4. Commitne a pushne → automaticky se spustí deploy

Workflow lze spustit i ručně přes záložku **Actions** na GitHubu.

## Přidání hlášky ručně

1. Nahraj MP3 do `Audio_files/` ve formátu `XXX_nazevbezdiakritikyamezer.mp3`
2. Přidej záznam do pole `sounds` v `index.html`:
   ```js
   { num: 'XXX', file: 'Audio_files/XXX_nazev.mp3', icon: '🍺', label: 'Název', color: 'var(--c1)' }
   ```
3. Zapiš hlášku do `Nazvy_hlasek.md`
4. Pushni na `main` – deploy proběhne automaticky

## Lokální spuštění

Stačí otevřít `index.html` v prohlížeči, nebo spustit lokální server:

```bash
python3 -m http.server 8000
```

a přejít na `http://localhost:8000`.

## Licence

Autorská práva k seriálu Hospoda patří České televizi. Tato stránka je vytvořena z lásky k seriálu a nemá komerční účel.

---

Vytvořil [Michal Prouza](https://buymeacoffee.com/michalp)
