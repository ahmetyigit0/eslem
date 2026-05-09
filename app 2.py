"""
İyi ki varsın Anne ❤️  –  Eslem için
Uraz Efe & Ahmet, 2026

Kalıcı depolama: streamlit-local-storage paketi ile tarayıcıda saklanır.
Yükleme:  pip install streamlit streamlit-local-storage Pillow
Çalıştırma: streamlit run app.py
"""

import streamlit as st
import base64, json, uuid
from datetime import datetime

# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="İyi ki varsın Anne ❤️",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── try local-storage ─────────────────────────────────────────────────────────
try:
    from streamlit_local_storage import LocalStorage
    _ls = LocalStorage()
    HAS_LS = True
except Exception:
    HAS_LS = False

LS_KEY = "anne_app_data_v2"

# ─────────────────────────────────────────────────────────────────────────────
# Veri modeli & kalıcı depolama
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_DATA = {
    "hero_img": None,         # base64 data-url
    "finale_img": None,
    "music_url": None,
    "music_name": "Bizim Şarkımız",
    "memories": [
        {"id":"m1","num":"01","date":"Ekim 2024",  "title":"Uraz Efe Doğdu",        "desc":"Küçük ellerin ilk kez senin parmağını tuttuğu an — dünyanın durduğu an.","img":None},
        {"id":"m2","num":"02","date":"Kasım 2024", "title":"İlk Aile Fotoğrafımız","desc":"Üçümüz, bir çatı altında, yeni bir hikâyenin başında.","img":None},
        {"id":"m3","num":"03","date":"Şubat 2025", "title":"İlk Tatilimiz",         "desc":"Deniz kokusu, bebek sesi ve senin gülüşün. Mükemmel bir tablo.","img":None},
        {"id":"m4","num":"04","date":"Mart 2025",  "title":"İlk Kahkahamız",        "desc":"Uraz Efe ilk kez güldüğünde sen de güldün. O ses hâlâ kulaklarımızda.","img":None},
    ],
    "moments": [
        {"id":"mo1","icon":"🤒","category":"Hastalık Anları",     "date":"Aralık 2024","title":"İlk Ateşimiz",            "story":"Üç gündü hiç inmiyordu. Sen hiç ayrılmadın başından. Sabahın dördünde alnıma koyduğun ıslak bezi unutmadım.","img":None,"video":None},
        {"id":"mo2","icon":"🍼","category":"Beslenme Keyifleri",  "date":"Kasım 2024","title":"İlk Mama Macerası",        "story":"Yüzüme sürdüm, saçıma bulaştırdım, sana da fırlattım. Sen sadece güldün. O gülüş her şeye değdi.","img":None,"video":None},
        {"id":"mo3","icon":"🐛","category":"Emekleme",            "date":"Ocak 2025", "title":"İlk Adımlarım",            "story":"Önce diz çöküp ilerlemeye çalıştım. Sonra anladım. Nereye gidersem gitsin, sen oradaydın.","img":None,"video":None},
        {"id":"mo4","icon":"👣","category":"Yürüme",              "date":"Mart 2025", "title":"İlk Adım Attım",           "story":"Sallandım, senin kollarına düştüm. Dünyayı fethettim sanki. Sen zaten oradaydın — her zaman olduğun gibi.","img":None,"video":None},
        {"id":"mo5","icon":"😄","category":"İyi Günler",          "date":"Nisan 2025","title":"Güneşli Bir Pazar Sabahı","story":"Üçümüz birlikte uyandık. Pencereden güneş süzülüyordu. Hiçbir şey olmadı ama her şey mükemmeldi.","img":None,"video":None},
        {"id":"mo6","icon":"🌧","category":"Kötü Günler",         "date":"Şubat 2025","title":"Uykusuz Geceler",          "story":"Bazen ikimiz de ağlıyorduk. Ama sen hiç bırakmadın. Sabah olunca gülümsüyordun — bu cesaret nereden geliyordu?","img":None,"video":None},
    ],
    "videos": [
        {"id":"v1","label":"Uraz Efe'nin İlk Sesi",    "url":None},
        {"id":"v2","label":"Birlikte Uyuyan Anımız",   "url":None},
        {"id":"v3","label":"Parkta Bir Sabah",         "url":None},
    ],
}

