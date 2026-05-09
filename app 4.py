"""
İyi ki varsın Anne ❤️  –  Eslem için
Uraz Efe & Ahmet, 2026

• Kullanıcı görünümü: Temiz, hiçbir düzenleme butonu yok
• Admin paneli: En alttaki 🔐 tuşuna bas → şifre gir → paneller açılır
• Kalıcı depolama: data/ klasörü (sayfa yenilenince kaybolmaz)

Kurulum:  pip install streamlit Pillow
Çalıştır: streamlit run app.py
"""

import streamlit as st
import json, shutil, uuid, base64, random
from pathlib import Path

# ── Admin şifresi (değiştirilebilir) ─────────────────────────────────────────
ADMIN_PASSWORD = "eslem2026"

# ── Disk depolama ─────────────────────────────────────────────────────────────
BASE_DIR  = Path(__file__).parent / "data"
META_FILE = BASE_DIR / "meta.json"
MEDIA_DIR = BASE_DIR / "media"
BASE_DIR.mkdir(exist_ok=True)
MEDIA_DIR.mkdir(exist_ok=True)

# ── Varsayılan içerik ─────────────────────────────────────────────────────────
DEFAULT = {
    # ─ Genel metinler
    "hero_eyebrow":    "Anneler Günü · 2026",
    "hero_title":      "İyi ki\nvarsın\nAnne ❤️",
    "hero_subtitle":   "Bugün sana küçük ama özel bir sürpriz hazırladık.\nUraz Efe ve Ahmet'ten, sana…",
    "hero_img":        None,

    "letter_date":     "Mayıs 2026",
    "letter_body":     "Ben henüz tam konuşamıyorum ama sana her gün teşekkür etmek istiyorum.\n\nBeni sabırla uyuttuğun,\nbeni güldürdüğün,\nhasta olduğumda hiç ayrılmadığın,\nve bana sevginin ne olduğunu gösterdiğin için teşekkür ederim.\n\nDünyaya gözlerimi ilk açtığımda ilk gördüğüm sendin.\nVe o andan beri sen benim her şeyimsin.\n\nSeni çok seviyorum.",
    "letter_sign":     "Uraz Efe",

    "memories_title":  "Birlikte yazdığımız\nen güzel sayfalar",
    "moments_title":   "İyi günler, kötü günler,\nhepsi bizim",
    "videos_title":    "Küçük mutluluğumuzun\nen tatlı halleri",
    "music_title":     "Bizim\nşarkımız",
    "music_subtitle":  "Her ailenin kendine ait bir melodisi vardır.\nBu bizimki. Her çalanda içimiz ısınır.",
    "music_file":      None,

    "finale_pre_title": "Hazır mısın,\nEslem?",
    "finale_img":      None,
    "finale_message":  "Bazı insanlar anne olur.\nSen bizim yuvamız oldun.\n\nHer sabah uyanışımız, her gülüşümüz,\nher küçük anımız — hepsi seninle anlam kazandı.",
    "finale_sign":     "Seni çok seviyoruz ❤️\nUraz Efe & Ahmet",

    "footer_quote":    "\"Dünyanın tüm çiçeklerini toplasam, senin bir gülüşüne değişmem anne.\"",

    # ─ Listeler
    "memories": [
        {"id":"m1","num":"01","date":"Ekim 2024",  "title":"Uraz Efe Doğdu",        "desc":"Küçük ellerin ilk kez senin parmağını tuttuğu an — dünyanın durduğu an.","img":None},
        {"id":"m2","num":"02","date":"Kasım 2024", "title":"İlk Aile Fotoğrafımız","desc":"Üçümüz, bir çatı altında, yeni bir hikâyenin başında.","img":None},
        {"id":"m3","num":"03","date":"Şubat 2025", "title":"İlk Tatilimiz",         "desc":"Deniz kokusu, bebek sesi ve senin gülüşün. Mükemmel bir tablo.","img":None},
        {"id":"m4","num":"04","date":"Mart 2025",  "title":"İlk Kahkahamız",        "desc":"Uraz Efe ilk kez güldüğünde sen de güldün. O ses hâlâ kulaklarımızda.","img":None},
    ],
    "moments": [
        {"id":"mo1","icon":"🤒","category":"Hastalık Anları",    "date":"Aralık 2024","title":"İlk Ateşimiz",             "story":"Üç gündü hiç inmiyordu. Sen hiç ayrılmadın başından. Sabahın dördünde alnıma koyduğun ıslak bezi unutmadım.","img":None,"video":None},
        {"id":"mo2","icon":"🍼","category":"Beslenme Keyifleri", "date":"Kasım 2024","title":"İlk Mama Macerası",         "story":"Yüzüme sürdüm, saçıma bulaştırdım, sana da fırlattım. Sen sadece güldün. O gülüş her şeye değdi.","img":None,"video":None},
        {"id":"mo3","icon":"🐛","category":"Emekleme",           "date":"Ocak 2025", "title":"İlk Emekleme Adımlarım",   "story":"Önce diz çöküp ilerlemeye çalıştım. Nereye gidersem gitsin, sen oradaydın. Her zaman.","img":None,"video":None},
        {"id":"mo4","icon":"👣","category":"Yürüme",             "date":"Mart 2025", "title":"Ayağa Kalktım",            "story":"Sallandım, senin kollarına düştüm. Dünyayı fethettim sanki. Sen zaten oradaydın — her zaman olduğun gibi.","img":None,"video":None},
        {"id":"mo5","icon":"😄","category":"İyi Günler",         "date":"Nisan 2025","title":"Güneşli Bir Pazar Sabahı", "story":"Üçümüz birlikte uyandık. Pencereden güneş süzülüyordu. Hiçbir şey olmadı ama her şey mükemmeldi.","img":None,"video":None},
        {"id":"mo6","icon":"🌧","category":"Kötü Günler",        "date":"Şubat 2025","title":"Uykusuz Geceler",          "story":"Bazen ikimiz de ağlıyorduk. Ama sen hiç bırakmadın. Sabah olunca gülümsüyordun — bu cesaret nereden geliyordu?","img":None,"video":None},
    ],
    "videos": [
        {"id":"v1","label":"Uraz Efe'nin İlk Sesi",  "file":None},
        {"id":"v2","label":"Birlikte Uyuyan Anımız", "file":None},
        {"id":"v3","label":"Parkta Bir Sabah",       "file":None},
    ],
}

