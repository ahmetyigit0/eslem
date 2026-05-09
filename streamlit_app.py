import streamlit as st
import base64
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="İyi ki varsın Anne ❤️",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #fdf8f4 !important;
    color: #2a1f1a !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Hide Streamlit chrome */
[data-testid="stHeader"],
[data-testid="stToolbar"],
footer,
.viewerBadge_container__r5tak,
.st-emotion-cache-zq5wmm { display: none !important; }

/* Remove default padding */
[data-testid="stAppViewContainer"] > .main > div {
    padding: 0 !important;
    max-width: 100% !important;
}
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #fdf8f4; }
::-webkit-scrollbar-thumb { background: #e8b4b8; border-radius: 2px; }

/* ── SECTION WRAPPER ── */
.section {
    width: 100%;
    padding: 80px 6vw;
}

/* ── HERO ── */
.hero-wrap {
    position: relative;
    width: 100%;
    min-height: 100vh;
    background: linear-gradient(135deg, #fff9f5 0%, #fdeef0 40%, #f9e8ee 100%);
    display: flex;
    align-items: center;
    overflow: hidden;
}
.hero-bg-circle {
    position: absolute;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(237,176,185,0.18) 0%, transparent 70%);
}
.hero-bg-circle.c1 { width: 700px; height: 700px; top: -200px; right: -100px; }
.hero-bg-circle.c2 { width: 400px; height: 400px; bottom: -100px; left: -80px; }

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 640px;
    padding: 80px 6vw;
    animation: fadeUp 1.2s cubic-bezier(.22,1,.36,1) both;
}
.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 12px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #c97f8a;
    margin-bottom: 20px;
}
.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(52px, 8vw, 96px);
    font-weight: 300;
    line-height: 1.05;
    color: #1e1210;
    margin-bottom: 28px;
}
.hero-title span { color: #c9546a; font-style: italic; }
.hero-sub {
    font-size: 16px;
    font-weight: 300;
    color: #7a5a52;
    line-height: 1.7;
    max-width: 420px;
    margin-bottom: 48px;
}
.hero-cta {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    font-size: 13px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #c9546a;
    text-decoration: none;
    border-bottom: 1px solid rgba(201,84,106,0.3);
    padding-bottom: 4px;
    cursor: pointer;
    transition: gap .3s;
}
.hero-cta:hover { gap: 18px; }
.hero-image-side {
    position: absolute;
    right: 0; top: 0; bottom: 0;
    width: 52%;
    overflow: hidden;
}
.hero-image-side img {
    width: 100%; height: 100%;
    object-fit: cover;
    filter: brightness(.95) saturate(.9);
}
.hero-image-placeholder {
    width: 100%; height: 100%;
    background: linear-gradient(160deg, #f0d8dd 0%, #e8c8ce 50%, #dbb5bc 100%);
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    gap: 16px;
}
.hero-image-placeholder .ph-icon { font-size: 48px; opacity: .4; }
.hero-image-placeholder p { font-size: 13px; color: #9a6872; letter-spacing: 1px; }

/* ── DIVIDER ── */
.divider {
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(201,84,106,0.2), transparent);
    margin: 0;
}

/* ── LETTER ── */
.letter-section {
    background: #fff;
    padding: 100px 6vw;
}
.letter-label {
    font-size: 11px; letter-spacing: 4px; text-transform: uppercase;
    color: #c97f8a; margin-bottom: 40px;
    display: flex; align-items: center; gap: 16px;
}
.letter-label::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(201,127,138,0.3), transparent);
}
.letter-card {
    max-width: 680px;
    margin: 0 auto;
    background: #fffcf9;
    border: 1px solid rgba(201,127,138,0.12);
    border-radius: 4px;
    padding: 64px 72px;
    position: relative;
    box-shadow: 0 8px 48px rgba(180,100,110,0.06);
}
.letter-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #e8b4b8, #c9546a, #e8b4b8);
}
.letter-date {
    font-size: 12px; color: #b8897e; letter-spacing: 1px;
    margin-bottom: 32px;
    font-family: 'DM Sans', sans-serif;
}
.letter-salutation {
    font-family: 'Cormorant Garamond', serif;
    font-size: 28px; font-weight: 400; font-style: italic;
    color: #2a1f1a;
    margin-bottom: 24px;
}
.letter-body {
    font-family: 'Cormorant Garamond', serif;
    font-size: 20px; font-weight: 300;
    line-height: 2;
    color: #4a3830;
}
.letter-body p { margin-bottom: 16px; }
.letter-sign {
    margin-top: 40px;
    font-family: 'Cormorant Garamond', serif;
    font-size: 22px; font-style: italic;
    color: #c9546a;
}
.letter-heart { display: inline-block; animation: pulse 1.8s ease-in-out infinite; }