# ── load / save ───────────────────────────────────────────────────────────────
def load_data():
    if HAS_LS:
        try:
            raw = _ls.getItem(LS_KEY)
            if raw:
                stored = json.loads(raw) if isinstance(raw, str) else raw
                # merge: new keys from DEFAULT_DATA that might not exist yet
                for k, v in DEFAULT_DATA.items():
                    if k not in stored:
                        stored[k] = v
                return stored
        except Exception:
            pass
    if "app_data" in st.session_state:
        return st.session_state["app_data"]
    return json.loads(json.dumps(DEFAULT_DATA))

def save_data(d):
    st.session_state["app_data"] = d
    if HAS_LS:
        try:
            _ls.setItem(LS_KEY, json.dumps(d, ensure_ascii=False))
        except Exception:
            pass

def clear_all_data():
    if HAS_LS:
        try:
            _ls.deleteItem(LS_KEY)
        except Exception:
            pass
    st.session_state.pop("app_data", None)

# ── helpers ───────────────────────────────────────────────────────────────────
def file_to_data_url(f):
    data = f.read()
    b64  = base64.b64encode(data).decode()
    return f"data:{f.type};base64,{b64}"

def img_tag(url, style="width:100%;height:100%;object-fit:cover"):
    return f'<img src="{url}" style="{style}">' if url else ""

# ── init ──────────────────────────────────────────────────────────────────────
if "data" not in st.session_state:
    st.session_state["data"] = load_data()
if "edit_mode" not in st.session_state:
    st.session_state["edit_mode"] = False
if "show_surprise" not in st.session_state:
    st.session_state["show_surprise"] = False
if "show_confetti" not in st.session_state:
    st.session_state["show_confetti"] = False
if "confirm_delete_all" not in st.session_state:
    st.session_state["confirm_delete_all"] = False

DATA = st.session_state["data"]
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

/* ── EDIT BAR ── */
.edit-bar{
  position:fixed;top:0;left:0;right:0;z-index:999;
  background:rgba(30,18,16,0.96);
  backdrop-filter:blur(12px);
  border-bottom:1px solid rgba(201,84,106,0.3);
  display:flex;align-items:center;gap:12px;
  padding:10px 24px;
}
.edit-bar-title{
  font-size:12px;letter-spacing:3px;text-transform:uppercase;
  color:rgba(201,84,106,0.8);flex:1}
.edit-badge{
  background:rgba(201,84,106,0.12);
  border:1px solid rgba(201,84,106,0.3);
  color:#c9546a;font-size:11px;letter-spacing:2px;
  padding:4px 12px;border-radius:2px}
.page-offset{padding-top:52px}

/* ── UPLOAD ZONE ── */
.upload-zone{
  background:rgba(253,248,244,0.95);
  border:1.5px dashed rgba(201,127,138,0.45);
  border-radius:6px;padding:10px 14px;margin:8px 0}
