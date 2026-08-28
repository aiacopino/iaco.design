import pandas as pd
from datetime import datetime, timezone
import urllib.parse

# UI Translations Dictionary
translations = {
    'en': {
        'LANG_CODE': 'en',
        'TAGLINE': 'fine art studio zurich',
        'UNIQUE_TITLE': 'Original Works',
        'PRINTS_TITLE': 'Archival Prints',
        'ABOUT_TEXT': 'Taking the time to appreciate the small hidden wonders of nature has always brought me a sense of peace and gratefulness for the beauty around us. My work grows out of that: Close observation of structures the world offers abundantly, composed in symmetrical and sometimes unexpected ways. What I hope to pass on, along with each piece, is a little of that same stillness. A reminder to slow down and notice.',
        'INQUIRY_TITLE': 'Studio Inquiries',
        'INQUIRY_SUBTEXT': 'For custom commissions, collaborations, or general questions.',
        'INQUIRY_BTN': 'Contact the Studio',
        'LANG_TOGGLE_URL': 'index-de.html',
        'LANG_TOGGLE_TEXT': 'DE'
    },
    'de': {
        'LANG_CODE': 'de',
        'TAGLINE': 'fine art studio zürich',
        'UNIQUE_TITLE': 'Originalwerke',
        'PRINTS_TITLE': 'Kunstdrucke',
        'ABOUT_TEXT': 'Schon immer schöpfe ich viel Ruhe und Dankbarkeit aus der Natur um mich herum. Meine Arbeit widmet sich dem Beobachten manchmal verborgener, manchmal offensichtlicher Muster und Strukturen, sowie der Wiedergabe und Neukombination ihrer Symmetrien. Was ich mit jedem Stück weitergeben möchte, ist ein wenig von dieser Stille. Eine Erinnerung, innezuhalten und genau hinzusehen.',
        'INQUIRY_TITLE': 'Studio Anfragen',
        'INQUIRY_SUBTEXT': 'Für individuelle Aufträge, Kooperationen oder allgemeine Fragen.',
        'INQUIRY_BTN': 'Studio Kontaktieren',
        'LANG_TOGGLE_URL': 'index.html',
        'LANG_TOGGLE_TEXT': 'EN'
    }
}

def generate_mailto(title, price):
    subject = urllib.parse.quote(f"Purchase Inquiry: {title}")
    body = urllib.parse.quote(f"Hello,\n\nI would like to inquire about purchasing '{title}' ({price}).\n\nPlease let me know the next steps.")
    return f"mailto:studio@iacopino.ch?subject={subject}&body={body}"

def generate_grid_html(df_filtered):
    grid_html = ""
    for _, row in df_filtered.iterrows():
        status = str(row['status']).strip()
        is_sold = status.upper() == 'SOLD'
        
        button_html = '<span class="btn sold">SOLD</span>' if is_sold else f'<a href="{generate_mailto(row["title"], status)}" class="btn">Inquire / {status}</a>'

        grid_html += f"""
        <article class="card">
            <div class="card-inner">
                <div class="card-front">
                    <img src="assets/{row['filename']}" alt="Artwork: {row['title']}" loading="lazy">
                </div>
                <div class="card-back">
                    <h3>{row['title']}</h3>
                    <p>{row['date']}</p>
                    <p>{row['size']}</p>
                    <p>{row['medium']}</p>
                    <div class="status">{button_html}</div>
                </div>
            </div>
        </article>
        """
    return grid_html

def build_site():
    df = pd.read_csv('inventory.csv').fillna('')
    
    # Split dataframe by category
    df_unique = df[df['category'].str.lower() == 'unique']
    df_prints = df[df['category'].str.lower() == 'print']

    # Generate the grid HTML strings
    unique_html = generate_grid_html(df_unique)
    prints_html = generate_grid_html(df_prints)

    with open('template.html', 'r', encoding='utf-8') as file:
        template = file.read()

    timestamp = datetime.now(timezone.utc).strftime("BUILD DEPLOYMENT: %Y-%m-%d %H:%M:%S UTC")

    # Generate a file for each language
    for lang, strings in translations.items():
        output_html = template.replace('{{GALLERY_GRID_UNIQUE}}', unique_html)
        output_html = output_html.replace('{{GALLERY_GRID_PRINTS}}', prints_html)
        output_html = output_html.replace('<!-- {{BUILD_TIMESTAMP}} -->', f'<!-- {timestamp} -->')
        
        # Inject UI translations
        for key, value in strings.items():
            output_html = output_html.replace(f'{{{{{key}}}}}', value)

        filename = 'index.html' if lang == 'en' else f'index-{lang}.html'
        
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(output_html)
            
    print("Static build complete. English and German files generated.")

if __name__ == "__main__":
    build_site()