# ── Meta yardımcılar ──────────────────────────────────────────────────────────
def load_meta():
    if META_FILE.exists():
        try:
            stored = json.loads(META_FILE.read_text(encoding="utf-8"))
            for k, v in DEFAULT.items():
                if k not in stored:
                    stored[k] = v
            return stored
        except Exception:
            pass
    return json.loads(json.dumps(DEFAULT))

def save_meta(d):
    META_FILE.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

def save_uploaded(f, sub=""):
    d = MEDIA_DIR / sub if sub else MEDIA_DIR
    d.mkdir(exist_ok=True)
    ext   = Path(f.name).suffix.lower()
    fname = f"{uuid.uuid4().hex}{ext}"
    p     = d / fname
    p.write_bytes(f.getbuffer())
    return str(p.relative_to(BASE_DIR))

def abs_path(rel):
    return str(BASE_DIR / rel) if rel else None

def to_data_url(rel):
    p = Path(abs_path(rel)) if rel else None
    if not p or not p.exists(): return None
    ext  = p.suffix.lower().lstrip(".")
    mime = {"jpg":"image/jpeg","jpeg":"image/jpeg","png":"image/png","gif":"image/gif",
            "webp":"image/webp","mp4":"video/mp4","mov":"video/mp4",
            "mp3":"audio/mpeg","wav":"audio/wav","ogg":"audio/ogg","m4a":"audio/mp4"
            }.get(ext, "application/octet-stream")
    b64 = base64.b64encode(p.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"

def del_file(rel):
    if rel:
        p = BASE_DIR / rel
        if p.exists(): p.unlink()

def clear_all():
    if MEDIA_DIR.exists(): shutil.rmtree(MEDIA_DIR)
    MEDIA_DIR.mkdir(exist_ok=True)
    if META_FILE.exists(): META_FILE.unlink()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="İyi ki varsın Anne ❤️", page_icon="❤️",
                   layout="wide", initial_sidebar_state="collapsed")

# ── Session defaults ──────────────────────────────────────────────────────────
ss = st.session_state
for k, v in [("admin",False),("show_pw",False),("pw_input",""),
             ("show_surprise",False),("show_confetti",False),
             ("confirm_del",False)]:
    if k not in ss: ss[k] = v

D    = load_meta()
EDIT = ss["admin"]

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Sans:wght@300;400;500&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,[data-testid="stAppViewContainer"]{
  background:#fdf8f4!important;color:#2a1f1a!important;
  font-family:'DM Sans',sans-serif!important}
