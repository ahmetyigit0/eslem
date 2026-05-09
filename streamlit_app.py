import streamlit as st
import base64
import random

# ─────────────────────────────────────────────────────────────────────────────
# MEDYA AYARLARI — Siteyi bitirince buradan yönet
# ─────────────────────────────────────────────────────────────────────────────
# show_upload = True  → Upload butonu göster (test/düzenleme modu)
# show_upload = False → Upload butonu gizle  (yayın modu)
# file = "dosya.jpg"  → Sabit dosya kullan   (yayın modu)
# ─────────────────────────────────────────────────────────────────────────────
MEDIA = {
    "hero":     {"show_upload": True, "file": None},  # Örn: "hero.jpg"
    "memory_1": {"show_upload": True, "file": None},  # "uraz_dogdu.jpg"
    "memory_2": {"show_upload": True, "file": None},  # "aile_foto.jpg"
    "memory_3": {"show_upload": True, "file": None},  # "tatil.jpg"
    "memory_4": {"show_upload": True, "file": None},  # "kahkaha.jpg"
    "video_1":  {"show_upload": True, "file": None},  # "uraz_ses.mp4"
    "video_2":  {"show_upload": True, "file": None},  # "uyku.mp4"
    "video_3":  {"show_upload": True, "file": None},  # "park.mp4"
    "music":    {"show_upload": True, "file": None},  # "sarki.mp3"
    "finale":   {"show_upload": True, "file": None},  # "final_foto.jpg"
}

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="İyi ki varsın Anne ❤️",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Helpers ───────────────────────────────────────────────────────────────────
def to_data_url(uploaded_file):
    data = uploaded_file.read()
    b64  = base64.b64encode(data).decode()
    return f"data:{uploaded_file.type};base64,{b64}"

def file_to_data_url(path, mime="image/jpeg"):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{b64}"

def get_media(key, accept_types=["jpg","jpeg","png"], label="Fotoğraf yükle"):
    """
    Önce sabit dosya → sonra session state → sonra upload widget.
    Döndürür: data_url veya None
    """
    cfg = MEDIA.get(key, {})

    # 1) Sabit dosya
    if cfg.get("file"):
        ext = cfg["file"].rsplit(".", 1)[-1].lower()
        mime_map = {"mp4":"video/mp4","mov":"video/mp4","mp3":"audio/mpeg",
                    "wav":"audio/wav","ogg":"audio/ogg","m4a":"audio/mp4"}
        mime = mime_map.get(ext, "image/jpeg")
        return file_to_data_url(cfg["file"], mime)

    # 2) Session state'te daha önce yüklendi mi?
    if f"media_{key}" in st.session_state:
        return st.session_state[f"media_{key}"]

    # 3) Upload widget
    if cfg.get("show_upload", False):
        uploaded = st.file_uploader(label, type=accept_types,
                                    key=f"uploader_{key}",
                                    label_visibility="collapsed")
        if uploaded:
            url = to_data_url(uploaded)
            st.session_state[f"media_{key}"] = url
            return url

    return None


# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [data-testid="stAppViewContainer"] {
    background: #fdf8f4 !important; color: #2a1f1a !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stHeader"], [data-testid="stToolbar"], footer,