.upload-lbl{
  display:block;font-size:10px;letter-spacing:2.5px;
  text-transform:uppercase;color:#c97f8a;margin-bottom:4px}
[data-testid="stFileUploader"]{padding:0!important}
[data-testid="stFileUploader"] section{
  padding:8px!important;border-radius:4px!important;
  background:rgba(253,248,244,0.5)!important;
  border-color:rgba(201,127,138,0.3)!important}

/* ── HERO ── */
.hero-wrap{
  position:relative;width:100%;min-height:100vh;
  background:linear-gradient(135deg,#fff9f5 0%,#fdeef0 40%,#f9e8ee 100%);
  display:flex;align-items:center;overflow:hidden}
.hero-blob{position:absolute;border-radius:50%;
  background:radial-gradient(circle,rgba(237,176,185,0.18) 0%,transparent 70%)}
.hero-content{
  position:relative;z-index:2;max-width:640px;padding:80px 6vw;
  animation:fadeUp 1.2s cubic-bezier(.22,1,.36,1) both}
.hero-eyebrow{font-size:12px;letter-spacing:3px;text-transform:uppercase;color:#c97f8a;margin-bottom:20px}
.hero-title{
  font-family:'Cormorant Garamond',serif;
  font-size:clamp(52px,8vw,96px);font-weight:300;
  line-height:1.05;color:#1e1210;margin-bottom:28px}
.hero-title em{color:#c9546a;font-style:italic}
.hero-sub{font-size:16px;font-weight:300;color:#7a5a52;line-height:1.7;max-width:420px;margin-bottom:48px}
.hero-img-side{position:absolute;right:0;top:0;bottom:0;width:52%;overflow:hidden}
.hero-img-side img{width:100%;height:100%;object-fit:cover;filter:brightness(.95) saturate(.9)}
.hero-ph{width:100%;height:100%;background:linear-gradient(160deg,#f0d8dd,#e8c8ce,#dbb5bc);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px}
.hero-ph span{font-size:48px;opacity:.4}
.hero-ph p{font-size:13px;color:#9a6872;letter-spacing:1px}

/* ── DIVIDER ── */
.divider{width:100%;height:1px;
  background:linear-gradient(90deg,transparent,rgba(201,84,106,0.2),transparent)}

/* ── LETTER ── */
.letter-section{background:#fff;padding:100px 6vw}
.letter-label{font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#c97f8a;
  margin-bottom:40px;display:flex;align-items:center;gap:16px}
.letter-label::after{content:'';flex:1;height:1px;
  background:linear-gradient(90deg,rgba(201,127,138,.3),transparent)}
.letter-card{max-width:680px;margin:0 auto;background:#fffcf9;
  border:1px solid rgba(201,127,138,.12);border-radius:4px;
  padding:64px 72px;position:relative;box-shadow:0 8px 48px rgba(180,100,110,.06)}
.letter-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,#e8b4b8,#c9546a,#e8b4b8)}
.letter-date{font-size:12px;color:#b8897e;letter-spacing:1px;margin-bottom:32px}
.letter-salutation{font-family:'Cormorant Garamond',serif;font-size:28px;
  font-style:italic;color:#2a1f1a;margin-bottom:24px}
.letter-body{font-family:'Cormorant Garamond',serif;font-size:20px;
  font-weight:300;line-height:2;color:#4a3830}
.letter-body p{margin-bottom:16px}
.letter-sign{margin-top:40px;font-family:'Cormorant Garamond',serif;
  font-size:22px;font-style:italic;color:#c9546a}
.letter-heart{display:inline-block;animation:pulse 1.8s ease-in-out infinite}

/* ── SECTION HEADER ── */
.sec-label{font-size:11px;letter-spacing:4px;text-transform:uppercase;color:#c97f8a;margin-bottom:16px}
.sec-title{font-family:'Cormorant Garamond',serif;font-size:clamp(36px,5vw,60px);
  font-weight:300;color:#1e1210;line-height:1.1}

/* ── MEMORY CARDS ── */
.timeline-section{background:#fdf8f4;padding:100px 6vw}
.t-card{background:#fff;border-radius:3px;overflow:hidden;
  border:1px solid rgba(201,127,138,.1);
  transition:transform .4s cubic-bezier(.22,1,.36,1),box-shadow .4s}
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

/* ── MOMENT CARDS ── */
.moments-section{background:#fff;padding:100px 6vw}
.moment-card{
  background:#fffcf9;border:1px solid rgba(201,127,138,.12);
  border-radius:4px;padding:36px;margin-bottom:32px;position:relative;
  transition:box-shadow .3s}
.moment-card:hover{box-shadow:0 12px 48px rgba(180,100,110,.08)}
.moment-card::before{content:'';position:absolute;top:0;left:0;bottom:0;width:3px;
  background:linear-gradient(180deg,#e8b4b8,#c9546a)}
.moment-icon{font-size:28px;margin-bottom:12px;display:block}
.moment-cat{font-size:10px;letter-spacing:3px;text-transform:uppercase;color:#c97f8a;margin-bottom:6px}
.moment-title{font-family:'Cormorant Garamond',serif;font-size:26px;
  font-weight:400;color:#2a1f1a;margin-bottom:14px}
.moment-date{font-size:11px;color:#b8897e;letter-spacing:1px;margin-bottom:16px}
.moment-story{font-family:'Cormorant Garamond',serif;font-size:18px;
  font-weight:300;line-height:1.9;color:#4a3830}
.moment-media{margin-top:24px;border-radius:3px;overflow:hidden}
.moment-media img{width:100%;max-height:400px;object-fit:cover;border-radius:3px}

/* ── VIDEO ── */
.video-section{background:#1e1210;padding:100px 6vw}
.video-ph{aspect-ratio:16/9;background:#2e1f1a;border-radius:3px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;
  border:1px solid rgba(201,84,106,.15)}
.play-btn{width:56px;height:56px;border:1.5px solid rgba(201,84,106,.5);
  border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-size:18px;color:#c9546a}
.video-lbl{font-size:13px;color:rgba(255,245,240,.5);letter-spacing:1px}

/* ── MUSIC ── */
.music-section{background:#fdf8f4;padding:100px 6vw;
  display:flex;align-items:center;gap:80px;flex-wrap:wrap}
.music-text{flex:1;min-width:280px}
.music-player-wrap{flex:0 0 360px;min-width:280px}
.player-card{background:#fff;border:1px solid rgba(201,127,138,.15);
  border-radius:4px;padding:40px;text-align:center;
  box-shadow:0 4px 24px rgba(180,100,110,.06)}
.player-thumb{width:120px;height:120px;border-radius:50%;
  background:linear-gradient(135deg,#f0d8dd,#e8c0c8);
  margin:0 auto 28px;display:flex;align-items:center;justify-content:center;font-size:36px}
.player-song{font-family:'Cormorant Garamond',serif;font-size:22px;color:#2a1f1a;margin-bottom:4px}
.player-artist{font-size:13px;color:#9a7a72;margin-bottom:20px}

/* ── FINALE ── */
.finale-section{
  background:linear-gradient(160deg,#1e1210,#2e1a18,#1e1210);
  padding:120px 6vw;text-align:center;position:relative;overflow:hidden}
.finale-bg{position:absolute;inset:0;
  background:radial-gradient(ellipse at 50% 50%,rgba(201,84,106,.1) 0%,transparent 70%);
  pointer-events:none}
.finale-label{color:rgba(201,84,106,.7);font-size:11px;letter-spacing:4px;
  text-transform:uppercase;margin-bottom:32px}
.finale-title{font-family:'Cormorant Garamond',serif;font-size:clamp(40px,6vw,72px);
  font-weight:300;color:#fff5f0;line-height:1.2;margin-bottom:48px}
.surprise-box{animation:fadeUp .8s cubic-bezier(.22,1,.36,1) both}
.finale-img-round{width:280px;height:280px;border-radius:50%;object-fit:cover;
  margin:0 auto 48px;display:block;
  border:3px solid rgba(201,84,106,.3);box-shadow:0 0 60px rgba(201,84,106,.2)}
.finale-ph{width:280px;height:280px;border-radius:50%;
  background:linear-gradient(135deg,#3a2520,#2e1a18);
  border:1px solid rgba(201,84,106,.2);display:flex;flex-direction:column;
  align-items:center;justify-content:center;margin:0 auto 48px;font-size:40px;gap:12px}
.surprise-msg{font-family:'Cormorant Garamond',serif;font-size:clamp(22px,3vw,34px);
  font-weight:300;color:#fff5f0;line-height:1.8;max-width:560px;margin:0 auto 16px}
.surprise-sign{font-family:'Cormorant Garamond',serif;font-size:20px;
  font-style:italic;color:#c9546a;margin-top:24px}

/* ── FOOTER ── */
.quote-footer{background:#1e1210;padding:60px 6vw;text-align:center;
  border-top:1px solid rgba(201,84,106,.1)}
.quote-text{font-family:'Cormorant Garamond',serif;font-size:clamp(16px,2.5vw,22px);
  font-weight:300;font-style:italic;color:rgba(255,245,240,.4);
  max-width:600px;margin:0 auto;line-height:1.8}

/* ── CONFETTI ── */
.confetti-wrap{position:fixed;inset:0;pointer-events:none;z-index:9999;overflow:hidden}
.cp{position:absolute;top:-10px;animation:fall linear forwards}
@keyframes fall{to{transform:translateY(110vh) rotate(720deg);opacity:0}}
@keyframes fadeUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.15)}}

/* ── DELETE BTN ── */
.del-zone{border:1px solid rgba(180,60,60,.25);border-radius:4px;
  padding:8px 12px;background:rgba(180,60,60,.04);margin-top:6px}

@media(max-width:768px){
  .hero-img-side{display:none}
  .letter-card{padding:40px 28px}
  .music-section{flex-direction:column;gap:40px}
  .music-player-wrap{flex:1;width:100%}
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# EDIT BAR (fixed top)
# ══════════════════════════════════════════════════════════════════════════════
if EDIT:
    st.markdown('<div class="edit-bar"><span class="edit-bar-title">✏️ Düzenleme Modu</span><span class="edit-badge">AÇIK</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="page-offset"></div>', unsafe_allow_html=True)

# Edit toggle button — top right via columns
_c1, _c2, _c3 = st.columns([6, 1, 1])
with _c2:
    edit_label = "✏️ Düzenle" if not EDIT else "✅ Kapat"
    if st.button(edit_label, key="toggle_edit", use_container_width=True):
        st.session_state["edit_mode"] = not EDIT
        save_data(DATA)
        st.rerun()
with _c3:
    pass  # spacer


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

if DATA["hero_img"]:
    st.markdown(f'<img src="{DATA["hero_img"]}" style="width:100%;height:100%;object-fit:cover;filter:brightness(.95) saturate(.9)">', unsafe_allow_html=True)
else:
    st.markdown('<div class="hero-ph"><span>📸</span><p>AİLE FOTOĞRAFI</p></div>', unsafe_allow_html=True)

st.markdown("</div></section><div class='divider'></div>", unsafe_allow_html=True)

if EDIT:
    with st.expander("📸 Hero Fotoğrafı", expanded=False):
        col_h1, col_h2 = st.columns([3, 1])
        with col_h1:
            f = st.file_uploader("Hero fotoğrafı yükle", type=["jpg","jpeg","png"],
                                 key="up_hero_main", label_visibility="collapsed")
            if f:
                DATA["hero_img"] = file_to_data_url(f)
                save_data(DATA)
                st.rerun()
        with col_h2:
            if DATA["hero_img"] and st.button("🗑 Sil", key="del_hero"):
                DATA["hero_img"] = None
                save_data(DATA)
                st.rerun()


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

# Render memory cards
mem_cols = st.columns(4, gap="medium")
for i, mem in enumerate(DATA["memories"]):
    img_html = (f'<img src="{mem["img"]}" style="width:100%;height:100%;object-fit:cover">'
                if mem["img"] else '<div class="t-card-ph">📸</div>')
    st.markdown(f"""
    <div class="t-card" style="animation:fadeUp .8s {i*0.15}s cubic-bezier(.22,1,.36,1) both">
      <div class="t-card-img">
        {img_html}
        <div class="t-card-num">{mem['num']}</div>
      </div>
      <div class="t-card-body">
        <p class="t-card-date">{mem['date']}</p>
        <h3 class="t-card-title">{mem['title']}</h3>
        <p class="t-card-desc">{mem['desc']}</p>
      </div>
    </div>""", unsafe_allow_html=True)

st.markdown("</section><div class='divider'></div>", unsafe_allow_html=True)

# Edit panel for memories
if EDIT:
    with st.expander("📷 Anı Kartlarını Düzenle", expanded=False):
        for i, mem in enumerate(DATA["memories"]):
            st.markdown(f"**{mem['num']} — {mem['title']}**")
            ec1, ec2, ec3 = st.columns([3, 1, 1])
            with ec1:
                f = st.file_uploader(f"Fotoğraf", type=["jpg","jpeg","png"],
                                     key=f"up_mem_{mem['id']}", label_visibility="collapsed")
                if f:
                    DATA["memories"][i]["img"] = file_to_data_url(f)
                    save_data(DATA)
                    st.rerun()
            with ec2:
                if mem["img"] and st.button("🗑 Sil", key=f"del_mem_{mem['id']}"):
                    DATA["memories"][i]["img"] = None
                    save_data(DATA)
                    st.rerun()
            with ec3:
                if mem["img"]:
                    st.success("✓ Yüklü")
            st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# 4. ANLAR — UZUN HİKAYELER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<section id="moments" class="moments-section">
  <div style="margin-bottom:64px">
    <p class="sec-label">Büyüme Yolculuğu</p>
    <h2 class="sec-title">İyi günler, kötü günler,<br>hepsi bizim</h2>
  </div>
""", unsafe_allow_html=True)

for mo in DATA["moments"]:
    img_html = ""
    if mo.get("img"):
        img_html = f'<div class="moment-media"><img src="{mo["img"]}"></div>'
    vid_html = ""
    if mo.get("video"):
        vid_html = '<div class="moment-media" style="margin-top:16px">[video]</div>'

    st.markdown(f"""
    <div class="moment-card">
      <span class="moment-icon">{mo['icon']}</span>
      <p class="moment-cat">{mo['category']}</p>
      <h3 class="moment-title">{mo['title']}</h3>
      <p class="moment-date">{mo['date']}</p>
      <p class="moment-story">{mo['story']}</p>
      {img_html}
    </div>""", unsafe_allow_html=True)

    # Inline video render (Streamlit handles it)
    if mo.get("video"):
        st.video(mo["video"])

st.markdown("</section><div class='divider'></div>", unsafe_allow_html=True)

# Edit moments
if EDIT:
    with st.expander("✨ Büyüme Anlarını Düzenle", expanded=False):
        for i, mo in enumerate(DATA["moments"]):
            st.markdown(f"**{mo['icon']} {mo['title']}**")
            mc1, mc2, mc3 = st.columns([2, 2, 1])
            with mc1:
                st.caption("📷 Fotoğraf")
                f_img = st.file_uploader("Fotoğraf", type=["jpg","jpeg","png"],
                                         key=f"up_mo_img_{mo['id']}", label_visibility="collapsed")
                if f_img:
                    DATA["moments"][i]["img"] = file_to_data_url(f_img)
                    save_data(DATA)
                    st.rerun()
                if mo.get("img") and st.button("🗑 Foto sil", key=f"del_mo_img_{mo['id']}"):
                    DATA["moments"][i]["img"] = None
                    save_data(DATA)
                    st.rerun()
            with mc2:
                st.caption("🎬 Video")
                f_vid = st.file_uploader("Video", type=["mp4","mov"],
                                         key=f"up_mo_vid_{mo['id']}", label_visibility="collapsed")
                if f_vid:
                    DATA["moments"][i]["video"] = file_to_data_url(f_vid)
                    save_data(DATA)
                    st.rerun()
                if mo.get("video") and st.button("🗑 Video sil", key=f"del_mo_vid_{mo['id']}"):
                    DATA["moments"][i]["video"] = None
                    save_data(DATA)
                    st.rerun()
            with mc3:
                status = []
                if mo.get("img"):   status.append("📷")
                if mo.get("video"): status.append("🎬")
                if status: st.success(" ".join(status) + " Yüklü")
            st.divider()

        # Add new moment
        st.markdown("**➕ Yeni An Ekle**")
        with st.form("add_moment_form"):
            nc1, nc2 = st.columns(2)
            new_icon  = nc1.text_input("İkon (emoji)", value="⭐")
            new_cat   = nc2.text_input("Kategori", value="Özel Anlar")
            new_title = st.text_input("Başlık")
            nd1, nd2  = st.columns(2)
            new_date  = nd1.text_input("Tarih", value="2025")
            new_story = st.text_area("Hikaye", height=100)
            if st.form_submit_button("✅ Ekle"):
                if new_title and new_story:
                    DATA["moments"].append({
                        "id": str(uuid.uuid4())[:8],
                        "icon": new_icon, "category": new_cat,
                        "title": new_title, "date": new_date,
                        "story": new_story, "img": None, "video": None
                    })
                    save_data(DATA)
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

vcols = st.columns(len(DATA["videos"]), gap="medium")
for i, vid in enumerate(DATA["videos"]):
    with vcols[i]:
        if vid.get("url"):
            st.video(vid["url"])
            st.markdown(f'<p style="color:rgba(255,245,240,.5);font-size:12px;text-align:center;margin-top:6px;letter-spacing:1px">{vid["label"]}</p>',
                        unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="video-ph">
              <div class="play-btn">▶</div>
              <p class="video-lbl">{vid['label']}</p>
            </div>""", unsafe_allow_html=True)

st.markdown("</section><div class='divider' style='background:linear-gradient(90deg,transparent,rgba(201,84,106,.1),transparent)'></div>", unsafe_allow_html=True)

if EDIT:
    with st.expander("🎬 Videoları Düzenle", expanded=False):
        for i, vid in enumerate(DATA["videos"]):
            st.markdown(f"**{vid['label']}**")
            vc1, vc2, vc3 = st.columns([3, 1, 1])
            with vc1:
                f = st.file_uploader("Video yükle", type=["mp4","mov","avi"],
                                     key=f"up_vid_{vid['id']}", label_visibility="collapsed")
                if f:
                    DATA["videos"][i]["url"] = file_to_data_url(f)
                    save_data(DATA)
                    st.rerun()
            with vc2:
                if vid.get("url") and st.button("🗑 Sil", key=f"del_vid_{vid['id']}"):
                    DATA["videos"][i]["url"] = None
                    save_data(DATA)
                    st.rerun()
            with vc3:
                if vid.get("url"): st.success("✓ Yüklü")
            st.divider()

        # Add video slot
        with st.form("add_video_form"):
            new_vl = st.text_input("Video adı/açıklaması")
            if st.form_submit_button("➕ Video Slotu Ekle"):
                if new_vl:
                    DATA["videos"].append({"id": str(uuid.uuid4())[:8], "label": new_vl, "url": None})
                    save_data(DATA)
                    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# 6. MÜZİK
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<section id="music" class="music-section">
  <div class="music-text">
    <p class="sec-label">Müziğimiz</p>
    <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(36px,5vw,60px);
      font-weight:300;color:#1e1210;line-height:1.1">
      Bizim<br>şarkımız
    </h2>
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

if DATA.get("music_url"):
    st.audio(DATA["music_url"])
else:
    st.markdown('<p style="font-size:13px;color:#c97f8a;text-align:center;padding:8px 0">Henüz şarkı yüklenmedi</p>',
                unsafe_allow_html=True)

st.markdown("</div></div></div></section><div class='divider'></div>", unsafe_allow_html=True)

if EDIT:
    with st.expander("🎵 Müziği Düzenle", expanded=False):
        mu1, mu2 = st.columns([3, 1])
        with mu1:
            fm = st.file_uploader("Müzik yükle", type=["mp3","wav","ogg","m4a"],
                                  key="up_music_main", label_visibility="collapsed")
            if fm:
                DATA["music_url"] = file_to_data_url(fm)
                save_data(DATA)
                st.rerun()
        with mu2:
            if DATA.get("music_url") and st.button("🗑 Müziği Sil", key="del_music"):
                DATA["music_url"] = None
                save_data(DATA)
                st.rerun()


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
            st.markdown('<span style="color:#c97f8a;font-size:10px;letter-spacing:2px;text-transform:uppercase">📎 Final Fotoğrafı</span>', unsafe_allow_html=True)
            ff = st.file_uploader("Final fotoğrafı", type=["jpg","jpeg","png"],
                                  key="up_finale_edit", label_visibility="collapsed")
            if ff:
                DATA["finale_img"] = file_to_data_url(ff)
                save_data(DATA)
                st.rerun()
            if DATA.get("finale_img") and st.button("🗑 Sil", key="del_finale_img"):
                DATA["finale_img"] = None
                save_data(DATA)
                st.rerun()

    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        if st.button("Son Mesaj ❤️", key="surprise_btn", use_container_width=True):
            st.session_state["show_surprise"] = True
            st.session_state["show_confetti"] = True
            st.rerun()

else:
    import random as _rand
    if st.session_state["show_confetti"]:
        colors = ["#c9546a","#e8b4b8","#f5c8cc","#fff5f0","#b8495e","#f0d8dd"]
        pieces = "".join([
            f'<div class="cp" style="left:{_rand.randint(0,100)}%;'
            f'width:{_rand.randint(6,13)}px;height:{_rand.randint(6,13)}px;'
            f'background:{colors[i%len(colors)]};'
            f'animation-duration:{_rand.uniform(2.5,5):.1f}s;'
            f'animation-delay:{_rand.uniform(0,2):.1f}s;'
            f'border-radius:{"50%" if i%3==0 else "1px"}"></div>'
            for i in range(80)
        ])
        st.markdown(f'<div class="confetti-wrap">{pieces}</div>', unsafe_allow_html=True)
        st.session_state["show_confetti"] = False

    if DATA.get("finale_img"):
        st.markdown(f'<img class="finale-img-round" src="{DATA["finale_img"]}">', unsafe_allow_html=True)
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
# FOOTER + TÜM VERİLERİ SİL
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<footer class="quote-footer">
  <p class="quote-text">"Dünyanın tüm çiçeklerini toplasam, senin bir gülüşüne değişmem anne."</p>
</footer>
""", unsafe_allow_html=True)

# ── Tüm verileri sil (en altta, edit moddan bağımsız her zaman görünür) ──
st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
st.markdown("---")

col_del1, col_del2, col_del3 = st.columns([3, 2, 3])
with col_del2:
    if not st.session_state["confirm_delete_all"]:
        if st.button("🗑 Tüm Yüklenen Verileri Sil", key="ask_delete_all",
                     use_container_width=True, type="secondary"):
            st.session_state["confirm_delete_all"] = True
            st.rerun()
    else:
        st.warning("Emin misin? Bu işlem geri alınamaz.")
        d1, d2 = st.columns(2)
        if d1.button("✅ Evet, sil", key="confirm_yes", use_container_width=True, type="primary"):
            clear_all_data()
            st.session_state["data"] = json.loads(json.dumps(DEFAULT_DATA))
            st.session_state["show_surprise"] = False
            st.session_state["confirm_delete_all"] = False
            st.rerun()
        if d2.button("❌ İptal", key="confirm_no", use_container_width=True):
            st.session_state["confirm_delete_all"] = False
            st.rerun()

st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
