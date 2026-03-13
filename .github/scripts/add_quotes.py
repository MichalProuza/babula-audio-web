#!/usr/bin/env python3
"""
Automaticky přidá 4 nové hlášky ze složky Audio_files/ na web.
Spouští se jako GitHub Actions cron job každých 72 hodin.
"""

import os
import re
import sys

REPO_ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
INDEX_PATH = os.path.join(REPO_ROOT, 'index.html')
AUDIO_DIR = os.path.join(REPO_ROOT, 'Audio_files')
TRACKING_PATH = os.path.join(REPO_ROOT, 'Nazvy_hlasek.md')

BATCH_SIZE = 4

# Emoji pool – cyklicky se přiřazují novým hláškám
EMOJI_POOL = [
    '🍺', '🍻', '😂', '🤣', '😎', '🥴', '🫡', '🤷',
    '💪', '🫣', '😡', '🤔', '🫠', '🤙', '👀', '🙃',
]

# 16 barev z CSS
COLORS = [f'var(--c{i})' for i in range(1, 17)]


def get_audio_files():
    """Vrátí seřazený seznam všech MP3 souborů ve složce Audio_files."""
    files = []
    for f in os.listdir(AUDIO_DIR):
        if f.lower().endswith('.mp3') and re.match(r'^\d{3}_', f):
            files.append(f)
    return sorted(files)


def get_existing_nums(html):
    """Vytáhne čísla hlášek, které už jsou v sounds poli."""
    nums = set()
    for m in re.finditer(r"num:\s*'(\d{3})'", html):
        nums.add(m.group(1))
    return nums


def label_from_filename(filename):
    """Odvodí zobrazovaný název z názvu souboru.

    Příklad: '033_hovado.mp3' → 'Hovado'
             '042_30piv.mp3'  → '30piv'
    """
    # Odstraní číslo a příponu
    name = re.sub(r'^\d{3}_', '', filename)
    name = re.sub(r'\.mp3$', '', name, flags=re.IGNORECASE)
    # První písmeno velké
    if name and name[0].isalpha():
        name = name[0].upper() + name[1:]
    return name


def build_entry(num, filename, index_in_batch):
    """Vytvoří řádek pro sounds pole."""
    label = label_from_filename(filename)
    icon = EMOJI_POOL[int(num) % len(EMOJI_POOL)]
    color = COLORS[int(num) % len(COLORS)]
    file_path = f'Audio_files/{filename}'
    return (
        f"  {{ num: '{num}', file: '{file_path}',"
        f" icon: '{icon}', label: '{label}',"
        f" color: '{color}' }}"
    )


def update_index_html(html, new_entries):
    """Vloží nové záznamy na začátek sounds pole."""
    marker = 'const sounds = [\n'
    pos = html.find(marker)
    if pos == -1:
        print('ERROR: Nenalezeno pole "const sounds" v index.html', file=sys.stderr)
        sys.exit(1)

    insert_pos = pos + len(marker)
    lines = ',\n'.join(new_entries) + ',\n'
    return html[:insert_pos] + lines + html[insert_pos:]


def update_tracking_md(md_content, entries_info):
    """Přidá nové hlášky do sekce 'Aktuálně na webu' v Nazvy_hlasek.md."""
    rows = ''
    for num, filename, label in entries_info:
        rows += f'| {num} | {label} | `{filename}` |\n'

    # Vloží před řádek "---" který odděluje sekce (druhý výskyt ---)
    parts = md_content.split('\n---\n')
    if len(parts) >= 2:
        # Přidá na konec první tabulky (před druhý ---)
        parts[1] = rows + '\n---\n' + parts[2] if len(parts) > 2 else rows
        # Znovu sestav
        result = parts[0] + '\n' + rows + '\n---\n'
        if len(parts) > 2:
            result += '\n'.join(parts[2:])
        else:
            result += parts[1]

    # Jednodušší přístup: vlož řádky před "## Čekají na doplnění"
    marker = '## Čekají na doplnění na web'
    idx = md_content.find(marker)
    if idx == -1:
        return md_content + '\n' + rows

    # Najdi konec tabulky (poslední řádek s |) před markerem
    before = md_content[:idx]
    after = md_content[idx:]
    return before.rstrip() + '\n' + rows + '\n---\n\n' + after


def main():
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    existing = get_existing_nums(html)
    all_files = get_audio_files()

    # Najdi soubory, které ještě nejsou na webu
    candidates = []
    for filename in all_files:
        num = filename[:3]
        if num not in existing:
            candidates.append((num, filename))

    if not candidates:
        print('Všechny hlášky už jsou na webu. Nic k přidání.')
        sys.exit(0)

    # Vyber první BATCH_SIZE
    to_add = candidates[:BATCH_SIZE]
    print(f'Přidávám {len(to_add)} nových hlášek:')

    new_entries = []
    entries_info = []
    for i, (num, filename) in enumerate(to_add):
        label = label_from_filename(filename)
        entry = build_entry(num, filename, i)
        new_entries.append(entry)
        entries_info.append((num, filename, label))
        print(f'  {num} - {label} ({filename})')

    # Aktualizuj index.html
    updated_html = update_index_html(html, new_entries)
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(updated_html)
    print('index.html aktualizován.')

    # Aktualizuj Nazvy_hlasek.md
    with open(TRACKING_PATH, 'r', encoding='utf-8') as f:
        md = f.read()
    updated_md = update_tracking_md(md, entries_info)
    with open(TRACKING_PATH, 'w', encoding='utf-8') as f:
        f.write(updated_md)
    print('Nazvy_hlasek.md aktualizován.')

    # Zbývající hlášky po přidání
    remaining = len(candidates) - len(to_add)
    print(f'Zbývá {remaining} hlášek ve frontě.')

    # Zapiš počet přidaných a zbývajících pro GitHub Actions output
    github_output = os.environ.get('GITHUB_OUTPUT', '')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f'added_count={len(to_add)}\n')
            f.write(f'remaining_count={remaining}\n')


if __name__ == '__main__':
    main()