.viewerBadge_container__r5tak { display: none !important; }
[data-testid="stAppViewContainer"] > .main > div { padding: 0 !important; max-width: 100% !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #e8b4b8; border-radius: 2px; }

/* Upload widget stili */
.upload-zone {
    background: rgba(253,248,244,0.9);
    border: 1.5px dashed rgba(201,127,138,0.4);
    border-radius: 6px;
    padding: 12px 16px;
    margin: 8px 0 0;
}
.upload-label {
    display: block;
    font-size: 10px; letter-spacing: 2.5px; text-transform: uppercase;
    color: #c97f8a; margin-bottom: 6px;
}
[data-testid="stFileUploader"] { padding: 0 !important; }
[data-testid="stFileUploader"] section {
    padding: 10px !important;
    border-radius: 4px !important;
    background: rgba(253,248,244,0.5) !important;
    border-color: rgba(201,127,138,0.3) !important;
}

/* HERO */
.hero-wrap {
    position: relative; width: 100%; min-height: 100vh;
    background: linear-gradient(135deg, #fff9f5 0%, #fdeef0 40%, #f9e8ee 100%);
    display: flex; align-items: center; overflow: hidden;
}
.hero-bg-c { position: absolute; border-radius: 50%;
    background: radial-gradient(circle, rgba(237,176,185,0.18) 0%, transparent 70%); }
.hero-content {
    position: relative; z-index: 2; max-width: 640px; padding: 80px 6vw;
    animation: fadeUp 1.2s cubic-bezier(.22,1,.36,1) both;
}
.hero-eyebrow { font-size: 12px; letter-spacing: 3px; text-transform: uppercase; color: #c97f8a; margin-bottom: 20px; }
.hero-title { font-family: 'Cormorant Garamond', serif; font-size: clamp(52px,8vw,96px); font-weight: 300; line-height: 1.05; color: #1e1210; margin-bottom: 28px; }
.hero-title em { color: #c9546a; font-style: italic; }
.hero-sub { font-size: 16px; font-weight: 300; color: #7a5a52; line-height: 1.7; max-width: 420px; margin-bottom: 48px; }
.hero-img-side { position: absolute; right: 0; top: 0; bottom: 0; width: 52%; overflow: hidden; }
.hero-img-side img { width: 100%; height: 100%; object-fit: cover; filter: brightness(.95) saturate(.9); }
.hero-ph { width: 100%; height: 100%; background: linear-gradient(160deg, #f0d8dd, #e8c8ce, #dbb5bc);
    display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px; }
.hero-ph span { font-size: 48px; opacity: .4; }
.hero-ph p { font-size: 13px; color: #9a6872; letter-spacing: 1px; }

/* DIVIDER */
.divider { width: 100%; height: 1px; background: linear-gradient(90deg, transparent, rgba(201,84,106,0.2), transparent); }

/* LETTER */
.letter-section { background: #fff; padding: 100px 6vw; }
.letter-label { font-size: 11px; letter-spacing: 4px; text-transform: uppercase; color: #c97f8a; margin-bottom: 40px; display: flex; align-items: center; gap: 16px; }
.letter-label::after { content: ''; flex: 1; height: 1px; background: linear-gradient(90deg, rgba(201,127,138,0.3), transparent); }
.letter-card { max-width: 680px; margin: 0 auto; background: #fffcf9; border: 1px solid rgba(201,127,138,0.12); border-radius: 4px; padding: 64px 72px; position: relative; box-shadow: 0 8px 48px rgba(180,100,110,0.06); }
.letter-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #e8b4b8, #c9546a, #e8b4b8); }
.letter-date { font-size: 12px; color: #b8897e; letter-spacing: 1px; margin-bottom: 32px; }
.letter-salutation { font-family: 'Cormorant Garamond', serif; font-size: 28px; font-style: italic; color: #2a1f1a; margin-bottom: 24px; }
.letter-body { font-family: 'Cormorant Garamond', serif; font-size: 20px; font-weight: 300; line-height: 2; color: #4a3830; }
.letter-body p { margin-bottom: 16px; }
.letter-sign { margin-top: 40px; font-family: 'Cormorant Garamond', serif; font-size: 22px; font-style: italic; color: #c9546a; }
.letter-heart { display: inline-block; animation: pulse 1.8s ease-in-out infinite; }

/* TIMELINE */
.timeline-section { background: #fdf8f4; padding: 100px 6vw; }
.section-label { font-size: 11px; letter-spacing: 4px; text-transform: uppercase; color: #c97f8a; margin-bottom: 16px; }
.section-title { font-family: 'Cormorant Garamond', serif; font-size: clamp(36px,5vw,60px); font-weight: 300; color: #1e1210; line-height: 1.1; }
.timeline-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 32px; margin-top: 0; }
.t-card { background: #fff; border-radius: 3px; overflow: hidden; border: 1px solid rgba(201,127,138,0.1); transition: transform .4s cubic-bezier(.22,1,.36,1), box-shadow .4s; }
.t-card:hover { transform: translateY(-6px); box-shadow: 0 20px 60px rgba(180,100,110,0.12); }
.t-card-img { width: 100%; height: 200px; overflow: hidden; position: relative; }
.t-card-img img { width: 100%; height: 100%; object-fit: cover; }
.t-card-ph { width: 100%; height: 100%; background: linear-gradient(160deg, #f5e0e4, #ead0d5); display: flex; align-items: center; justify-content: center; font-size: 32px; color: rgba(180,100,110,0.3); }
.t-card-num { position: absolute; top: 12px; left: 12px; background: rgba(255,255,255,.9); border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 500; color: #c9546a; }
.t-card-body { padding: 28px; }
.t-card-date { font-size: 11px; letter-spacing: 2px; color: #c97f8a; margin-bottom: 8px; }
.t-card-title { font-family: 'Cormorant Garamond', serif; font-size: 22px; color: #2a1f1a; margin-bottom: 10px; }
.t-card-desc { font-size: 14px; color: #7a5a52; line-height: 1.6; font-weight: 300; }

/* VIDEO */
.video-section { background: #1e1210; padding: 100px 6vw; }
.video-ph { aspect-ratio: 16/9; background: #2e1f1a; border-radius: 3px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; border: 1px solid rgba(201,84,106,0.15); }
.play-btn { width: 56px; height: 56px; border: 1.5px solid rgba(201,84,106,0.5); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; color: #c9546a; }
.video-lbl { font-size: 13px; color: rgba(255,245,240,0.5); letter-spacing: 1px; }

/* MUSIC */
.music-section { background: #fff; padding: 100px 6vw; display: flex; align-items: center; gap: 80px; flex-wrap: wrap; }
.music-text { flex: 1; min-width: 280px; }
.music-player-wrap { flex: 0 0 360px; min-width: 280px; }
.player-card { background: #fdf8f4; border: 1px solid rgba(201,127,138,0.15); border-radius: 4px; padding: 40px; text-align: center; }
.player-thumb { width: 120px; height: 120px; border-radius: 50%; background: linear-gradient(135deg, #f0d8dd, #e8c0c8); margin: 0 auto 28px; display: flex; align-items: center; justify-content: center; font-size: 36px; }
.player-song { font-family: 'Cormorant Garamond', serif; font-size: 22px; color: #2a1f1a; margin-bottom: 4px; }
.player-artist { font-size: 13px; color: #9a7a72; margin-bottom: 20px; }

/* FINALE */
.finale-section { background: linear-gradient(160deg, #1e1210, #2e1a18, #1e1210); padding: 120px 6vw; text-align: center; position: relative; overflow: hidden; }
.finale-bg { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 50%, rgba(201,84,106,0.1) 0%, transparent 70%); pointer-events: none; }
.finale-label { color: rgba(201,84,106,0.7); font-size: 11px; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 32px; }
.finale-title { font-family: 'Cormorant Garamond', serif; font-size: clamp(40px,6vw,72px); font-weight: 300; color: #fff5f0; line-height: 1.2; margin-bottom: 48px; }
.surprise-box { animation: fadeUp .8s cubic-bezier(.22,1,.36,1) both; }
.finale-img-round { width: 280px; height: 280px; border-radius: 50%; object-fit: cover; margin: 0 auto 48px; display: block; border: 3px solid rgba(201,84,106,0.3); box-shadow: 0 0 60px rgba(201,84,106,0.2); }
.finale-ph { width: 280px; height: 280px; border-radius: 50%; background: linear-gradient(135deg, #3a2520, #2e1a18); border: 1px solid rgba(201,84,106,0.2); display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 0 auto 48px; font-size: 40px; gap: 12px; }
.surprise-msg { font-family: 'Cormorant Garamond', serif; font-size: clamp(22px,3vw,34px); font-weight: 300; color: #fff5f0; line-height: 1.8; max-width: 560px; margin: 0 auto 16px; }
.surprise-sign { font-family: 'Cormorant Garamond', serif; font-size: 20px; font-style: italic; color: #c9546a; margin-top: 24px; }

/* FOOTER */
.quote-footer { background: #fdf8f4; padding: 60px 6vw; text-align: center; border-top: 1px solid rgba(201,127,138,0.1); }
.quote-text { font-family: 'Cormorant Garamond', serif; font-size: clamp(16px,2.5vw,22px); font-weight: 300; font-style: italic; color: #9a7a72; max-width: 600px; margin: 0 auto; line-height: 1.8; }

/* CONFETTI */
.confetti-wrap { position: fixed; inset: 0; pointer-events: none; z-index: 9999; overflow: hidden; }
.cp { position: absolute; top: -10px; animation: fall linear forwards; }
@keyframes fall { to { transform: translateY(110vh) rotate(720deg); opacity: 0; } }
@keyframes fadeUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
@keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.15); } }

@media (max-width: 768px) {
    .hero-img-side { display: none; }
    .letter-card { padding: 40px 28px; }
    .music-section { flex-direction: column; gap: 40px; }
    .music-player-wrap { flex: 1; width: 100%; }
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [("show_surprise", False), ("show_confetti", False)]:
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════════════
# 1. HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<section class="hero-wrap">
  <div class="hero-bg-c" style="width:700px;height:700px;top:-200px;right:-100px"></div>
  <div class="hero-bg-c" style="width:400px;height:400px;bottom:-100px;left:-80px"></div>
  <div class="hero-content">
    <p class="hero-eyebrow">Anneler Günü · 2025</p>
    <h1 class="hero-title">İyi ki<br>varsın<br><em>Anne</em> ❤️</h1>
    <p class="hero-sub">Bugün sana küçük ama özel bir sürpriz hazırladık.<br>Uraz ve Ahmet'ten, sana…</p>
  </div>
  <div class="hero-img-side">
""", unsafe_allow_html=True)

hero_url = get_media("hero", ["jpg","jpeg","png"], "Hero fotoğrafı")
if hero_url:
    st.markdown(f'<img src="{hero_url}" style="width:100%;height:100%;object-fit:cover;filter:brightness(.95) saturate(.9)">', unsafe_allow_html=True)
else:
    st.markdown('<div class="hero-ph"><span>📸</span><p>AİLE FOTOĞRAFI</p></div>', unsafe_allow_html=True)

st.markdown("</div></section>", unsafe_allow_html=True)

# Hero upload paneli (sadece show_upload=True ise ve henüz yüklenmemişse)
if MEDIA["hero"]["show_upload"] and not hero_url:
    with st.expander("📸 Hero fotoğrafı yükle (sağ panel)", expanded=False):
        st.caption("Yüklendikten sonra bu kutu kaybolur.")
        get_media("hero", ["jpg","jpeg","png"], "Fotoğraf seç")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 2. MEKTUP
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<section id="letter" class="letter-section">
  <div class="letter-label">Uraz'dan Mektup</div>
  <div class="letter-card">
    <p class="letter-date">Mayıs 2025</p>
    <p class="letter-salutation">Merhaba anne,</p>
    <div class="letter-body">
      <p>Ben henüz konuşamıyorum ama sana her gün teşekkür etmek istiyorum.</p>
      <p>Beni sabırla uyuttuğun,<br>beni güldürdüğün,<br>
         ve bana sevginin ne olduğunu gösterdiğin için teşekkür ederim.</p>
      <p>Dünyaya gözlerimi ilk açtığımda ilk gördüğüm sendin.<br>
         Ve o andan beri sen benim her şeyimsin.</p>
      <p>Seni çok seviyorum.</p>
    </div>
    <div class="letter-sign">Uraz <span class="letter-heart">❤️</span></div>
  </div>
</section>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 3. ANI TİMLİNE
# ══════════════════════════════════════════════════════════════════════════════
memories = [
    ("memory_1", "01", "Ekim 2024",  "Uraz Doğdu",            "Küçük ellerin ilk kez senin parmağını tuttuğu an — dünyanın durduğu an."),
    ("memory_2", "02", "Kasım 2024", "İlk Aile Fotoğrafımız", "Üçümüz, bir çatı altında, yeni bir hikâyenin başında."),
    ("memory_3", "03", "Şubat 2025", "İlk Tatilimiz",         "Deniz kokusu, bebek sesi ve senin gülüşün. Mükemmel bir tablo."),
    ("memory_4", "04", "Mart 2025",  "İlk Kahkahamız",        "Uraz ilk kez güldüğünde sen de güldün. O ses hâlâ kulaklarımızda."),
]

st.markdown("""
<section id="memories" class="timeline-section">
  <div style="margin-bottom:64px">
    <p class="section-label">Anılarımız</p>
    <h2 class="section-title">Birlikte yazdığımız<br>en güzel sayfalar</h2>
  </div>
""", unsafe_allow_html=True)

cols = st.columns(4, gap="medium")
for i, (key, num, date, title, desc) in enumerate(memories):
    with cols[i]:
        # Upload widget
        if MEDIA[key]["show_upload"]:
            st.markdown(f'<span class="upload-label">📎 {title}</span>', unsafe_allow_html=True)
        img_url = get_media(key, ["jpg","jpeg","png"], f"{title} fotoğrafı")

    img_html = (f'<img src="{img_url}" style="width:100%;height:100%;object-fit:cover">'
                if img_url else '<div class="t-card-ph">📸</div>')
    st.markdown(f"""
    <div class="t-card" style="animation:fadeUp .8s {i*0.15}s cubic-bezier(.22,1,.36,1) both">
      <div class="t-card-img">
        {img_html}
        <div class="t-card-num">{num}</div>
      </div>
      <div class="t-card-body">
        <p class="t-card-date">{date}</p>
        <h3 class="t-card-title">{title}</h3>
        <p class="t-card-desc">{desc}</p>
      </div>
    </div>""", unsafe_allow_html=True)

st.markdown("</section><div class='divider'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 4. VİDEOLAR
# ══════════════════════════════════════════════════════════════════════════════
video_items = [
    ("video_1", "Uraz'ın İlk Sesi"),
    ("video_2", "Birlikte Uyuyan Anımız"),
    ("video_3", "Parkta Bir Sabah"),
]

st.markdown("""
<section id="videos" class="video-section">
  <p class="section-label" style="color:#c9546a">Videolar</p>
  <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(36px,5vw,60px);font-weight:300;color:#fff5f0;line-height:1.1;margin-bottom:48px">
    Küçük mutluluğumuzun<br>en tatlı halleri
  </h2>
""", unsafe_allow_html=True)

vcols = st.columns(3, gap="medium")
for i, (key, label) in enumerate(video_items):
    with vcols[i]:
        if MEDIA[key]["show_upload"]:
            st.markdown(f'<span class="upload-label" style="color:#c97f8a">📎 {label}</span>', unsafe_allow_html=True)
        vid_url = get_media(key, ["mp4","mov","avi"], f"{label} videosu")
        if vid_url:
            st.video(vid_url)
            st.markdown(f'<p style="color:rgba(255,245,240,.5);font-size:12px;text-align:center;margin-top:6px;letter-spacing:1px">{label}</p>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="video-ph">
              <div class="play-btn">▶</div>
              <p class="video-lbl">{label}</p>
            </div>""", unsafe_allow_html=True)

st.markdown("""
</section>
<div class="divider" style="background:linear-gradient(90deg,transparent,rgba(201,84,106,0.1),transparent)"></div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 5. MÜZİK
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<section id="music" class="music-section">
  <div class="music-text">
    <p class="section-label">Müziğimiz</p>
    <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(36px,5vw,60px);font-weight:300;color:#1e1210;line-height:1.1">
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
      <p class="player-artist">Eslem, Ahmet & Uraz</p>
""", unsafe_allow_html=True)

if MEDIA["music"]["show_upload"]:
    st.markdown('<span class="upload-label">📎 Şarkıyı yükle</span>', unsafe_allow_html=True)
music_url = get_media("music", ["mp3","wav","ogg","m4a"], "Müzik dosyası seç")
if music_url:
    st.audio(music_url)
else:
    st.markdown('<p style="font-size:13px;color:#c97f8a;text-align:center">Henüz şarkı yüklenmedi</p>', unsafe_allow_html=True)

st.markdown("</div></div></div></section><div class='divider'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 6. FİNAL SÜRPRİZ
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<section id="finale" class="finale-section"><div class="finale-bg"></div>', unsafe_allow_html=True)

if not st.session_state.show_surprise:
    st.markdown("""
    <p class="finale-label">Son Sürpriz</p>
    <h2 class="finale-title">Hazır mısın,<br>Eslem?</h2>
    """, unsafe_allow_html=True)

    # Finale fotoğrafı upload (gizli, önceden yüklensin)
    if MEDIA["finale"]["show_upload"]:
        fc1, fc2, fc3 = st.columns([2, 2, 2])
        with fc2:
            st.markdown('<span class="upload-label" style="color:#c97f8a;text-align:center;display:block">📎 Final fotoğrafı yükle</span>', unsafe_allow_html=True)
            get_media("finale", ["jpg","jpeg","png"], "Aile fotoğrafı seç")

    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        if st.button("Son Mesaj ❤️", key="surprise_btn", use_container_width=True):
            st.session_state.show_surprise = True
            st.session_state.show_confetti = True
            st.rerun()

else:
    # Konfeti
    if st.session_state.show_confetti:
        colors = ["#c9546a","#e8b4b8","#f5c8cc","#fff5f0","#b8495e","#f0d8dd"]
        pieces = "".join([
            f'<div class="cp" style="left:{random.randint(0,100)}%;'
            f'width:{random.randint(6,13)}px;height:{random.randint(6,13)}px;'
            f'background:{colors[i%len(colors)]};'
            f'animation-duration:{random.uniform(2.5,5):.1f}s;'
            f'animation-delay:{random.uniform(0,2):.1f}s;'
            f'border-radius:{"50%" if i%3==0 else "1px"}"></div>'
            for i in range(70)
        ])
        st.markdown(f'<div class="confetti-wrap">{pieces}</div>', unsafe_allow_html=True)
        st.session_state.show_confetti = False

    # Final fotoğrafı
    finale_url = get_media("finale", ["jpg","jpeg","png"], "Aile fotoğrafı")
    if finale_url:
        st.markdown(f'<img class="finale-img-round" src="{finale_url}">', unsafe_allow_html=True)
    else:
        st.markdown('<div class="finale-ph"><span>📸</span><p style="font-size:12px;color:rgba(255,245,240,.3)">AİLE FOTOĞRAFI</p></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="surprise-box">
      <p class="finale-label">Eslem'e, Uraz & Ahmet'ten</p>
      <div class="surprise-msg">
        Bazı insanlar anne olur.<br>
        <em>Sen bizim yuvamız oldun.</em><br><br>
        Her sabah uyanışımız, her gülüşümüz,<br>
        her küçük anımız — hepsi seninle anlam kazandı.
      </div>
      <div class="surprise-sign">Seni çok seviyoruz &nbsp;❤️<br>Uraz & Ahmet</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</section>", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<footer class="quote-footer">
  <p class="quote-text">"Dünyanın tüm çiçeklerini toplasam, senin bir gülüşüne değişmem anne."</p>
</footer>
""", unsafe_allow_html=True)
