"""
İyi ki varsın Anne ❤️  –  Eslem için
Uraz Efe & Ahmet, 2026

Kalıcı depolama: Dosyalar diske kaydedilir (data/ klasörü).
Sayfa yenilenince, site kapanıp açılınca veriler kaybolmaz.

Kurulum:  pip install streamlit Pillow
Çalıştır: streamlit run app.py
"""

import streamlit as st
import json, os, shutil, uuid, base64
from pathlib import Path

# ── Depolama dizini ────────────────────────────────────────────────────────────
BASE_DIR  = Path(__file__).parent / "data"
META_FILE = BASE_DIR / "meta.json"
MEDIA_DIR = BASE_DIR / "media"
BASE_DIR.mkdir(exist_ok=True)
MEDIA_DIR.mkdir(exist_ok=True)

# ── Varsayılan veri ────────────────────────────────────────────────────────────
DEFAULT_META = {
    "hero_img": None,
    "finale_img": None,
    "music_file": None,
    "music_name": "Bizim Şarkımız",
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

# ── Meta okuma/yazma ──────────────────────────────────────────────────────────
def load_meta():
    if META_FILE.exists():
        try:
            with open(META_FILE, encoding="utf-8") as f:
                stored = json.load(f)
            # yeni anahtarları default'tan ekle
            for k, v in DEFAULT_META.items():
                if k not in stored:
                    stored[k] = v
            return stored
        except Exception:
            pass
    return json.loads(json.dumps(DEFAULT_META))

def save_meta(d):
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

# ── Dosya kaydetme ────────────────────────────────────────────────────────────
def save_uploaded(uploaded_file, subfolder=""):
    """Yüklenen dosyayı diske kaydet, göreceli yolunu döndür."""
    target_dir = MEDIA_DIR / subfolder if subfolder else MEDIA_DIR
    target_dir.mkdir(exist_ok=True)
    ext  = Path(uploaded_file.name).suffix.lower()
    fname = f"{uuid.uuid4().hex}{ext}"
    fpath = target_dir / fname
    with open(fpath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(fpath.relative_to(BASE_DIR))  # data/media/... formatında

def abs_path(rel):
    """Göreceli yolu mutlak yola çevir."""
    return str(BASE_DIR / rel) if rel else None

def file_to_data_url(path):
    """Disk dosyasını base64 data-url'e çevir (HTML içinde göstermek için)."""
    p = Path(path) if path else None
    if not p or not p.exists():
        return None
    ext = p.suffix.lower().lstrip(".")
    mime_map = {
        "jpg":"image/jpeg","jpeg":"image/jpeg","png":"image/png","gif":"image/gif","webp":"image/webp",
        "mp4":"video/mp4","mov":"video/mp4","avi":"video/x-msvideo",
        "mp3":"audio/mpeg","wav":"audio/wav","ogg":"audio/ogg","m4a":"audio/mp4",
    }
    mime = mime_map.get(ext, "application/octet-stream")
    with open(p, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{b64}"

def delete_file(rel):
    """Disk'ten dosyayı sil."""
    if rel:
        p = BASE_DIR / rel
        if p.exists():
            p.unlink()

def clear_all():
    """Tüm media klasörünü sil ve meta'yı sıfırla."""
    if MEDIA_DIR.exists():
        shutil.rmtree(MEDIA_DIR)
    MEDIA_DIR.mkdir(exist_ok=True)
    if META_FILE.exists():
        META_FILE.unlink()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="İyi ki varsın Anne ❤️",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state init ────────────────────────────────────────────────────────
if "edit_mode"          not in st.session_state: st.session_state["edit_mode"]          = False
if "show_surprise"      not in st.session_state: st.session_state["show_surprise"]      = False
if "show_confetti"      not in st.session_state: st.session_state["show_confetti"]      = False
if "confirm_delete_all" not in st.session_state: st.session_state["confirm_delete_all"] = False

DATA = load_meta()
EDIT = st.session_state["edit_mode"]

# ── CSS ───────────────────────────────────────────────────────────────────────
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

/* EDIT BAR */
.edit-bar{position:fixed;top:0;left:0;right:0;z-index:9998;
  background:rgba(30,18,16,0.97);backdrop-filter:blur(12px);
  border-bottom:1px solid rgba(201,84,106,0.35);
  display:flex;align-items:center;gap:12px;padding:10px 24px}
.edit-bar-title{font-size:12px;letter-spacing:3px;text-transform:uppercase;
  color:rgba(201,84,106,0.8);flex:1}
.edit-badge{background:rgba(201,84,106,0.12);border:1px solid rgba(201,84,106,0.3);
  color:#c9546a;font-size:11px;letter-spacing:2px;padding:4px 12px;border-radius:2px}
.page-top-pad{height:52px}

/* HERO */
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
.hero-sub{font-size:16px;font-weight:300;color:#7a5a52;line-height:1.7;max-width:420px;margin-bottom:48px}
.hero-img-side{position:absolute;right:0;top:0;bottom:0;width:52%;overflow:hidden}
.hero-img-side img{width:100%;height:100%;object-fit:cover;filter:brightness(.95) saturate(.9)}
.hero-ph{width:100%;height:100%;background:linear-gradient(160deg,#f0d8dd,#e8c8ce,#dbb5bc);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px}
.hero-ph span{font-size:48px;opacity:.4}
.hero-ph p{font-size:13px;color:#9a6872;letter-spacing:1px}

/* DIVIDER */
.divider{width:100%;height:1px;background:linear-gradient(90deg,transparent,rgba(201,84,106,0.2),transparent)}

/* LETTER */
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

/* SECTION HEADER */
.sec-label{font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#c97f8a;margin-bottom:16px}
.sec-title{font-family:'Cormorant Garamond',serif;font-size:clamp(36px,5vw,60px);
  font-weight:300;color:#1e1210;line-height:1.1}

/* MEMORY CARDS */
.timeline-section{background:#fdf8f4;padding:100px 6vw}
.t-card{background:#fff;border-radius:3px;overflow:hidden;border:1px solid rgba(201,127,138,.1);
  transition:transform .4s cubic-bezier(.22,1,.36,1),box-shadow .4s}
.t-card:hover{transform:translateY(-6px);box-shadow:0 20px 60px rgba(180,100,110,.12)}
.t-card-img{width:100%;height:200px;overflow:hidden;position:relative}
.t-card-img img{width:100%;height:100%;object-fit:cover}
.t-card-ph{width:100%;height:100%;background:linear-gradient(160deg,#f5e0e4,#ead0d5);
  display:flex;align-items:center;justify-content:center;font-size:32px;color:rgba(180,100,110,.3)}
.t-card-num{position:absolute;top:12px;left:12px;background:rgba(255,255,255,.9);border-radius:50%;
  width:30px;height:30px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:500;color:#c9546a}
.t-card-body{padding:28px}
.t-card-date{font-size:11px;letter-spacing:2px;color:#c97f8a;margin-bottom:8px}
.t-card-title{font-family:'Cormorant Garamond',serif;font-size:22px;color:#2a1f1a;margin-bottom:10px}
.t-card-desc{font-size:14px;color:#7a5a52;line-height:1.6;font-weight:300}

/* MOMENTS */
.moments-section{background:#fff;padding:100px 6vw}
.moment-card{background:#fffcf9;border:1px solid rgba(201,127,138,.12);border-radius:4px;
  padding:40px;margin-bottom:32px;position:relative;transition:box-shadow .3s}
.moment-card:hover{box-shadow:0 12px 48px rgba(180,100,110,.08)}
.moment-card::before{content:'';position:absolute;top:0;left:0;bottom:0;width:3px;
  background:linear-gradient(180deg,#e8b4b8,#c9546a)}
.moment-icon{font-size:28px;margin-bottom:12px;display:block}
.moment-cat{font-size:10px;letter-spacing:3px;text-transform:uppercase;color:#c97f8a;margin-bottom:6px}
.moment-title{font-family:'Cormorant Garamond',serif;font-size:28px;font-weight:400;color:#2a1f1a;margin-bottom:12px}
.moment-date{font-size:11px;color:#b8897e;letter-spacing:1px;margin-bottom:16px}
.moment-story{font-family:'Cormorant Garamond',serif;font-size:19px;font-weight:300;line-height:2;color:#4a3830}
.moment-media{margin-top:24px;border-radius:3px;overflow:hidden}
.moment-media img{width:100%;max-height:460px;object-fit:cover;border-radius:3px}

/* VIDEO */
.video-section{background:#1e1210;padding:100px 6vw}
.video-ph{aspect-ratio:16/9;background:#2e1f1a;border-radius:3px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;
  border:1px solid rgba(201,84,106,.15)}
.play-btn{width:56px;height:56px;border:1.5px solid rgba(201,84,106,.5);border-radius:50%;
  display:flex;align-items:center;justify-content:center;font-size:18px;color:#c9546a}
.video-lbl{font-size:13px;color:rgba(255,245,240,.5);letter-spacing:1px}

/* MUSIC */
.music-section{background:#fdf8f4;padding:100px 6vw;display:flex;align-items:center;gap:80px;flex-wrap:wrap}
.music-text{flex:1;min-width:280px}
.music-player-wrap{flex:0 0 360px;min-width:280px}
.player-card{background:#fff;border:1px solid rgba(201,127,138,.15);border-radius:4px;
  padding:40px;text-align:center;box-shadow:0 4px 24px rgba(180,100,110,.06)}
.player-thumb{width:120px;height:120px;border-radius:50%;
  background:linear-gradient(135deg,#f0d8dd,#e8c0c8);
  margin:0 auto 28px;display:flex;align-items:center;justify-content:center;font-size:36px}
.player-song{font-family:'Cormorant Garamond',serif;font-size:22px;color:#2a1f1a;margin-bottom:4px}
.player-artist{font-size:13px;color:#9a7a72;margin-bottom:20px}

/* FINALE */
.finale-section{background:linear-gradient(160deg,#1e1210,#2e1a18,#1e1210);
  padding:120px 6vw;text-align:center;position:relative;overflow:hidden}
.finale-bg{position:absolute;inset:0;
  background:radial-gradient(ellipse at 50% 50%,rgba(201,84,106,.1) 0%,transparent 70%);pointer-events:none}
.finale-label{color:rgba(201,84,106,.7);font-size:11px;letter-spacing:4px;text-transform:uppercase;margin-bottom:32px}
.finale-title{font-family:'Cormorant Garamond',serif;font-size:clamp(40px,6vw,72px);
  font-weight:300;color:#fff5f0;line-height:1.2;margin-bottom:48px}
.surprise-box{animation:fadeUp .8s cubic-bezier(.22,1,.36,1) both}
.finale-img-round{width:280px;height:280px;border-radius:50%;object-fit:cover;
  margin:0 auto 48px;display:block;
  border:3px solid rgba(201,84,106,.3);box-shadow:0 0 60px rgba(201,84,106,.2)}
.finale-ph{width:280px;height:280px;border-radius:50%;
  background:linear-gradient(135deg,#3a2520,#2e1a18);border:1px solid rgba(201,84,106,.2);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  margin:0 auto 48px;font-size:40px;gap:12px}
.surprise-msg{font-family:'Cormorant Garamond',serif;font-size:clamp(22px,3vw,34px);
  font-weight:300;color:#fff5f0;line-height:1.8;max-width:560px;margin:0 auto 16px}
.surprise-sign{font-family:'Cormorant Garamond',serif;font-size:20px;font-style:italic;color:#c9546a;margin-top:24px}

/* FOOTER */
.quote-footer{background:#1e1210;padding:60px 6vw;text-align:center;border-top:1px solid rgba(201,84,106,.1)}
.quote-text{font-family:'Cormorant Garamond',serif;font-size:clamp(16px,2.5vw,22px);
  font-weight:300;font-style:italic;color:rgba(255,245,240,.4);max-width:600px;margin:0 auto;line-height:1.8}

/* CONFETTI */
.confetti-wrap{position:fixed;inset:0;pointer-events:none;z-index:9999;overflow:hidden}
.cp{position:absolute;top:-10px;animation:fall linear forwards}
@keyframes fall{to{transform:translateY(110vh) rotate(720deg);opacity:0}}
@keyframes fadeUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.15)}}

[data-testid="stFileUploader"]{padding:0!important}
[data-testid="stFileUploader"] section{padding:8px!important;border-radius:4px!important;
  background:rgba(253,248,244,0.5)!important;border-color:rgba(201,127,138,0.3)!important}

@media(max-width:768px){
  .hero-img-side{display:none}
  .letter-card{padding:40px 28px}
  .music-section{flex-direction:column;gap:40px}
  .music-player-wrap{flex:1;width:100%}
}
</style>
""", unsafe_allow_html=True)

# ── Edit bar ──────────────────────────────────────────────────────────────────
if EDIT:
    st.markdown('<div class="edit-bar"><span class="edit-bar-title">✏️ Düzenleme Modu</span><span class="edit-badge">AÇIK</span></div><div class="page-top-pad"></div>', unsafe_allow_html=True)

# Edit toggle — top right
_tc1, _tc2 = st.columns([8, 1])
with _tc2:
    if st.button("✏️ Düzenle" if not EDIT else "✅ Kapat", key="btn_toggle_edit", use_container_width=True):
        st.session_state["edit_mode"] = not EDIT
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# 1. HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<section class="hero-wrap">
  <div class="hero-blob" style="width:700px;height:700px;top:-200px;right:-100px"></div>
  <div class="hero-blob" style="width:400px;height:400px;bottom:-100px;left:-80px"></div>
  <div class="hero-content">
    <p class="hero-eyebrow">Anneler Günü · 2026</p>
    <h1 class="hero-title">İyi ki<br>varsın<br><em>Anne</em> ❤️</h1>
    <p class="hero-sub">Bugün sana küçük ama özel bir sürpriz hazırladık.<br>Uraz Efe ve Ahmet'ten, sana…</p>
  </div>
  <div class="hero-img-side">
""", unsafe_allow_html=True)

hero_url = file_to_data_url(abs_path(DATA["hero_img"])) if DATA["hero_img"] else None
if hero_url:
    st.markdown(f'<img src="{hero_url}" style="width:100%;height:100%;object-fit:cover;filter:brightness(.95) saturate(.9)">', unsafe_allow_html=True)
else:
    st.markdown('<div class="hero-ph"><span>📸</span><p>AİLE FOTOĞRAFI</p></div>', unsafe_allow_html=True)

st.markdown("</div></section><div class='divider'></div>", unsafe_allow_html=True)

if EDIT:
    with st.expander("📸 Hero Fotoğrafı", expanded=False):
        col_h1, col_h2 = st.columns([4, 1])
        with col_h1:
            f = st.file_uploader("Hero fotoğrafı", type=["jpg","jpeg","png"],
                                 key="up_hero", label_visibility="collapsed")
            if f:
                if DATA["hero_img"]: delete_file(DATA["hero_img"])
                DATA["hero_img"] = save_uploaded(f, "hero")
                save_meta(DATA)
                st.rerun()
        with col_h2:
            if DATA["hero_img"] and st.button("🗑 Sil", key="del_hero"):
                delete_file(DATA["hero_img"])
                DATA["hero_img"] = None
                save_meta(DATA)
                st.rerun()
        if DATA["hero_img"]: st.success("✓ Fotoğraf yüklü — sayfa yenilenince de kalır")


# ══════════════════════════════════════════════════════════════════════════════
# 2. MEKTUP
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<section id="letter" class="letter-section">
  <div class="letter-label">Uraz Efe'den Mektup</div>
  <div class="letter-card">
    <p class="letter-date">Mayıs 2026</p>
    <p class="letter-salutation">Merhaba anne,</p>
    <div class="letter-body">
      <p>Ben henüz tam konuşamıyorum ama sana her gün teşekkür etmek istiyorum.</p>
      <p>Beni sabırla uyuttuğun,<br>beni güldürdüğün,<br>
         hasta olduğumda hiç ayrılmadığın,<br>
         ve bana sevginin ne olduğunu gösterdiğin için teşekkür ederim.</p>
      <p>Dünyaya gözlerimi ilk açtığımda ilk gördüğüm sendin.<br>
         Ve o andan beri sen benim her şeyimsin.</p>
      <p>Seni çok seviyorum.</p>
    </div>
    <div class="letter-sign">Uraz Efe <span class="letter-heart">❤️</span></div>
  </div>
</section>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 3. ANI KARTI TİMLİNE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<section id="memories" class="timeline-section">
  <div style="margin-bottom:64px">
    <p class="sec-label">Anılarımız</p>
    <h2 class="sec-title">Birlikte yazdığımız<br>en güzel sayfalar</h2>
  </div>
""", unsafe_allow_html=True)

for i, mem in enumerate(DATA["memories"]):
    img_url = file_to_data_url(abs_path(mem["img"])) if mem["img"] else None
    img_html = f'<img src="{img_url}" style="width:100%;height:100%;object-fit:cover">' if img_url else '<div class="t-card-ph">📸</div>'
    st.markdown(f"""
    <div class="t-card" style="animation:fadeUp .8s {i*0.15}s cubic-bezier(.22,1,.36,1) both">
      <div class="t-card-img">{img_html}<div class="t-card-num">{mem['num']}</div></div>
      <div class="t-card-body">
        <p class="t-card-date">{mem['date']}</p>
        <h3 class="t-card-title">{mem['title']}</h3>
        <p class="t-card-desc">{mem['desc']}</p>
      </div>
    </div>""", unsafe_allow_html=True)

st.markdown("</section><div class='divider'></div>", unsafe_allow_html=True)

if EDIT:
    with st.expander("📷 Anı Kartlarını Düzenle", expanded=False):
        for i, mem in enumerate(DATA["memories"]):
            st.markdown(f"**{mem['num']} — {mem['title']}**")
            mc1, mc2, mc3 = st.columns([3, 1, 1])
            with mc1:
                f = st.file_uploader("Fotoğraf", type=["jpg","jpeg","png"],
                                     key=f"up_mem_{mem['id']}", label_visibility="collapsed")
                if f:
                    if mem["img"]: delete_file(mem["img"])
                    DATA["memories"][i]["img"] = save_uploaded(f, "memories")
                    save_meta(DATA)
                    st.rerun()
            with mc2:
                if mem["img"] and st.button("🗑 Sil", key=f"del_mem_{mem['id']}"):
                    delete_file(mem["img"])
                    DATA["memories"][i]["img"] = None
                    save_meta(DATA)
                    st.rerun()
            with mc3:
                if mem["img"]: st.success("✓")
            st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# 4. BÜYÜME ANLAR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<section id="moments" class="moments-section">
  <div style="margin-bottom:64px">
    <p class="sec-label">Büyüme Yolculuğu</p>
    <h2 class="sec-title">İyi günler, kötü günler,<br>hepsi bizim</h2>
  </div>
""", unsafe_allow_html=True)

for mo in DATA["moments"]:
    img_url = file_to_data_url(abs_path(mo["img"])) if mo.get("img") else None
    img_block = f'<div class="moment-media"><img src="{img_url}"></div>' if img_url else ""
    st.markdown(f"""
    <div class="moment-card">
      <span class="moment-icon">{mo['icon']}</span>
      <p class="moment-cat">{mo['category']}</p>
      <h3 class="moment-title">{mo['title']}</h3>
      <p class="moment-date">{mo['date']}</p>
      <p class="moment-story">{mo['story']}</p>
      {img_block}
    </div>""", unsafe_allow_html=True)
    if mo.get("video") and abs_path(mo["video"]) and Path(abs_path(mo["video"])).exists():
        with open(abs_path(mo["video"]), "rb") as vf:
            st.video(vf.read())

st.markdown("</section><div class='divider'></div>", unsafe_allow_html=True)

if EDIT:
    with st.expander("✨ Büyüme Anlarını Düzenle", expanded=False):
        for i, mo in enumerate(DATA["moments"]):
            st.markdown(f"**{mo['icon']} {mo['title']}**")
            ec1, ec2 = st.columns(2)
            with ec1:
                st.caption("📷 Fotoğraf")
                fi = st.file_uploader("Foto", type=["jpg","jpeg","png"],
                                      key=f"up_moimg_{mo['id']}", label_visibility="collapsed")
                if fi:
                    if mo.get("img"): delete_file(mo["img"])
                    DATA["moments"][i]["img"] = save_uploaded(fi, "moments")
                    save_meta(DATA)
                    st.rerun()
                if mo.get("img"):
                    r1, r2 = st.columns(2)
                    r2.success("✓ Yüklü")
                    if r1.button("🗑 Foto sil", key=f"del_moimg_{mo['id']}"):
                        delete_file(mo["img"])
                        DATA["moments"][i]["img"] = None
                        save_meta(DATA)
                        st.rerun()
            with ec2:
                st.caption("🎬 Video")
                fv = st.file_uploader("Video", type=["mp4","mov"],
                                      key=f"up_movid_{mo['id']}", label_visibility="collapsed")
                if fv:
                    if mo.get("video"): delete_file(mo["video"])
                    DATA["moments"][i]["video"] = save_uploaded(fv, "moments")
                    save_meta(DATA)
                    st.rerun()
                if mo.get("video"):
                    r1, r2 = st.columns(2)
                    r2.success("✓ Yüklü")
                    if r1.button("🗑 Video sil", key=f"del_movid_{mo['id']}"):
                        delete_file(mo["video"])
                        DATA["moments"][i]["video"] = None
                        save_meta(DATA)
                        st.rerun()
            st.divider()

        st.markdown("**➕ Yeni An Ekle**")
        with st.form("form_add_moment"):
            fa1, fa2 = st.columns(2)
            n_icon = fa1.text_input("İkon", value="⭐")
            n_cat  = fa2.text_input("Kategori", value="Özel Anlar")
            n_title = st.text_input("Başlık")
            fb1, fb2 = st.columns(2)
            n_date  = fb1.text_input("Tarih", value="2025")
            n_story = st.text_area("Hikaye", height=80)
            if st.form_submit_button("✅ Ekle"):
                if n_title and n_story:
                    DATA["moments"].append({
                        "id": uuid.uuid4().hex[:8],
                        "icon": n_icon, "category": n_cat,
                        "title": n_title, "date": n_date,
                        "story": n_story, "img": None, "video": None
                    })
                    save_meta(DATA)
                    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# 5. VİDEOLAR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<section id="videos" class="video-section">
  <p class="sec-label" style="color:#c9546a">Videolar</p>
  <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(36px,5vw,60px);
    font-weight:300;color:#fff5f0;line-height:1.1;margin-bottom:48px">
    Küçük mutluluğumuzun<br>en tatlı halleri
  </h2>
""", unsafe_allow_html=True)

vcols = st.columns(max(len(DATA["videos"]), 1), gap="medium")
for i, vid in enumerate(DATA["videos"]):
    with vcols[i % len(vcols)]:
        vpath = abs_path(vid["file"]) if vid.get("file") else None
        if vpath and Path(vpath).exists():
            with open(vpath, "rb") as vf:
                st.video(vf.read())
            st.markdown(f'<p style="color:rgba(255,245,240,.5);font-size:12px;text-align:center;margin-top:6px;letter-spacing:1px">{vid["label"]}</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="video-ph"><div class="play-btn">▶</div><p class="video-lbl">{vid["label"]}</p></div>', unsafe_allow_html=True)

st.markdown("</section><div class='divider' style='background:linear-gradient(90deg,transparent,rgba(201,84,106,.1),transparent)'></div>", unsafe_allow_html=True)

if EDIT:
    with st.expander("🎬 Videoları Düzenle", expanded=False):
        for i, vid in enumerate(DATA["videos"]):
            st.markdown(f"**{vid['label']}**")
            vc1, vc2, vc3 = st.columns([3, 1, 1])
            with vc1:
                fv = st.file_uploader("Video", type=["mp4","mov","avi"],
                                      key=f"up_vid_{vid['id']}", label_visibility="collapsed")
                if fv:
                    if vid.get("file"): delete_file(vid["file"])
                    DATA["videos"][i]["file"] = save_uploaded(fv, "videos")
                    save_meta(DATA)
                    st.rerun()
            with vc2:
                if vid.get("file") and st.button("🗑 Sil", key=f"del_vid_{vid['id']}"):
                    delete_file(vid["file"])
                    DATA["videos"][i]["file"] = None
                    save_meta(DATA)
                    st.rerun()
            with vc3:
                if vid.get("file"): st.success("✓")
            st.divider()

        with st.form("form_add_video"):
            new_vl = st.text_input("Yeni video adı")
            if st.form_submit_button("➕ Video Slotu Ekle"):
                if new_vl:
                    DATA["videos"].append({"id": uuid.uuid4().hex[:8], "label": new_vl, "file": None})
                    save_meta(DATA)
                    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# 6. MÜZİK
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<section id="music" class="music-section">
  <div class="music-text">
    <p class="sec-label">Müziğimiz</p>
    <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(36px,5vw,60px);
      font-weight:300;color:#1e1210;line-height:1.1">Bizim<br>şarkımız</h2>
    <p style="margin-top:24px;font-size:15px;color:#7a5a52;line-height:1.8;font-weight:300;max-width:380px">
      Her ailenin kendine ait bir melodisi vardır.<br>Bu bizimki. Her çalanda içimiz ısınır.
    </p>
  </div>
  <div class="music-player-wrap">
    <div class="player-card">
      <div class="player-thumb">🎵</div>
      <p class="player-song">Bizim Şarkımız</p>
      <p class="player-artist">Eslem, Ahmet & Uraz Efe</p>
""", unsafe_allow_html=True)

mpath = abs_path(DATA["music_file"]) if DATA.get("music_file") else None
if mpath and Path(mpath).exists():
    with open(mpath, "rb") as mf:
        st.audio(mf.read())
else:
    st.markdown('<p style="font-size:13px;color:#c97f8a;text-align:center;padding:8px 0">Henüz şarkı yüklenmedi</p>', unsafe_allow_html=True)

st.markdown("</div></div></div></section><div class='divider'></div>", unsafe_allow_html=True)

if EDIT:
    with st.expander("🎵 Müziği Düzenle", expanded=False):
        mu1, mu2 = st.columns([4, 1])
        with mu1:
            fm = st.file_uploader("Müzik", type=["mp3","wav","ogg","m4a"],
                                  key="up_music", label_visibility="collapsed")
            if fm:
                if DATA.get("music_file"): delete_file(DATA["music_file"])
                DATA["music_file"] = save_uploaded(fm, "music")
                save_meta(DATA)
                st.rerun()
        with mu2:
            if DATA.get("music_file") and st.button("🗑 Sil", key="del_music"):
                delete_file(DATA["music_file"])
                DATA["music_file"] = None
                save_meta(DATA)
                st.rerun()
        if DATA.get("music_file"): st.success("✓ Müzik yüklü")


# ══════════════════════════════════════════════════════════════════════════════
# 7. FİNAL SÜRPRİZ
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<section id="finale" class="finale-section"><div class="finale-bg"></div>', unsafe_allow_html=True)

if not st.session_state["show_surprise"]:
    st.markdown("""
    <p class="finale-label">Son Sürpriz</p>
    <h2 class="finale-title">Hazır mısın,<br>Eslem?</h2>
    """, unsafe_allow_html=True)

    if EDIT:
        ef1, ef2, ef3 = st.columns([2, 2, 2])
        with ef2:
            st.markdown('<p style="color:#c97f8a;font-size:11px;letter-spacing:2px;text-align:center">📎 Final Fotoğrafı</p>', unsafe_allow_html=True)
            ff = st.file_uploader("Final", type=["jpg","jpeg","png"],
                                  key="up_finale", label_visibility="collapsed")
            if ff:
                if DATA.get("finale_img"): delete_file(DATA["finale_img"])
                DATA["finale_img"] = save_uploaded(ff, "finale")
                save_meta(DATA)
                st.rerun()
            if DATA.get("finale_img") and st.button("🗑 Sil", key="del_finale"):
                delete_file(DATA["finale_img"])
                DATA["finale_img"] = None
                save_meta(DATA)
                st.rerun()

    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        if st.button("Son Mesaj ❤️", key="surprise_btn", use_container_width=True):
            st.session_state["show_surprise"] = True
            st.session_state["show_confetti"] = True
            st.rerun()

else:
    import random as _r
    if st.session_state["show_confetti"]:
        colors = ["#c9546a","#e8b4b8","#f5c8cc","#fff5f0","#b8495e","#f0d8dd"]
        pieces = "".join([
            f'<div class="cp" style="left:{_r.randint(0,100)}%;'
            f'width:{_r.randint(6,13)}px;height:{_r.randint(6,13)}px;'
            f'background:{colors[i%len(colors)]};'
            f'animation-duration:{_r.uniform(2.5,5):.1f}s;'
            f'animation-delay:{_r.uniform(0,2):.1f}s;'
            f'border-radius:{"50%" if i%3==0 else "1px"}"></div>'
            for i in range(80)
        ])
        st.markdown(f'<div class="confetti-wrap">{pieces}</div>', unsafe_allow_html=True)
        st.session_state["show_confetti"] = False

    fp = abs_path(DATA["finale_img"]) if DATA.get("finale_img") else None
    fp_url = file_to_data_url(fp) if fp and Path(fp).exists() else None
    if fp_url:
        st.markdown(f'<img class="finale-img-round" src="{fp_url}">', unsafe_allow_html=True)
    else:
        st.markdown('<div class="finale-ph"><span>📸</span><p style="font-size:12px;color:rgba(255,245,240,.3)">AİLE FOTOĞRAFI</p></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="surprise-box">
      <p class="finale-label">Eslem'e, Uraz Efe & Ahmet'ten</p>
      <div class="surprise-msg">
        Bazı insanlar anne olur.<br>
        <em>Sen bizim yuvamız oldun.</em><br><br>
        Her sabah uyanışımız, her gülüşümüz,<br>
        her küçük anımız — hepsi seninle anlam kazandı.
      </div>
      <div class="surprise-sign">Seni çok seviyoruz &nbsp;❤️<br>Uraz Efe & Ahmet</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</section>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<footer class="quote-footer">
  <p class="quote-text">"Dünyanın tüm çiçeklerini toplasam, senin bir gülüşüne değişmem anne."</p>
</footer>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TÜM VERİLERİ SİL (en altta, her zaman görünür)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
st.divider()
st.markdown("<p style='text-align:center;font-size:12px;color:#bbb;letter-spacing:1px'>VERİ YÖNETİMİ</p>", unsafe_allow_html=True)

cd1, cd2, cd3 = st.columns([3, 2, 3])
with cd2:
    if not st.session_state["confirm_delete_all"]:
        if st.button("🗑 Tüm Yüklenen Verileri Sil", key="btn_ask_delete",
                     use_container_width=True, type="secondary"):
            st.session_state["confirm_delete_all"] = True
            st.rerun()
    else:
        st.warning("⚠️ Tüm fotoğraf, video ve müzik silinecek. Bu işlem geri alınamaz.")
        dd1, dd2 = st.columns(2)
        if dd1.button("✅ Evet, sil", key="btn_confirm_delete", use_container_width=True, type="primary"):
            clear_all()
            st.session_state["show_surprise"] = False
            st.session_state["confirm_delete_all"] = False
            st.rerun()
        if dd2.button("❌ İptal", key="btn_cancel_delete", use_container_width=True):
            st.session_state["confirm_delete_all"] = False
            st.rerun()

st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