[data-testid="stHeader"],[data-testid="stToolbar"],footer{display:none!important}
[data-testid="stAppViewContainer"]>.main>div{padding:0!important;max-width:100%!important}
.block-container{padding:0!important;max-width:100%!important}
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-thumb{background:#e8b4b8;border-radius:2px}

/* ── ADMIN BAR ── */
.admin-bar{position:fixed;top:0;left:0;right:0;z-index:9998;
  background:rgba(22,12,10,0.97);backdrop-filter:blur(16px);
  border-bottom:1px solid rgba(201,84,106,0.4);
  display:flex;align-items:center;gap:16px;padding:10px 28px}
.admin-bar-title{font-size:11px;letter-spacing:3.5px;text-transform:uppercase;
  color:rgba(201,84,106,0.9);flex:1}
.admin-badge{background:rgba(201,84,106,0.15);border:1px solid rgba(201,84,106,0.35);
  color:#e8687e;font-size:10px;letter-spacing:2px;padding:3px 10px;border-radius:2px}
.admin-pad{height:56px}

/* ── HERO ── */
.hero-wrap{position:relative;width:100%;min-height:100vh;
  background:linear-gradient(135deg,#fff9f5 0%,#fdeef0 40%,#f9e8ee 100%);
  display:flex;align-items:center;overflow:hidden}
.hero-blob{position:absolute;border-radius:50%;
  background:radial-gradient(circle,rgba(237,176,185,0.18) 0%,transparent 70%)}
.hero-content{position:relative;z-index:2;max-width:640px;padding:80px 6vw;
  animation:fadeUp 1.2s cubic-bezier(.22,1,.36,1) both}
.hero-eyebrow{font-size:12px;letter-spacing:3px;text-transform:uppercase;color:#c97f8a;margin-bottom:20px}
.hero-title{font-family:'Cormorant Garamond',serif;font-size:clamp(52px,8vw,96px);
  font-weight:300;line-height:1.05;color:#1e1210;margin-bottom:28px}
.hero-title em{color:#c9546a;font-style:italic}
.hero-sub{font-size:16px;font-weight:300;color:#7a5a52;line-height:1.7;max-width:420px}
.hero-img-side{position:absolute;right:0;top:0;bottom:0;width:52%;overflow:hidden}
.hero-img-side img{width:100%;height:100%;object-fit:cover;filter:brightness(.95) saturate(.9)}
.hero-ph{width:100%;height:100%;background:linear-gradient(160deg,#f0d8dd,#e8c8ce,#dbb5bc);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px}
.hero-ph span{font-size:48px;opacity:.35}
.hero-ph p{font-size:12px;color:#9a6872;letter-spacing:1.5px;text-transform:uppercase}

/* ── DIVIDER ── */
.div{width:100%;height:1px;background:linear-gradient(90deg,transparent,rgba(201,84,106,0.18),transparent)}

/* ── LETTER ── */
.letter-section{background:#fff;padding:100px 6vw}
.letter-label{font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#c97f8a;
  margin-bottom:40px;display:flex;align-items:center;gap:16px}
.letter-label::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(201,127,138,.3),transparent)}
.letter-card{max-width:680px;margin:0 auto;background:#fffcf9;
  border:1px solid rgba(201,127,138,.12);border-radius:4px;padding:64px 72px;
  position:relative;box-shadow:0 8px 48px rgba(180,100,110,.06)}
.letter-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,#e8b4b8,#c9546a,#e8b4b8)}
.letter-date{font-size:12px;color:#b8897e;letter-spacing:1px;margin-bottom:32px}
.letter-salutation{font-family:'Cormorant Garamond',serif;font-size:28px;
  font-style:italic;color:#2a1f1a;margin-bottom:24px}
.letter-body{font-family:'Cormorant Garamond',serif;font-size:20px;font-weight:300;line-height:2;color:#4a3830}
.letter-body p{margin-bottom:16px}
.letter-sign{margin-top:40px;font-family:'Cormorant Garamond',serif;font-size:22px;font-style:italic;color:#c9546a}
.letter-heart{display:inline-block;animation:pulse 1.8s ease-in-out infinite}

/* ── SECTION HEADER ── */
.sec-label{font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#c97f8a;margin-bottom:16px}
.sec-title{font-family:'Cormorant Garamond',serif;font-size:clamp(34px,5vw,58px);
  font-weight:300;color:#1e1210;line-height:1.1;margin-bottom:48px}

/* ── MEMORY CARDS ── */
.tl-section{background:#fdf8f4;padding:100px 6vw}
.t-card{background:#fff;border-radius:3px;overflow:hidden;
  border:1px solid rgba(201,127,138,.1);
  transition:transform .4s cubic-bezier(.22,1,.36,1),box-shadow .4s;
  animation:fadeUp .8s cubic-bezier(.22,1,.36,1) both}
.t-card:hover{transform:translateY(-6px);box-shadow:0 20px 60px rgba(180,100,110,.12)}
.t-card-img{width:100%;height:200px;overflow:hidden;position:relative}
.t-card-img img{width:100%;height:100%;object-fit:cover}
.t-card-ph{width:100%;height:100%;background:linear-gradient(160deg,#f5e0e4,#ead0d5);
  display:flex;align-items:center;justify-content:center;font-size:32px;color:rgba(180,100,110,.3)}
.t-card-num{position:absolute;top:12px;left:12px;background:rgba(255,255,255,.9);
  border-radius:50%;width:30px;height:30px;display:flex;align-items:center;justify-content:center;
  font-size:12px;font-weight:500;color:#c9546a}
.t-card-body{padding:28px}
.t-card-date{font-size:11px;letter-spacing:2px;color:#c97f8a;margin-bottom:8px}
.t-card-title{font-family:'Cormorant Garamond',serif;font-size:22px;color:#2a1f1a;margin-bottom:10px}
.t-card-desc{font-size:14px;color:#7a5a52;line-height:1.6;font-weight:300}

/* ── MOMENTS ── */
.mo-section{background:#fff;padding:100px 6vw}
.mo-card{background:#fffcf9;border:1px solid rgba(201,127,138,.1);border-radius:4px;
  padding:44px;margin-bottom:32px;position:relative;transition:box-shadow .3s}
.mo-card:hover{box-shadow:0 12px 48px rgba(180,100,110,.07)}
.mo-card::before{content:'';position:absolute;top:0;left:0;bottom:0;width:3px;
  background:linear-gradient(180deg,#e8b4b8,#c9546a)}
.mo-icon{font-size:30px;margin-bottom:14px;display:block}
.mo-cat{font-size:10px;letter-spacing:3px;text-transform:uppercase;color:#c97f8a;margin-bottom:6px}
.mo-title{font-family:'Cormorant Garamond',serif;font-size:28px;font-weight:400;color:#2a1f1a;margin-bottom:10px}
.mo-date{font-size:11px;color:#b8897e;letter-spacing:1px;margin-bottom:18px}
.mo-story{font-family:'Cormorant Garamond',serif;font-size:19px;font-weight:300;line-height:2;color:#4a3830}
.mo-media{margin-top:24px;border-radius:3px;overflow:hidden}
.mo-media img{width:100%;max-height:460px;object-fit:cover;border-radius:3px}

/* ── VIDEO ── */
.vid-section{background:#1e1210;padding:100px 6vw}
.vid-ph{aspect-ratio:16/9;background:#2e1f1a;border-radius:3px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;
  border:1px solid rgba(201,84,106,.15)}
.play-btn{width:56px;height:56px;border:1.5px solid rgba(201,84,106,.5);border-radius:50%;
  display:flex;align-items:center;justify-content:center;font-size:18px;color:#c9546a}
.vid-lbl{font-size:13px;color:rgba(255,245,240,.45);letter-spacing:1px}

/* ── MUSIC ── */
.mu-section{background:#fdf8f4;padding:100px 6vw;display:flex;align-items:center;gap:80px;flex-wrap:wrap}
.mu-text{flex:1;min-width:280px}
.mu-player{flex:0 0 360px;min-width:280px}
.player-card{background:#fff;border:1px solid rgba(201,127,138,.15);border-radius:4px;
  padding:40px;text-align:center;box-shadow:0 4px 24px rgba(180,100,110,.06)}
.player-thumb{width:120px;height:120px;border-radius:50%;
  background:linear-gradient(135deg,#f0d8dd,#e8c0c8);
  margin:0 auto 28px;display:flex;align-items:center;justify-content:center;font-size:36px}
.player-song{font-family:'Cormorant Garamond',serif;font-size:22px;color:#2a1f1a;margin-bottom:4px}
.player-artist{font-size:13px;color:#9a7a72;margin-bottom:20px}

/* ── FINALE ── */
.fin-section{background:linear-gradient(160deg,#1e1210,#2e1a18,#1e1210);
  padding:120px 6vw;text-align:center;position:relative;overflow:hidden}
.fin-bg{position:absolute;inset:0;
  background:radial-gradient(ellipse at 50% 50%,rgba(201,84,106,.1) 0%,transparent 70%);pointer-events:none}
.fin-label{color:rgba(201,84,106,.7);font-size:11px;letter-spacing:4px;text-transform:uppercase;margin-bottom:32px}
.fin-title{font-family:'Cormorant Garamond',serif;font-size:clamp(40px,6vw,72px);
  font-weight:300;color:#fff5f0;line-height:1.2;margin-bottom:48px}
.surp-box{animation:fadeUp .8s cubic-bezier(.22,1,.36,1) both}
.surp-img{width:280px;height:280px;border-radius:50%;object-fit:cover;
  margin:0 auto 48px;display:block;
  border:3px solid rgba(201,84,106,.3);box-shadow:0 0 60px rgba(201,84,106,.2)}
.surp-ph{width:280px;height:280px;border-radius:50%;
  background:linear-gradient(135deg,#3a2520,#2e1a18);border:1px solid rgba(201,84,106,.2);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  margin:0 auto 48px;font-size:40px;gap:12px}
.surp-msg{font-family:'Cormorant Garamond',serif;font-size:clamp(22px,3vw,34px);
  font-weight:300;color:#fff5f0;line-height:1.8;max-width:560px;margin:0 auto 16px}
.surp-sign{font-family:'Cormorant Garamond',serif;font-size:20px;font-style:italic;color:#c9546a;margin-top:24px}

/* ── FOOTER ── */
.footer{background:#1e1210;padding:60px 6vw;text-align:center;border-top:1px solid rgba(201,84,106,.08)}
.footer-q{font-family:'Cormorant Garamond',serif;font-size:clamp(16px,2.5vw,22px);
  font-weight:300;font-style:italic;color:rgba(255,245,240,.35);max-width:600px;margin:0 auto;line-height:1.8}

/* ── LOCK BTN ── */
.lock-wrap{display:flex;justify-content:center;padding:32px 0 48px}
.lock-btn-style{background:transparent!important;border:1px solid rgba(150,130,120,0.2)!important;
  color:rgba(150,130,120,0.4)!important;font-size:11px!important;
  letter-spacing:2px!important;padding:6px 18px!important;border-radius:2px!important}

/* ── ADMIN PANEL ── */
.admin-section{background:#faf4f0;border-top:1px solid rgba(201,127,138,.15);padding:48px 6vw}
.admin-title{font-family:'Cormorant Garamond',serif;font-size:28px;font-weight:300;
  color:#2a1f1a;margin-bottom:32px;border-bottom:1px solid rgba(201,127,138,.15);padding-bottom:16px}

/* ── CONFETTI ── */
.cf-wrap{position:fixed;inset:0;pointer-events:none;z-index:9999;overflow:hidden}
.cp{position:absolute;top:-10px;animation:fall linear forwards}
@keyframes fall{to{transform:translateY(110vh) rotate(720deg);opacity:0}}
@keyframes fadeUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.15)}}

[data-testid="stFileUploader"]{padding:0!important}
[data-testid="stFileUploader"] section{padding:8px!important;border-radius:4px!important;
  background:rgba(253,248,244,0.6)!important;border-color:rgba(201,127,138,0.25)!important}

@media(max-width:768px){
  .hero-img-side{display:none}
  .letter-card{padding:40px 28px}
  .mu-section{flex-direction:column;gap:40px}
  .mu-player{flex:1;width:100%}
}
</style>
""", unsafe_allow_html=True)

# ── Admin bar (fixed, sadece admin modunda) ───────────────────────────────────
if EDIT:
    st.markdown("""
    <div class="admin-bar">
      <span class="admin-bar-title">⚙️ Admin Modu Açık</span>
      <span class="admin-badge">DÜZENLEME AKTİF</span>
    </div>
    <div class="admin-pad"></div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Yardımcı: çok satırlı metni HTML <br> ile göster
def nl2br(t): return t.replace("\n","<br>")
# Yardımcı: başlıktaki son kelimeyi italik yap
def styled_title(t):
    lines = t.strip().split("\n")
    if not lines: return t
    last = lines[-1]
    # Son satırdaki ❤️ ve kelimeler için italic span
    lines[-1] = f'<em>{last}</em>'
    return "<br>".join(lines)

# ─────────────────────────────────────────────────────────────────────────────
# 1. HERO
# ─────────────────────────────────────────────────────────────────────────────
hero_url = to_data_url(D["hero_img"])
hero_lines = D["hero_title"].strip().split("\n")
hero_html_title = "<br>".join(
    [f'<em>{l}</em>' if i == len(hero_lines)-1 else l for i, l in enumerate(hero_lines)]
)

st.markdown(f"""
<section class="hero-wrap">
  <div class="hero-blob" style="width:700px;height:700px;top:-200px;right:-100px"></div>
  <div class="hero-blob" style="width:400px;height:400px;bottom:-100px;left:-80px"></div>
  <div class="hero-content">
    <p class="hero-eyebrow">{D['hero_eyebrow']}</p>
    <h1 class="hero-title">{hero_html_title}</h1>
    <p class="hero-sub">{nl2br(D['hero_subtitle'])}</p>
  </div>
  <div class="hero-img-side">
    {'<img src="'+hero_url+'">' if hero_url else '<div class="hero-ph"><span>📸</span><p>Aile Fotoğrafı</p></div>'}
  </div>
</section>
<div class="div"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 2. MEKTUP
# ─────────────────────────────────────────────────────────────────────────────
letter_paras = "".join(f"<p>{nl2br(p.strip())}</p>" for p in D["letter_body"].split("\n\n") if p.strip())

st.markdown(f"""
<section class="letter-section">
  <div class="letter-label">Uraz Efe'den Mektup</div>
  <div class="letter-card">
    <p class="letter-date">{D['letter_date']}</p>
    <p class="letter-salutation">Merhaba anne,</p>
    <div class="letter-body">{letter_paras}</div>
    <div class="letter-sign">{D['letter_sign']} <span class="letter-heart">❤️</span></div>
  </div>
</section>
<div class="div"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 3. ANI KARTLARI
# ─────────────────────────────────────────────────────────────────────────────
mem_title_lines = D["memories_title"].strip().split("\n")
mem_title_html  = "<br>".join(mem_title_lines)

st.markdown(f"""
<section class="tl-section">
  <p class="sec-label">Anılarımız</p>
  <h2 class="sec-title">{mem_title_html}</h2>
""", unsafe_allow_html=True)

cols = st.columns(max(len(D["memories"]),1), gap="medium")
for i, mem in enumerate(D["memories"]):
    img_url = to_data_url(mem["img"])
    img_html = f'<img src="{img_url}">' if img_url else '<div class="t-card-ph">📸</div>'
    with cols[i % len(cols)]:
        st.markdown(f"""
        <div class="t-card" style="animation-delay:{i*0.12}s">
          <div class="t-card-img">{img_html}<div class="t-card-num">{mem['num']}</div></div>
          <div class="t-card-body">
            <p class="t-card-date">{mem['date']}</p>
            <h3 class="t-card-title">{mem['title']}</h3>
            <p class="t-card-desc">{mem['desc']}</p>
          </div>
        </div>""", unsafe_allow_html=True)

st.markdown("</section><div class='div'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 4. BÜYÜME ANLARI
# ─────────────────────────────────────────────────────────────────────────────
mo_title_lines = D["moments_title"].strip().split("\n")
mo_title_html  = "<br>".join(mo_title_lines)

st.markdown(f"""
<section class="mo-section">
  <p class="sec-label">Büyüme Yolculuğu</p>
  <h2 class="sec-title">{mo_title_html}</h2>
""", unsafe_allow_html=True)

for mo in D["moments"]:
    img_url = to_data_url(mo["img"])
    img_block = f'<div class="mo-media"><img src="{img_url}"></div>' if img_url else ""
    st.markdown(f"""
    <div class="mo-card">
      <span class="mo-icon">{mo['icon']}</span>
      <p class="mo-cat">{mo['category']}</p>
      <h3 class="mo-title">{mo['title']}</h3>
      <p class="mo-date">{mo['date']}</p>
      <p class="mo-story">{nl2br(mo['story'])}</p>
      {img_block}
    </div>""", unsafe_allow_html=True)
    if mo.get("video"):
        vp = Path(abs_path(mo["video"])) if mo["video"] else None
        if vp and vp.exists():
            st.video(vp.read_bytes())

st.markdown("</section><div class='div'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 5. VİDEOLAR
# ─────────────────────────────────────────────────────────────────────────────
vid_title_lines = D["videos_title"].strip().split("\n")
vid_title_html  = "<br>".join(vid_title_lines)

st.markdown(f"""
<section class="vid-section">
  <p class="sec-label" style="color:#c9546a">Videolar</p>
  <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(34px,5vw,58px);
    font-weight:300;color:#fff5f0;line-height:1.1;margin-bottom:48px">
    {vid_title_html}
  </h2>
""", unsafe_allow_html=True)

vcols = st.columns(max(len(D["videos"]),1), gap="medium")
for i, vid in enumerate(D["videos"]):
    with vcols[i % len(vcols)]:
        vp = Path(abs_path(vid["file"])) if vid.get("file") else None
        if vp and vp.exists():
            st.video(vp.read_bytes())
            st.markdown(f'<p style="color:rgba(255,245,240,.45);font-size:12px;text-align:center;margin-top:6px;letter-spacing:1px">{vid["label"]}</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="vid-ph"><div class="play-btn">▶</div><p class="vid-lbl">{vid["label"]}</p></div>', unsafe_allow_html=True)

st.markdown("</section><div class='div' style='background:linear-gradient(90deg,transparent,rgba(201,84,106,.08),transparent)'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 6. MÜZİK
# ─────────────────────────────────────────────────────────────────────────────
mu_title_html = "<br>".join(D["music_title"].strip().split("\n"))

st.markdown(f"""
<section class="mu-section">
  <div class="mu-text">
    <p class="sec-label">Müziğimiz</p>
    <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(34px,5vw,58px);
      font-weight:300;color:#1e1210;line-height:1.1">{mu_title_html}</h2>
    <p style="margin-top:24px;font-size:15px;color:#7a5a52;line-height:1.8;font-weight:300;max-width:380px">
      {nl2br(D['music_subtitle'])}
    </p>
  </div>
  <div class="mu-player">
    <div class="player-card">
      <div class="player-thumb">🎵</div>
      <p class="player-song">Bizim Şarkımız</p>
      <p class="player-artist">Eslem, Ahmet & Uraz Efe</p>
""", unsafe_allow_html=True)

mp = Path(abs_path(D["music_file"])) if D.get("music_file") else None
if mp and mp.exists():
    st.audio(mp.read_bytes())
else:
    st.markdown('<p style="font-size:13px;color:#c97f8a;text-align:center;padding:8px 0">Henüz şarkı yüklenmedi</p>', unsafe_allow_html=True)

st.markdown("</div></div></div></section><div class='div'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 7. FİNAL SÜRPRİZ
# ─────────────────────────────────────────────────────────────────────────────
fin_pre_html = "<br>".join(D["finale_pre_title"].strip().split("\n"))
fin_msg_html = nl2br(D["finale_message"])
fin_sign_html = nl2br(D["finale_sign"])

st.markdown(f'<section class="fin-section"><div class="fin-bg"></div>', unsafe_allow_html=True)

if not ss["show_surprise"]:
    st.markdown(f"""
    <p class="fin-label">Son Sürpriz</p>
    <h2 class="fin-title">{fin_pre_html}</h2>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2,1,2])
    with c2:
        if st.button("Son Mesaj ❤️", key="btn_surprise", use_container_width=True):
            ss["show_surprise"] = True
            ss["show_confetti"] = True
            st.rerun()
else:
    if ss["show_confetti"]:
        colors = ["#c9546a","#e8b4b8","#f5c8cc","#fff5f0","#b8495e","#f0d8dd"]
        pieces = "".join([
            f'<div class="cp" style="left:{random.randint(0,100)}%;'
            f'width:{random.randint(6,13)}px;height:{random.randint(6,13)}px;'
            f'background:{colors[i%len(colors)]};'
            f'animation-duration:{random.uniform(2.5,5):.1f}s;'
            f'animation-delay:{random.uniform(0,2):.1f}s;'
            f'border-radius:{"50%" if i%3==0 else "1px"}"></div>'
            for i in range(80)
        ])
        st.markdown(f'<div class="cf-wrap">{pieces}</div>', unsafe_allow_html=True)
        ss["show_confetti"] = False

    fin_img_url = to_data_url(D["finale_img"])
    if fin_img_url:
        st.markdown(f'<img class="surp-img" src="{fin_img_url}">', unsafe_allow_html=True)
    else:
        st.markdown('<div class="surp-ph"><span>📸</span><p style="font-size:12px;color:rgba(255,245,240,.3)">Aile Fotoğrafı</p></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="surp-box">
      <p class="fin-label">Eslem'e, Uraz Efe & Ahmet'ten</p>
      <div class="surp-msg">{fin_msg_html}</div>
      <div class="surp-sign">{fin_sign_html}</div>
    </div>
    """, unsafe_allow_html=True)

    # Final butonu — tekrar göster
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    fc1, fc2, fc3 = st.columns([2,1,2])
    with fc2:
        if st.button("↩ Tekrar Göster", key="btn_replay", use_container_width=True):
            ss["show_surprise"] = False
            st.rerun()

st.markdown("</section>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<footer class="footer">
  <p class="footer-q">{D['footer_quote']}</p>
</footer>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 🔐 GİZLİ ADMIN BUTONU (en altta, soluk görünür)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
lc1, lc2, lc3 = st.columns([4,1,4])
with lc2:
    if not EDIT:
        if st.button("🔐", key="btn_show_pw", help="Yönetici girişi", use_container_width=True):
            ss["show_pw"] = not ss["show_pw"]
            st.rerun()
    else:
        if st.button("🔒 Çıkış", key="btn_logout", use_container_width=True):
            ss["admin"]   = False
            ss["show_pw"] = False
            st.rerun()

# Şifre kutusu
if ss["show_pw"] and not EDIT:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    pw_c1, pw_c2, pw_c3 = st.columns([3,2,3])
    with pw_c2:
        pw = st.text_input("Şifre", type="password", key="pw_field",
                           placeholder="Şifreyi girin", label_visibility="collapsed")
        if st.button("Giriş", key="btn_pw_submit", use_container_width=True):
            if pw == ADMIN_PASSWORD:
                ss["admin"]   = True
                ss["show_pw"] = False
                st.rerun()
            else:
                st.error("Hatalı şifre")

st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ADMIN PANELİ — sadece giriş yapılınca görünür
# ─────────────────────────────────────────────────────────────────────────────
if EDIT:
    st.markdown('<div class="admin-section">', unsafe_allow_html=True)
    st.markdown('<p class="admin-title">⚙️ İçerik Yönetimi</p>', unsafe_allow_html=True)

    # ── GENEL METİNLER ───────────────────────────────────────────────────────
    with st.expander("📝 Genel Metinler & Başlıklar", expanded=False):
        changed = False
        g1, g2 = st.columns(2)

        new_ey = g1.text_input("Hero üst yazı", value=D["hero_eyebrow"], key="g_eyebrow")
        new_ht = g1.text_area("Hero başlık (her satır ayrı)", value=D["hero_title"], key="g_htitle", height=100)
        new_hs = g1.text_area("Hero alt yazı", value=D["hero_subtitle"], key="g_hsub", height=80)

        new_ld = g2.text_input("Mektup tarihi", value=D["letter_date"], key="g_ldate")
        new_lb = g2.text_area("Mektup metni (paragraflar arası boş satır)", value=D["letter_body"], key="g_lbody", height=180)
        new_ls = g2.text_input("Mektup imza", value=D["letter_sign"], key="g_lsign")

        g3, g4 = st.columns(2)
        new_mt  = g3.text_area("Anılar bölüm başlığı", value=D["memories_title"], key="g_memtitle", height=70)
        new_mot = g3.text_area("Anlar bölüm başlığı",  value=D["moments_title"],  key="g_motitle",  height=70)
        new_vt  = g4.text_area("Videolar başlığı",     value=D["videos_title"],   key="g_vtitle",   height=70)
        new_mu  = g4.text_area("Müzik başlığı",        value=D["music_title"],    key="g_mutitle",  height=70)
        new_mus = g4.text_area("Müzik alt yazı",       value=D["music_subtitle"], key="g_musub",    height=70)

        g5, g6 = st.columns(2)
        new_fp  = g5.text_area("Final ön başlık",  value=D["finale_pre_title"], key="g_fpre",   height=70)
        new_fm  = g5.text_area("Final mesajı",     value=D["finale_message"],   key="g_fmsg",   height=100)
        new_fsi = g6.text_input("Final imza",      value=D["finale_sign"],      key="g_fsign")
        new_fq  = g6.text_area("Footer alıntı",    value=D["footer_quote"],     key="g_fquote", height=70)

        if st.button("💾 Metinleri Kaydet", key="save_texts"):
            D.update({
                "hero_eyebrow":D["hero_eyebrow"],"hero_title":new_ht,"hero_subtitle":new_hs,
                "hero_eyebrow":new_ey,
                "letter_date":new_ld,"letter_body":new_lb,"letter_sign":new_ls,
                "memories_title":new_mt,"moments_title":new_mot,
                "videos_title":new_vt,"music_title":new_mu,"music_subtitle":new_mus,
                "finale_pre_title":new_fp,"finale_message":new_fm,"finale_sign":new_fsi,
                "footer_quote":new_fq,
            })
            save_meta(D)
            st.success("✓ Metinler kaydedildi")
            st.rerun()

    # ── HERO FOTOĞRAFI ────────────────────────────────────────────────────────
    with st.expander("📸 Hero Fotoğrafı", expanded=False):
        hc1, hc2 = st.columns([4,1])
        with hc1:
            fh = st.file_uploader("Hero", type=["jpg","jpeg","png","webp"],
                                  key="up_hero", label_visibility="collapsed")
            if fh:
                del_file(D["hero_img"]); D["hero_img"] = save_uploaded(fh,"hero"); save_meta(D); st.rerun()
        with hc2:
            if D["hero_img"] and st.button("🗑", key="del_hero"):
                del_file(D["hero_img"]); D["hero_img"] = None; save_meta(D); st.rerun()
        if D["hero_img"]: st.success("✓ Yüklü")

    # ── ANI KARTLARI ──────────────────────────────────────────────────────────
    with st.expander("🗂 Anı Kartları", expanded=False):
        # Mevcut kartları düzenle
        for i, mem in enumerate(D["memories"]):
            st.markdown(f"**{mem['num']} · {mem['title']}**")
            mc1, mc2, mc3, mc4 = st.columns([2,2,2,1])
            new_mdate  = mc1.text_input("Tarih",   value=mem["date"],  key=f"m_date_{mem['id']}")
            new_mtitle = mc2.text_input("Başlık",  value=mem["title"], key=f"m_title_{mem['id']}")
            new_mdesc  = mc3.text_input("Açıklama",value=mem["desc"],  key=f"m_desc_{mem['id']}")
            if mc4.button("💾", key=f"save_mem_{mem['id']}"):
                D["memories"][i].update({"date":new_mdate,"title":new_mtitle,"desc":new_mdesc})
                save_meta(D); st.success("✓"); st.rerun()

            fc1, fc2, fc3 = st.columns([3,1,1])
            with fc1:
                fm_img = st.file_uploader("Fotoğraf", type=["jpg","jpeg","png"],
                                          key=f"up_mem_{mem['id']}", label_visibility="collapsed")
                if fm_img:
                    del_file(mem["img"]); D["memories"][i]["img"] = save_uploaded(fm_img,"memories"); save_meta(D); st.rerun()
            with fc2:
                if mem["img"] and st.button("🗑 Foto", key=f"del_mem_{mem['id']}"):
                    del_file(mem["img"]); D["memories"][i]["img"] = None; save_meta(D); st.rerun()
            with fc3:
                if mem["img"]: st.success("✓")

            # Kartı sil
            if st.button(f"🗑 Bu kartı sil", key=f"del_mem_card_{mem['id']}"):
                del_file(mem["img"])
                D["memories"].pop(i); save_meta(D); st.rerun()
            st.divider()

        # Yeni kart ekle
        st.markdown("**➕ Yeni Anı Kartı**")
        with st.form("form_add_mem"):
            na1, na2 = st.columns(2)
            n_date  = na1.text_input("Tarih", value="2025")
            n_title = na2.text_input("Başlık")
            n_desc  = st.text_input("Açıklama")
            if st.form_submit_button("Ekle"):
                if n_title:
                    n = len(D["memories"]) + 1
                    D["memories"].append({"id":uuid.uuid4().hex[:8],"num":f"{n:02d}",
                                          "date":n_date,"title":n_title,"desc":n_desc,"img":None})
                    save_meta(D); st.rerun()

    # ── BÜYÜME ANLARI ─────────────────────────────────────────────────────────
    with st.expander("✨ Büyüme Anları", expanded=False):
        for i, mo in enumerate(D["moments"]):
            st.markdown(f"**{mo['icon']} {mo['title']}**")
            ea1, ea2, ea3, ea4 = st.columns([1,2,2,1])
            new_icon  = ea1.text_input("İkon",  value=mo["icon"],     key=f"mo_icon_{mo['id']}")
            new_cat   = ea2.text_input("Kateg.", value=mo["category"],  key=f"mo_cat_{mo['id']}")
            new_mdate = ea2.text_input("Tarih", value=mo["date"],      key=f"mo_date_{mo['id']}")
            new_mttl  = ea3.text_input("Başlık",value=mo["title"],     key=f"mo_ttl_{mo['id']}")
            new_story = ea3.text_area("Hikaye", value=mo["story"],     key=f"mo_story_{mo['id']}", height=80)
            if ea4.button("💾", key=f"save_mo_{mo['id']}"):
                D["moments"][i].update({"icon":new_icon,"category":new_cat,"date":new_mdate,"title":new_mttl,"story":new_story})
                save_meta(D); st.success("✓"); st.rerun()

            ub1, ub2 = st.columns(2)
            with ub1:
                st.caption("📷 Fotoğraf")
                fi = st.file_uploader("Foto", type=["jpg","jpeg","png"],
                                      key=f"up_moimg_{mo['id']}", label_visibility="collapsed")
                if fi:
                    del_file(mo["img"]); D["moments"][i]["img"] = save_uploaded(fi,"moments"); save_meta(D); st.rerun()
                if mo.get("img"):
                    r1, r2 = st.columns(2)
                    if r1.button("🗑 Sil", key=f"del_moimg_{mo['id']}"): del_file(mo["img"]); D["moments"][i]["img"]=None; save_meta(D); st.rerun()
                    r2.success("✓")
            with ub2:
                st.caption("🎬 Video")
                fv = st.file_uploader("Video", type=["mp4","mov"],
                                      key=f"up_movid_{mo['id']}", label_visibility="collapsed")
                if fv:
                    del_file(mo["video"]); D["moments"][i]["video"] = save_uploaded(fv,"moments"); save_meta(D); st.rerun()
                if mo.get("video"):
                    r1, r2 = st.columns(2)
                    if r1.button("🗑 Sil", key=f"del_movid_{mo['id']}"): del_file(mo["video"]); D["moments"][i]["video"]=None; save_meta(D); st.rerun()
                    r2.success("✓")

            if st.button("🗑 Bu anı sil", key=f"del_mo_card_{mo['id']}"):
                del_file(mo.get("img")); del_file(mo.get("video"))
                D["moments"].pop(i); save_meta(D); st.rerun()
            st.divider()

        st.markdown("**➕ Yeni An Ekle**")
        with st.form("form_add_mo"):
            fa1, fa2 = st.columns(2)
            n_icon  = fa1.text_input("İkon", value="⭐")
            n_cat   = fa2.text_input("Kategori")
            fb1, fb2 = st.columns(2)
            n_ttl   = fb1.text_input("Başlık")
            n_dt    = fb2.text_input("Tarih", value="2025")
            n_story = st.text_area("Hikaye", height=80)
            if st.form_submit_button("Ekle"):
                if n_ttl and n_story:
                    D["moments"].append({"id":uuid.uuid4().hex[:8],"icon":n_icon,"category":n_cat,
                                         "title":n_ttl,"date":n_dt,"story":n_story,"img":None,"video":None})
                    save_meta(D); st.rerun()

    # ── VİDEOLAR ─────────────────────────────────────────────────────────────
    with st.expander("🎬 Videolar", expanded=False):
        for i, vid in enumerate(D["videos"]):
            vc1, vc2, vc3, vc4 = st.columns([3,1,1,1])
            new_vlbl = vc1.text_input("Açıklama", value=vid["label"], key=f"vl_{vid['id']}")
            if vc2.button("💾 Kaydet", key=f"save_vl_{vid['id']}"):
                D["videos"][i]["label"] = new_vlbl; save_meta(D); st.rerun()

            fv2 = st.file_uploader("Video yükle", type=["mp4","mov","avi"],
                                   key=f"up_vid_{vid['id']}", label_visibility="collapsed")
            if fv2:
                del_file(vid["file"]); D["videos"][i]["file"] = save_uploaded(fv2,"videos"); save_meta(D); st.rerun()
            if vid.get("file"):
                dv1, dv2 = st.columns(2)
                if dv1.button("🗑 Video sil", key=f"del_vid_{vid['id']}"): del_file(vid["file"]); D["videos"][i]["file"]=None; save_meta(D); st.rerun()
                dv2.success("✓ Yüklü")
            if vc4.button("🗑 Slot sil", key=f"del_slot_{vid['id']}"):
                del_file(vid.get("file")); D["videos"].pop(i); save_meta(D); st.rerun()
            st.divider()

        with st.form("form_add_vid"):
            new_vl = st.text_input("Yeni video adı")
            if st.form_submit_button("➕ Ekle"):
                if new_vl: D["videos"].append({"id":uuid.uuid4().hex[:8],"label":new_vl,"file":None}); save_meta(D); st.rerun()

    # ── MÜZİK ────────────────────────────────────────────────────────────────
    with st.expander("🎵 Müzik", expanded=False):
        mu1, mu2 = st.columns([4,1])
        with mu1:
            fm2 = st.file_uploader("Müzik", type=["mp3","wav","ogg","m4a"],
                                   key="up_music", label_visibility="collapsed")
            if fm2:
                del_file(D["music_file"]); D["music_file"] = save_uploaded(fm2,"music"); save_meta(D); st.rerun()
        with mu2:
            if D.get("music_file") and st.button("🗑 Sil", key="del_music"):
                del_file(D["music_file"]); D["music_file"]=None; save_meta(D); st.rerun()
        if D.get("music_file"): st.success("✓ Müzik yüklü")

    # ── FİNAL FOTOĞRAFI ───────────────────────────────────────────────────────
    with st.expander("🎊 Final Fotoğrafı", expanded=False):
        ff1, ff2 = st.columns([4,1])
        with ff1:
            fff = st.file_uploader("Final foto", type=["jpg","jpeg","png"],
                                   key="up_finale", label_visibility="collapsed")
            if fff:
                del_file(D["finale_img"]); D["finale_img"] = save_uploaded(fff,"finale"); save_meta(D); st.rerun()
        with ff2:
            if D.get("finale_img") and st.button("🗑 Sil", key="del_finale"):
                del_file(D["finale_img"]); D["finale_img"]=None; save_meta(D); st.rerun()
        if D.get("finale_img"): st.success("✓ Yüklü")

    # ── VERİ YÖNETİMİ ─────────────────────────────────────────────────────────
    with st.expander("🗑 Veri Yönetimi", expanded=False):
        st.warning("⚠️ Tüm yüklenen medya dosyaları ve içerik sıfırlanır. Bu işlem geri alınamaz.")
        if not ss["confirm_del"]:
            if st.button("Tüm Verileri Sil", key="btn_ask_del", type="secondary"):
                ss["confirm_del"] = True; st.rerun()
        else:
            d1, d2 = st.columns(2)
            if d1.button("✅ Evet, tümünü sil", key="btn_yes_del", type="primary"):
                clear_all(); ss["show_surprise"]=False; ss["confirm_del"]=False; st.rerun()
            if d2.button("❌ İptal", key="btn_no_del"):
                ss["confirm_del"]=False; st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
