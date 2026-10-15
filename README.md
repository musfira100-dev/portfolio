# Portfolio — Django backend

Frontend bilkul wahi hai (design/animations same). Data ab Django database se aata hai aur **/admin/** se manage hota hai.

## Sabse tez tareeqa (dummy data ke saath ready)
`db.sqlite3` mein original wala saara dummy data pehle se bhara hua hai (profile, 4 projects, 5 services, 6 skills, 4 timeline, 1 sample message).
```bash
pip install -r requirements.txt
python manage.py runserver
```
Admin login: **admin / admin12345** — deploy se pehle password zaroor badal dein.

## Shuru se setup (agar db khali ho)
```bash
python -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_portfolio       # original demo data (optional)
python manage.py createsuperuser      # admin login banayein
python manage.py runserver
```
- Site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Admin se kya kya hota hai
| Section | Kya karein |
|---|---|
| Site profile | Naam, tagline, manifesto, email, social links, stats, coordinates |
| Projects | Add / edit / delete, image upload ya URL, order, publish on/off |
| Services | Title, description, hover image |
| Skills | Constellation nodes (level, position) |
| Timeline entries | Saal-ba-saal journey |
| Contact messages | Form se aaye messages (read-only inbox) |

## Production (deploy)
```bash
export DJANGO_DEBUG=0
export DJANGO_SECRET_KEY="lamba-random-secret"
export DJANGO_ALLOWED_HOSTS="yourdomain.com"
export DJANGO_CSRF_ORIGINS="https://yourdomain.com"
python manage.py collectstatic --noinput
gunicorn config.wsgi
```
- Uploaded images `media/` folder mein save hote hain (hosting par yeh folder persistent hona chahiye).
- Public page par "DJANGO CMS" button ko chhupana ho to `SHOW_CMS_BUTTON=0` set karein.

## Pages
| URL | Page |
|---|---|
| `/` | Landing page (saare sections ek jagah) |
| `/about/` | Manifesto |
| `/timeline/` | Timeline |
| `/skills/` | Skills (category wise) |
| `/services/` | Services |
| `/projects/` , `/projects/<id>/` | Work list aur har project ka detail page |
| `/stats/` | Numbers |
| `/contact/` | Contact form |

Landing par har section ke corner mein "FULL PAGE ↗" link hai. Alag pages ka style (paper/editorial) landing (dark/neon) se jaan-boojh kar alag hai.
Sab content admin se hi aata hai, koi naya model ya migration nahi.

## Dummy data / images
`python manage.py seed_portfolio` kisi bhi waqt chala sakte hain (duplicate nahi banata): khali jagah dummy data se bharta hai
aur Unsplash/khali images ko local images (`media/dummy/`) se badal deta hai — internet ki zaroorat nahi.
Apni images admin se upload karenge to woh dummy ki jagah le leti hain.

**Zaroori:** site hamesha `python manage.py runserver` ke zariye `http://127.0.0.1:8000/` par kholein.
`index.html` file par double-click karne se data/cursor nahi chalega (woh Django template hai).

## Landing page
`/` ka apna alag light design hai (nila-jamni-gulabi gradient, Sora font) — alag pages (beige/serif) se jaan-boojh kar alag.
Hero, marquee, About, Timeline, Skills (rings), Services, Work, Metrics, Contact + footer. Sab data admin se aata hai,
aur har section ke saath "Open page" link hai. Navbar mein "All pages" menu se saare alag pages khulte hain.

## Resume
Admin -> Site profile -> **Resume (PDF)** mein PDF upload karein. Navbar (landing aur alag pages) mein "Resume" button khud aa jata hai.
PDF na ho to button nahi dikhta.

## Social links
Admin -> Site profile -> Contact & social: GitHub, LinkedIn, Facebook, Instagram, X. Khali field ka button nahi dikhta.