/* ── TIMELINE ── */
.timeline-section {
    background: #fdf8f4;
    padding: 100px 6vw;
}
.section-header {
    margin-bottom: 64px;
}
.section-label {
    font-size: 11px; letter-spacing: 4px; text-transform: uppercase;
    color: #c97f8a; margin-bottom: 16px;
}
.section-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(36px, 5vw, 60px);
    font-weight: 300;
    color: #1e1210;
    line-height: 1.1;
}
.timeline-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 32px;
}
.timeline-card {
    background: #fff;
    border-radius: 3px;
    overflow: hidden;
    border: 1px solid rgba(201,127,138,0.1);
    transition: transform .4s cubic-bezier(.22,1,.36,1), box-shadow .4s;
    animation: fadeUp .8s cubic-bezier(.22,1,.36,1) both;
}
.timeline-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 60px rgba(180,100,110,0.12);
}
.card-image {
    width: 100%; height: 200px;
    background: linear-gradient(160deg, #f5e0e4 0%, #ead0d5 100%);
    display: flex; align-items: center; justify-content: center;
    font-size: 32px; color: rgba(180,100,110,0.3);
    position: relative; overflow: hidden;
}
.card-image .card-num {
    position: absolute; top: 16px; left: 16px;
    background: rgba(255,255,255,.9);
    border-radius: 50%;
    width: 32px; height: 32px;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 500; color: #c9546a;
}
.card-body { padding: 28px 28px 32px; }
.card-date { font-size: 11px; letter-spacing: 2px; color: #c97f8a; margin-bottom: 8px; }
.card-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 22px; font-weight: 400;
    color: #2a1f1a; margin-bottom: 10px;
}
.card-desc { font-size: 14px; color: #7a5a52; line-height: 1.6; font-weight: 300; }

/* ── VIDEO ── */
.video-section {
    background: #1e1210;
    padding: 100px 6vw;
}
.video-section .section-label { color: #c9546a; }
.video-section .section-title { color: #fff5f0; }
.video-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 24px;
    margin-top: 48px;
}
.video-placeholder {
    aspect-ratio: 16/9;
    background: #2e1f1a;
    border-radius: 3px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    gap: 12px;
    border: 1px solid rgba(201,84,106,0.15);
    cursor: pointer;
    transition: border-color .3s, background .3s;
    position: relative; overflow: hidden;
}
.video-placeholder::after {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(201,84,106,0.04), transparent);
}
.video-placeholder:hover { border-color: rgba(201,84,106,0.4); background: #3a2520; }
.play-btn {
    width: 56px; height: 56px;
    border: 1.5px solid rgba(201,84,106,0.5);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; color: #c9546a;
    transition: all .3s;
}
.video-placeholder:hover .play-btn {
    background: rgba(201,84,106,0.1);
    border-color: #c9546a;
    transform: scale(1.05);
}
.video-label { font-size: 13px; color: rgba(255,245,240,0.5); letter-spacing: 1px; }

/* ── MUSIC ── */
.music-section {
    background: #fff;
    padding: 100px 6vw;
    display: flex;
    align-items: center;
    gap: 80px;
    flex-wrap: wrap;
}
.music-text { flex: 1; min-width: 280px; }
.music-player { flex: 0 0 360px; min-width: 280px; }
.player-card {
    background: #fdf8f4;
    border: 1px solid rgba(201,127,138,0.15);
    border-radius: 4px;
    padding: 40px;
    text-align: center;
}
.player-thumb {
    width: 120px; height: 120px;
    border-radius: 50%;
    background: linear-gradient(135deg, #f0d8dd 0%, #e8c0c8 100%);
    margin: 0 auto 28px;
    display: flex; align-items: center; justify-content: center;
    font-size: 36px;
    animation: spin 8s linear infinite;
    animation-play-state: paused;
}
.player-thumb.playing { animation-play-state: running; }
.player-song { font-family: 'Cormorant Garamond', serif; font-size: 22px; color: #2a1f1a; margin-bottom: 4px; }
.player-artist { font-size: 13px; color: #9a7a72; margin-bottom: 28px; }
.player-controls {
    display: flex; align-items: center; justify-content: center; gap: 24px;
    margin-bottom: 24px;
}
.ctrl-btn {
    background: none; border: none; cursor: pointer;
    font-size: 18px; color: #9a7a72;
    transition: color .2s, transform .2s;
    padding: 8px;
}
.ctrl-btn:hover { color: #c9546a; transform: scale(1.1); }
.ctrl-play {
    width: 52px; height: 52px;
    background: #c9546a;
    border-radius: 50%; border: none;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; color: #fff; cursor: pointer;
    transition: background .2s, transform .2s;
    box-shadow: 0 6px 20px rgba(201,84,106,0.3);
}
.ctrl-play:hover { background: #b8495e; transform: scale(1.05); }
.progress-bar {
    width: 100%; height: 2px;
    background: rgba(201,127,138,0.2);
    border-radius: 1px;
    overflow: hidden;
}
.progress-fill {
    height: 100%; width: 35%;
    background: linear-gradient(90deg, #c9546a, #e8b4b8);
    border-radius: 1px;
    animation: progress 12s linear infinite;
}

/* ── FINAL SURPRISE ── */
.finale-section {
    background: linear-gradient(160deg, #1e1210 0%, #2e1a18 50%, #1e1210 100%);
    padding: 120px 6vw;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.finale-bg {
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 50% 50%, rgba(201,84,106,0.1) 0%, transparent 70%);
    pointer-events: none;
}
.finale-label { color: rgba(201,84,106,0.7); font-size: 11px; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 32px; }
.finale-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(40px, 6vw, 72px);
    font-weight: 300;
    color: #fff5f0;
    line-height: 1.2;
    margin-bottom: 48px;
}
.finale-btn {
    display: inline-block;
    padding: 18px 48px;
    background: transparent;
    border: 1px solid rgba(201,84,106,0.5);
    border-radius: 2px;
    color: #c9546a;
    font-size: 12px;
    letter-spacing: 3px;
    text-transform: uppercase;
    cursor: pointer;
    transition: all .3s;
    font-family: 'DM Sans', sans-serif;
}
.finale-btn:hover {
    background: rgba(201,84,106,0.1);
    border-color: #c9546a;
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(201,84,106,0.2);
}
.surprise-box {
    animation: fadeUp .8s cubic-bezier(.22,1,.36,1) both;
}
.surprise-photo-placeholder {
    width: 280px; height: 280px;
    border-radius: 50%;
    background: linear-gradient(135deg, #3a2520 0%, #2e1a18 100%);
    border: 1px solid rgba(201,84,106,0.2);
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    margin: 0 auto 48px;
    font-size: 40px;
    gap: 12px;
}
.surprise-photo-placeholder p { font-size: 12px; color: rgba(255,245,240,0.3); letter-spacing: 1px; }
.surprise-message {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(22px, 3vw, 34px);
    font-weight: 300;
    color: #fff5f0;
    line-height: 1.8;
    max-width: 560px;
    margin: 0 auto 16px;
}
.surprise-sign {
    font-family: 'Cormorant Garamond', serif;
    font-size: 20px; font-style: italic;
    color: #c9546a; margin-top: 24px;
}

/* ── QUOTE FOOTER ── */
.quote-footer {
    background: #fdf8f4;
    padding: 60px 6vw;
    text-align: center;
    border-top: 1px solid rgba(201,127,138,0.1);
}
.quote-text {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(16px, 2.5vw, 22px);
    font-weight: 300; font-style: italic;
    color: #9a7a72;
    max-width: 600px; margin: 0 auto;
    line-height: 1.8;
}

/* ── CONFETTI ── */
.confetti-container {
    position: fixed; inset: 0; pointer-events: none; z-index: 9999;
    overflow: hidden;
}
.confetti-piece {
    position: absolute;
    top: -10px;
    width: 8px; height: 8px;
    border-radius: 1px;
    animation: fall linear forwards;
}
@keyframes fall {
    to { transform: translateY(110vh) rotate(720deg); opacity: 0; }
}

/* ── ANIMATIONS ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.15); }
}
@keyframes spin {
    to { transform: rotate(360deg); }
}
@keyframes progress {
    from { width: 0%; }
    to   { width: 100%; }
}

/* ── RESPONSIVE ── */
@media (max-width: 768px) {
    .hero-image-side { display: none; }
    .hero-content { max-width: 100%; }
    .letter-card { padding: 40px 28px; }
    .music-section { flex-direction: column; gap: 40px; }
    .music-player { flex: 1; width: 100%; }
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "show_surprise" not in st.session_state:
    st.session_state.show_surprise = False
if "playing" not in st.session_state:
    st.session_state.playing = False
if "show_confetti" not in st.session_state:
    st.session_state.show_confetti = False

# ── 1. HERO ───────────────────────────────────────────────────────────────────
st.markdown("""
<section class="hero-wrap">
  <div class="hero-bg-circle c1"></div>
  <div class="hero-bg-circle c2"></div>
  <div class="hero-content">
    <p class="hero-eyebrow">Anneler Günü · 2025</p>
    <h1 class="hero-title">İyi ki<br>varsın<br><span>Anne</span> ❤️</h1>
    <p class="hero-sub">Bugün sana küçük ama özel bir sürpriz hazırladık.<br>
    Uraz ve Ahmet'ten, sana…</p>
    <a class="hero-cta" href="#letter">Keşfetmeye başla &darr;</a>
  </div>
  <div class="hero-image-side">
    <div class="hero-image-placeholder">
      <div class="ph-icon">📸</div>
      <p>AILE FOTOĞRAFI</p>
      <p style="font-size:11px;opacity:.6">app.py'de değiştirilebilir</p>
    </div>
  </div>
</section>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── 2. LETTER ─────────────────────────────────────────────────────────────────
st.markdown("""
<section id="letter" class="letter-section">
  <div class="letter-label">Uraz'dan Mektup</div>
  <div class="letter-card">
    <p class="letter-date">Mayıs 2025</p>
    <p class="letter-salutation">Merhaba anne,</p>
    <div class="letter-body">
      <p>Ben henüz konuşamıyorum ama sana her gün teşekkür etmek istiyorum.</p>
      <p>Beni sabırla uyuttuğun,<br>
         beni güldürdüğün,<br>
         ve bana sevginin ne olduğunu gösterdiğin için teşekkür ederim.</p>
      <p>Dünyaya gözlerimi ilk açtığımda ilk gördüğüm sendin.<br>
         Ve o andan beri sen benim her şeyimsin.</p>
      <p>Seni çok seviyorum.</p>
    </div>
    <div class="letter-sign">
      Uraz <span class="letter-heart">❤️</span>
    </div>
  </div>
</section>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── 3. TIMELINE ───────────────────────────────────────────────────────────────
memories = [
    ("01", "Ekim 2024", "Uraz Doğdu", "Küçük ellerin ilk kez senin parmağını tuttuğu an — dünyanın durduğu an."),
    ("02", "Kasım 2024", "İlk Aile Fotoğrafımız", "Üçümüz, bir çatı altında, yeni bir hikâyenin başında."),
    ("03", "Şubat 2025", "İlk Tatilimiz", "Deniz kokusu, bebek sesi ve senin gülüşün. Mükemmel bir tablo."),
    ("04", "Mart 2025", "İlk Kahkahamız", "Uraz ilk kez güldüğünde sen de güldün. O ses hâlâ kulaklarımızda."),
]

cards_html = ""
for delay, (num, date, title, desc) in enumerate(memories):
    cards_html += f"""
    <div class="timeline-card" style="animation-delay:{delay*0.15}s">
      <div class="card-image">
        📸
        <div class="card-num">{num}</div>
      </div>
      <div class="card-body">
        <p class="card-date">{date}</p>
        <h3 class="card-title">{title}</h3>
        <p class="card-desc">{desc}</p>
      </div>
    </div>"""

st.markdown(f"""
<section id="memories" class="timeline-section">
  <div class="section-header">
    <p class="section-label">Anılarımız</p>
    <h2 class="section-title">Birlikte yazdığımız<br>en güzel sayfalar</h2>
  </div>
  <div class="timeline-grid">
    {cards_html}
  </div>
</section>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── 4. VIDEO ──────────────────────────────────────────────────────────────────
videos = [
    "Uraz'ın İlk Sesi",
    "Birlikte Uyuyan Anımız",
    "Parkta Bir Sabah",
]
videos_html = "".join([
    f"""<div class="video-placeholder">
      <div class="play-btn">▶</div>
      <p class="video-label">{v}</p>
    </div>""" for v in videos
])

st.markdown(f"""
<section id="videos" class="video-section">
  <p class="section-label" style="color:#c9546a">Videolar</p>
  <h2 class="section-title" style="color:#fff5f0">Küçük mutluluğumuzun<br>en tatlı halleri</h2>
  <div class="video-grid">
    {videos_html}
  </div>
</section>
<div class="divider" style="background:linear-gradient(90deg,transparent,rgba(201,84,106,0.1),transparent)"></div>
""", unsafe_allow_html=True)

# ── 5. MUSIC ──────────────────────────────────────────────────────────────────
playing_class = "playing" if st.session_state.playing else ""
play_icon = "⏸" if st.session_state.playing else "▶"

st.markdown(f"""
<section id="music" class="music-section">
  <div class="music-text">
    <p class="section-label">Müziğimiz</p>
    <h2 class="section-title">Bizim<br>şarkımız</h2>
    <p style="margin-top:24px;font-size:15px;color:#7a5a52;line-height:1.8;font-weight:300;max-width:380px">
      Her ailenin kendine ait bir melodisi vardır.<br>
      Bu bizimki. Her çalanda içimiz ısınır.
    </p>
  </div>
  <div class="music-player">
    <div class="player-card">
      <div class="player-thumb {playing_class}">🎵</div>
      <p class="player-song">Bizim Şarkımız</p>
      <p class="player-artist">Eslem, Ahmet & Uraz</p>
      <div class="player-controls">
        <button class="ctrl-btn">⏮</button>
        <button class="ctrl-play">{play_icon}</button>
        <button class="ctrl-btn">⏭</button>
      </div>
      <div class="progress-bar">
        <div class="progress-fill {'playing' if st.session_state.playing else ''}" 
             style="animation-play-state:{'running' if st.session_state.playing else 'paused'}"></div>
      </div>
    </div>
  </div>
</section>
<div class="divider"></div>
""", unsafe_allow_html=True)

col_m1, col_m2, col_m3 = st.columns([3, 1, 3])
with col_m2:
    if st.button("▶ / ⏸", key="play_btn", help="Oynat/Duraklat", use_container_width=True):
        st.session_state.playing = not st.session_state.playing
        st.rerun()

# ── 6. FINALE ─────────────────────────────────────────────────────────────────
st.markdown("""
<section id="finale" class="finale-section">
  <div class="finale-bg"></div>
""", unsafe_allow_html=True)

if not st.session_state.show_surprise:
    st.markdown("""
    <p class="finale-label">Son Sürpriz</p>
    <h2 class="finale-title">Hazır mısın,<br>Eslem?</h2>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Son Mesaj ❤️", key="surprise_btn", use_container_width=True):
            st.session_state.show_surprise = True
            st.session_state.show_confetti = True
            st.rerun()
else:
    # Confetti
    if st.session_state.show_confetti:
        confetti_pieces = ""
        colors = ["#c9546a","#e8b4b8","#f5c8cc","#fff5f0","#b8495e","#f0d8dd"]
        import random
        for i in range(60):
            left = random.randint(0, 100)
            dur  = random.uniform(2.5, 5.0)
            delay= random.uniform(0, 2.0)
            color= colors[i % len(colors)]
            size = random.randint(6, 12)
            confetti_pieces += f"""<div class="confetti-piece" style="
                left:{left}%;
                width:{size}px;height:{size}px;
                background:{color};
                animation-duration:{dur:.1f}s;
                animation-delay:{delay:.1f}s;
                border-radius:{'50%' if i%3==0 else '1px'};
            "></div>"""

        st.markdown(f"""
        <div class="confetti-container">{confetti_pieces}</div>
        """, unsafe_allow_html=True)
        st.session_state.show_confetti = False

    st.markdown("""
    <div class="surprise-box">
      <div class="surprise-photo-placeholder">
        📸
        <p>AİLE FOTOĞRAFI</p>
      </div>
      <p class="finale-label">Eslem'e, Uraz & Ahmet'ten</p>
      <div class="surprise-message">
        Bazı insanlar anne olur.<br>
        <em>Sen bizim yuvamız oldun.</em><br><br>
        Her sabah uyanışımız, her gülüşümüz,<br>
        her küçük anımız — hepsi seninle anlam kazandı.
      </div>
      <div class="surprise-sign">Seni çok seviyoruz &nbsp;❤️<br>Uraz & Ahmet</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</section>", unsafe_allow_html=True)

# ── QUOTE FOOTER ──────────────────────────────────────────────────────────────
st.markdown("""
<footer class="quote-footer">
  <p class="quote-text">"Dünyanın tüm çiçeklerini toplasam, senin bir gülüşüne değişmem anne."</p>
</footer>
""", unsafe_allow_html=True)
