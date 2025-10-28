import streamlit as st
import random
from pathlib import Path
from openai import OpenAI
import json
from datetime import datetime
import os 
from dotenv import load_dotenv

# Page config
st.set_page_config(
    page_title="Suprise Mariam",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: linear-gradient(135deg, #FFF5F7 0%, #FFE6F0 50%, #F5E6FF 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFB6C1 0%, #E6B8F5 100%);
        padding: 20px 10px;
    }
    
    [data-testid="stSidebar"] button {
        background: rgba(255, 255, 255, 0.9) !important;
        color: #4A4A4A !important;
        border: 2px solid rgba(255, 182, 193, 0.5) !important;
        border-radius: 15px !important;
        font-weight: 600 !important;
        padding: 12px 20px !important;
        margin: 8px 0 !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stSidebar"] button:hover {
        background: white !important;
        border-color: #FFB6C1 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 182, 193, 0.4);
    }
    
    .audio-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9999;
        background: linear-gradient(135deg, #FFB6C1 0%, #FF9AA2 100%);
        padding: 15px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(255, 182, 193, 0.6);
    }
    
    .audio-container audio {
        width: 250px;
        height: 40px;
    }
    
    h1 {
        color: #FF69B4 !important;
        font-family: 'Georgia', serif;
        text-align: center;
        padding: 20px 0;
        text-shadow: 2px 2px 4px rgba(255, 182, 193, 0.3);
    }
    
    h2 {
        color: #E75480 !important;
        font-family: 'Georgia', serif;
        margin-top: 30px;
    }
    
    h3 {
        color: #DA70D6 !important;
        font-family: 'Georgia', serif;
    }
    
    h4 {
        color: #FF69B4 !important;
        font-family: 'Georgia', serif;
    }
    
    p {
        color: #4A4A4A !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #FFB6C1 0%, #FF9AA2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px 30px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 182, 193, 0.4) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(255, 182, 193, 0.6) !important;
    }
    
    .stTextInput input, .stTextArea textarea {
        border: 2px solid #FFB6C1 !important;
        border-radius: 15px !important;
        padding: 12px !important;
        background: white !important;
        color: #4A4A4A !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #FF69B4 !important;
        box-shadow: 0 0 10px rgba(255, 182, 193, 0.3) !important;
    }
    
    .stChatMessage {
        background: white !important;
        border-radius: 20px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
        box-shadow: 0 2px 10px rgba(255, 182, 193, 0.2) !important;
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, #FFB6C1 0%, #FF69B4 100%) !important;
    }
    
    .stAlert {
        background: rgba(255, 255, 255, 0.95) !important;
        border-left: 4px solid #FFB6C1 !important;
        border-radius: 10px !important;
        color: #4A4A4A !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #FF69B4 !important;
        font-weight: bold !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #4A4A4A !important;
    }
    
    .flashcard {
        background: linear-gradient(135deg, #FFB6C1 0%, #E6B8F5 100%);
        padding: 60px 40px;
        border-radius: 25px;
        box-shadow: 0 10px 30px rgba(255, 182, 193, 0.4);
        text-align: center;
        min-height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 30px 0;
    }
    
    .question-text {
        color: white !important;
        font-size: 32px;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        font-family: 'Georgia', serif;
    }
    
    .message-box {
        background: linear-gradient(135deg, #FFB6C1 0%, #E6B8F5 100%);
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 10px 30px rgba(255, 182, 193, 0.4);
        text-align: center;
        margin: 30px 0;
    }
    
    .message-box h1,
    .message-box h2, 
    .message-box h3,
    .message-box h4,
    .message-box p,
    .message-box strong {
        color: white !important;
        margin-bottom: 15px;
    }
    
    .envelope {
        width: 350px;
        height: 220px;
        margin: 50px auto;
        position: relative;
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    
    .envelope:hover {
        transform: scale(1.05);
    }
    
    .envelope-body {
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #FFB6C1 0%, #FF9AA2 100%);
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(255, 182, 193, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    .envelope-flap {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 50%;
        background: linear-gradient(135deg, #E6B8F5 0%, #DA70D6 100%);
        clip-path: polygon(0 0, 50% 80%, 100% 0);
        box-shadow: 0 4px 10px rgba(230, 184, 245, 0.4);
    }
    
    .envelope-seal {
        position: absolute;
        top: 35%;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 60px;
        background: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        z-index: 3;
    }
    
    .resolution-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);
        border-left: 4px solid #FFB6C1;
    }
    
    .person-card {
        background: white;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);
        text-align: center;
    }
    
    .person-card img {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    
    .event-card {
        background: white;
        padding: 20px;
        margin: 15px 0;
        border-radius: 15px;
        border-left: 4px solid #FFB6C1;
        box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    .event-card img {
        width: 150px;
        height: 150px;
        object-fit: cover;
        border-radius: 10px;
    }
    
    .stImage {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);
    }
    
    a {
        color: #FF69B4 !important;
        text-decoration: none !important;
        font-weight: 600 !important;
    }
    
    .stSuccess {
        background: rgba(255, 182, 193, 0.2) !important;
        color: #4A4A4A !important;
    }
</style>
""", unsafe_allow_html=True)

load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
FINE_TUNED_MODEL = os.getenv("FINE_TUNED_MODEL", "gpt-3.5-turbo")
TARGET_PERSON = "Mariam Asal"

if api_key:
    client = OpenAI(api_key=api_key)
else:
    client = None
    st.error("⚠️ OpenAI API key not found. Please add it to your .env file.")
# Session state initialization
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'envelope_opened' not in st.session_state:
    st.session_state.envelope_opened = False

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": f"You are {TARGET_PERSON}, responding naturally in Arabic."}
    ]

if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.all_stickers = []
    st.session_state.unused_stickers = []
    st.session_state.current_champion = None
    st.session_state.current_challenger = None
    st.session_state.comparisons_made = 0
    st.session_state.winner = None

if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

if 'show_flowers' not in st.session_state:
    st.session_state.show_flowers = False

if 'show_hug' not in st.session_state:
    st.session_state.show_hug = False

if 'resolutions' not in st.session_state:
    st.session_state.resolutions = []

# Background Music
MUSIC_FILE = "يا سيد يا بدوى.mp3"

if Path(MUSIC_FILE).exists():
    st.markdown('<div class="audio-container">', unsafe_allow_html=True)
    st.audio(MUSIC_FILE, format='audio/mp3', loop=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Friendship test questions
FRIENDSHIP_QUESTIONS = [
    "إيه اللون المفضل عند مريم؟",
    "إيه الأكلة اللي مريم بتحبها أوي؟",
    "إيه الفيلم أو المسلسل المفضل عند مريم؟",
    "مريم بتحب تعمل إيه في وقت فراغها؟",
    "إيه أكتر حاجة بتضحك مريم؟",
    "إيه الأغنية أو الفنان المفضل عند مريم؟",
    "مريم بتخاف من إيه؟",
    "إيه حلم مريم الكبير؟",
    "إيه أكتر صفة بتميز مريم؟",
    "مريم بتحب تسافر فين؟",
    "إيه المادة أو الموضوع اللي مريم بتحبه؟",
    "إيه أكتر حاجة بتزعل مريم؟",
    "مريم بتحب الحيوانات الأليفة؟ إيه نوع الحيوان المفضل؟",
    "إيه الهواية اللي مريم عايزة تتعلمها؟",
    "مريم من النوع اللي يصحى بدري ولا يسهر؟",
    "إيه أكتر حاجة مريم فخورة بيها في نفسها؟",
    "إيه المكان المفضل عند مريم في طنطا؟",
    "مريم بتحب القهوة ولا الشاي أكتر؟",
    "إيه أكتر موقف محرج حصل لمريم؟",
    "لو مريم كسبت مليون جنيه هتعمل بيهم إيه؟",
]

# Famous people
FAMOUS_PEOPLE = [
    {"name": "Winona Ryder", "description": "ممثلة أمريكية مشهورة", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Winona_Ryder_2010.jpg/440px-Winona_Ryder_2010.jpg"},
    {"name": "Richard Dreyfuss", "description": "ممثل حائز على الأوسكار", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Richard_Dreyfuss_at_the_2010_Independent_Spirit_Awards.jpg/440px-Richard_Dreyfuss_at_the_2010_Independent_Spirit_Awards.jpg"},
    {"name": "Gabrielle Union", "description": "ممثلة وناشطة", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Gabrielle_Union_2019_2.png/440px-Gabrielle_Union_2019_2.png"},
    {"name": "Bob Ross", "description": "رسام ومقدم برامج فنية", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Bob_Ross.jpg/440px-Bob_Ross.jpg"},
    {"name": "Tracee Ellis Ross", "description": "ممثلة ومغنية", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Tracee_Ellis_Ross_%2842611289%29_%28cropped%29.jpg/440px-Tracee_Ellis_Ross_%2842611289%29_%28cropped%29.jpg"},
    {"name": "Dan Castellaneta", "description": "صوت هومر سيمبسون", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Dan_Castellaneta_2019.jpg/440px-Dan_Castellaneta_2019.jpg"}
]

# Historical events
HISTORICAL_EVENTS = [
    {"year": "1929", "event": "Black Tuesday - انهيار بورصة وول ستريت وبداية الكساد الكبير", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Crowd_outside_nyse.jpg/560px-Crowd_outside_nyse.jpg"},
    {"year": "1923", "event": "تركيا أصبحت جمهورية بعد سقوط الدولة العثمانية", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Atat%C3%BCrk_C%C3%BCmhuriyet%27i_ilan_ediyor.jpg/560px-Atat%C3%BCrk_C%C3%BCmhuriyet%27i_ilan_ediyor.jpg"},
    {"year": "1863", "event": "تأسيس الصليب الأحمر الدولي في جنيف", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Red_Cross_or_Crescent.svg/440px-Red_Cross_or_Crescent.svg.png"},
    {"year": "1998", "event": "John Glenn أصبح أكبر شخص يطير للفضاء في سن 77 سنة", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/John_Glenn_NASA.jpg/440px-John_Glenn_NASA.jpg"},
    {"year": "2012", "event": "إعصار ساندي يضرب الساحل الشرقي لأمريكا", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Hurricane_Sandy_Oct_28_2012_1600Z.jpg/560px-Hurricane_Sandy_Oct_28_2012_1600Z.jpg"}
]

# Helper functions
def load_stickers():
    sticker_folder = Path("Mariam Stickers")
    if not sticker_folder.exists():
        return []
    stickers = list(sticker_folder.glob("*.png")) + list(sticker_folder.glob("*.jpg")) + list(sticker_folder.glob("*.jpeg")) + list(sticker_folder.glob("*.gif"))
    return [str(s) for s in stickers]

def start_game():
    st.session_state.all_stickers = load_stickers()
    if len(st.session_state.all_stickers) < 2:
        st.error("You need at least 2 stickers to play!")
        return
    st.session_state.unused_stickers = st.session_state.all_stickers.copy()
    random.shuffle(st.session_state.unused_stickers)
    st.session_state.game_started = True
    st.session_state.comparisons_made = 0
    st.session_state.winner = None
    st.session_state.current_champion = st.session_state.unused_stickers.pop(0)
    st.session_state.current_challenger = st.session_state.unused_stickers.pop(0)

def choose_sticker(chosen_is_champion):
    st.session_state.comparisons_made += 1
    if chosen_is_champion:
        winner = st.session_state.current_champion
    else:
        st.session_state.current_champion = st.session_state.current_challenger
        winner = st.session_state.current_champion
    if len(st.session_state.unused_stickers) > 0:
        st.session_state.current_challenger = st.session_state.unused_stickers.pop(0)
    else:
        st.session_state.winner = winner
        st.session_state.current_challenger = None
    st.rerun()

def save_resolutions():
    with open("mariam_resolutions.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.resolutions, f, ensure_ascii=False, indent=2)

def load_resolutions():
    try:
        with open("mariam_resolutions.json", "r", encoding="utf-8") as f:
            st.session_state.resolutions = json.load(f)
    except FileNotFoundError:
        st.session_state.resolutions = []

# Sidebar Navigation
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>Mariam's Birthday</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid white; margin: 20px 0;'>", unsafe_allow_html=True)
    
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()
    
    if st.button("🎉 ليه النهاردة يوم مميز", use_container_width=True):
        st.session_state.page = 'october29'
        st.rerun()
    
    if st.button("💬 اتكلمي مع نفسك", use_container_width=True):
        st.session_state.page = 'chat'
        st.rerun()
    
    if st.button("🎮 لعبة الستيكرات", use_container_width=True):
        st.session_state.page = 'game'
        st.rerun()
    
    if st.button("✨ مريم الجديدة", use_container_width=True):
        st.session_state.page = 'resolutions'
        st.rerun()
    
    if st.button("🤝 اختبري صحابك", use_container_width=True):
        st.session_state.page = 'friendship_test'
        st.rerun()
    
    if st.button("💝 Important Message", use_container_width=True):
        st.session_state.page = 'important'
        st.session_state.envelope_opened = False  # Reset envelope when navigating
        st.rerun()
    
    st.markdown("<hr style='border: 1px solid white; margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white; font-size: 14px;'>Made with ❤️</p>", unsafe_allow_html=True)

# HOME PAGE
if st.session_state.page == 'home':
    st.markdown("<h1>Happy Birthday Mariam!</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; padding: 30px; background: white; border-radius: 20px; margin: 20px 0; box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);'>
        <h2 style='color: #FF69B4;'>Welcome to Your Special Day!</h2>
        <p style='font-size: 18px; color: #4A4A4A; line-height: 1.8;'>
            This website was created with love just for you. Explore different sections to discover
            surprises, play games, and relive memories!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: white; padding: 25px; border-radius: 20px; margin: 10px 0; box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);'>
            <h3 style='color: #FF69B4;'>🎉 ليه النهاردة يوم مميز</h3>
            <p style='color: #4A4A4A;'>اكتشفي حقائق مذهلة عن يوم ميلادك</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("استكشفي", key="btn_oct29", use_container_width=True):
            st.session_state.page = 'october29'
            st.rerun()
        
        st.markdown("""
        <div style='background: white; padding: 25px; border-radius: 20px; margin: 10px 0; box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);'>
            <h3 style='color: #FF69B4;'>💬 اتكلمي مع نفسك</h3>
            <p style='color: #4A4A4A;'>تكلمي مع ذكاء اصطناعي متدرب على محادثاتك</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("ابدأي الدردشة", key="btn_chat", use_container_width=True):
            st.session_state.page = 'chat'
            st.rerun()
        
        st.markdown("""
        <div style='background: white; padding: 25px; border-radius: 20px; margin: 10px 0; box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);'>
            <h3 style='color: #FF69B4;'>🎮 لعبة الستيكرات</h3>
            <p style='color: #4A4A4A;'>لعبة التصفيات - اختاري الستيكر المفضل</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("العبي دلوقتي", key="btn_game", use_container_width=True):
            st.session_state.page = 'game'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style='background: white; padding: 25px; border-radius: 20px; margin: 10px 0; box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);'>
            <h3 style='color: #FF69B4;'>✨ مريم الجديدة</h3>
            <p style='color: #4A4A4A;'>اكتبي أحلامك وأهدافك للسنة الجديدة</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("اكتبي أحلامك", key="btn_resolutions", use_container_width=True):
            st.session_state.page = 'resolutions'
            st.rerun()
        
        st.markdown("""
        <div style='background: white; padding: 25px; border-radius: 20px; margin: 10px 0; box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);'>
            <h3 style='color: #FF69B4;'>🤝 اختبري صحابك</h3>
            <p style='color: #4A4A4A;'>شوفي مين فعلاً بيعرفك كويس</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("ابدأي الاختبار", key="btn_test", use_container_width=True):
            st.session_state.page = 'friendship_test'
            st.rerun()
        
        st.markdown("""
        <div style='background: white; padding: 25px; border-radius: 20px; margin: 10px 0; box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);'>
            <h3 style='color: #FF69B4;'>💝 Important Message</h3>
            <p style='color: #4A4A4A;'>A heartfelt message with virtual flowers and hugs</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Read Message", key="btn_important", use_container_width=True):
            st.session_state.page = 'important'
            st.session_state.envelope_opened = False
            st.rerun()

# OCTOBER 29TH PAGE
elif st.session_state.page == 'october29':
    st.markdown("<h1>29 أكتوبر - يوم مميز جداً!</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: white; padding: 30px; border-radius: 20px; margin: 20px 0; box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);'>
        <h2 style='color: #FF69B4;'>📊 حياتك في أرقام</h2>
        <p style='color: #4A4A4A; font-size: 16px;'>عايز تعرف حياتك اتحولت لكام ثانية؟ كام نبضة قلب؟</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.link_button("🔗 دوسي هنا بسرعة", "https://neal.fun/life-stats/", use_container_width=True)
    
    st.markdown("<hr style='border: 2px solid #FFB6C1; margin: 30px 0;'>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: white; padding: 30px; border-radius: 20px; box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);'>
        <h2 style='color: #FF69B4;'>🌟 مشاهير اتولدوا في 29 أكتوبر</h2>
        <p style='color: #4A4A4A;'>ناس كتير مشهورة اتولدت في اليوم ده</p>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(3)
    for idx, person in enumerate(FAMOUS_PEOPLE):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class='person-card'>
                <img src='{person["image"]}' alt='{person["name"]}'>
                <h4 style='color: #FF69B4; margin: 10px 0;'>{person["name"]}</h4>
                <p style='color: #4A4A4A; font-size: 14px;'>{person["description"]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 2px solid #FFB6C1; margin: 30px 0;'>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: white; padding: 30px; border-radius: 20px; box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);'>
        <h2 style='color: #FF69B4;'>📜 أحداث تاريخية مهمة</h2>
    </div>
    """, unsafe_allow_html=True)
    
    for event in HISTORICAL_EVENTS:
        st.markdown(f"""
        <div class='event-card'>
            <img src='{event["image"]}' alt='{event["year"]}'>
            <div>
                <h3 style='color: #FF69B4; margin: 0;'>{event["year"]}</h3>
                <p style='color: #4A4A4A; font-size: 16px; margin: 10px 0 0 0;'>{event["event"]}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 2px solid #FFB6C1; margin: 30px 0;'>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: #E75480;'>لكن في حدث مهم جداً كل الناس نسيته!</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #DA70D6;'> , حدث تاريخي من أهم الأحداث في التاريخ المصري والعالمي...</h3>", unsafe_allow_html=True)
    
    if st.button("يا ترى ايه هو", use_container_width=True):
        st.balloons()
        st.markdown("""
        <div class='message-box'>
            <h1>ميلاد أهم شخصية في طنطا!</h1>
            <h3>بعد السيد البدوي  </h3>
            <br>
            <h2>في يوم 29 أكتوبر اتولدت...</h2>
            <h1 style='font-size: 48px;'> مريم عمرو عادل عسل مشعارف باقي الاسم للامانة</h1>
            <br>
        </div>
        """, unsafe_allow_html=True)
        st.image("https://media.giphy.com/media/g5R9dok94mrIvplmZd/giphy.gif", use_container_width=True)

# CHAT PAGE
elif st.session_state.page == 'chat':
    st.markdown("<h1>اتكلمي مع نفسك</h1>", unsafe_allow_html=True)
    
    if not client:
        st.error("Chat feature is currently unavailable. API key not configured.")
        if st.button("🏠 العودة للصفحة الرئيسية", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
    else:
        for message in st.session_state.chat_history[1:]:
            if message["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.write(message["content"])
        
        user_input = st.chat_input("ربنا يكون في عونك")
        
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user", avatar="👤"):
                st.write(user_input)
            
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("مريم بترد استخبى بسرعة "):
                    try:
                        response = client.chat.completions.create(
                            model=FINE_TUNED_MODEL,
                            messages=st.session_state.chat_history,
                            temperature=0.8,
                            max_tokens=150
                        )
                        assistant_reply = response.choices[0].message.content
                        st.write(assistant_reply)
                        st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        if len(st.session_state.chat_history) > 1:
            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = [
                    {"role": "system", "content": f"You are {TARGET_PERSON}, responding naturally in Arabic."}
                ]
                st.rerun()

# STICKERS GAME PAGE
elif st.session_state.page == 'game':
    st.markdown("<h1>لعبة الستيكرات</h1>", unsafe_allow_html=True)
    
    if not st.session_state.game_started:
        st.markdown("""
        <div style='background: white; padding: 30px; border-radius: 20px; box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);'>
            <h3 style='color: #FF69B4;'> هنعرف ايه ستيكر مريم المفضل اخيرا:</h3>
        </div>
        """, unsafe_allow_html=True)
        
        sticker_count = len(load_stickers())
        if sticker_count > 0:
            st.info(f"Found {sticker_count} stickers ready to play!")
        
        if st.button("ابدأ اللعبة!", use_container_width=True):
            start_game()
            if st.session_state.game_started:
                st.rerun()
    
    else:
        total_stickers = len(st.session_state.all_stickers)
        remaining_count = len(st.session_state.unused_stickers) + 2
        
        if st.session_state.winner:
            remaining_count = 1
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("المقارنات", st.session_state.comparisons_made)
        with col2:
            st.metric("متبقي", remaining_count)
        with col3:
            if total_stickers > 0:
                progress_pct = int(((total_stickers - remaining_count) / total_stickers) * 100)
                st.metric("التقدم", f"{progress_pct}%")
        
        if total_stickers > 0:
            st.progress((total_stickers - remaining_count) / total_stickers)
        
        if st.session_state.winner:
            st.balloons()
            st.success("عندنا فائز!")
            st.markdown(f"<p style='color: #4A4A4A; font-size: 18px; text-align: center;'><strong>الفائز بعد {st.session_state.comparisons_made} مقارنة</strong></p>", unsafe_allow_html=True)
            st.image(st.session_state.winner, caption="الستيكر الي كسب! 🏆", use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("العب تاني!", use_container_width=True):
                    st.session_state.game_started = False
                    st.rerun()
            with col2:
                if st.button("رجوع للبداية", use_container_width=True):
                    st.session_state.page = 'home'
                    st.session_state.game_started = False
                    st.rerun()
        
        elif st.session_state.current_champion and st.session_state.current_challenger:
            st.markdown("<h3 style='color: #DA70D6;'>اختار الستيكر المفضل:</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(st.session_state.current_champion, use_container_width=True)
                if st.button("اختار ده", key="btn_champion", use_container_width=True):
                    choose_sticker(chosen_is_champion=True)
            
            with col2:
                st.image(st.session_state.current_challenger, use_container_width=True)
                if st.button("اختار ده", key="btn_challenger", use_container_width=True):
                    choose_sticker(chosen_is_champion=False)

# NEW YEAR RESOLUTIONS PAGE
elif st.session_state.page == 'resolutions':
    st.markdown("<h1>- أحلامي وأهدافي</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: white; padding: 30px; border-radius: 20px; margin: 20px 0; box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3); text-align: center;'>
        <h2 style='color: #FF69B4;'>✨ رحلتي نحو النجاح</h2>
        <p style='color: #4A4A4A; font-size: 18px;'>
اكتبي هنا كل حاجه نفسك فيها لو مكسلة فاكس انا قولت اعمل صفحة سادسة 
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    load_resolutions()
    
    st.markdown("<h2 style='color: #E75480;'>إضافة هدف جديد</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        resolution_title = st.text_input(
            "عنوان الهدف",
            placeholder="مثال: تعلم لغة جديدة، الحصول على ترقية، السفر لبلد جديد...",
            key="new_resolution_title"
        )
    
    with col2:
        resolution_category = st.selectbox(
            "الفئة",
            ["🎓 تعليم", "💼 عمل", "💪 صحة", "🌍 سفر", "🎨 هوايات", "💝 علاقات", "💰 مالي", "🌟 شخصي"],
            key="resolution_category"
        )
    
    resolution_details = st.text_area(
        "تفاصيل الهدف وخطة التنفيذ",
        placeholder=" كل دا شات جي بي اتي ",
        height=150,
        key="resolution_details"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("✨ إضافة الهدف", use_container_width=True):
            if resolution_title and resolution_details:
                new_resolution = {
                    "id": len(st.session_state.resolutions) + 1,
                    "title": resolution_title,
                    "category": resolution_category,
                    "details": resolution_details,
                    "date_added": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "completed": False
                }
                st.session_state.resolutions.append(new_resolution)
                save_resolutions()
                st.success("تم إضافة الهدف بنجاح! 🎉")
                st.balloons()
                st.rerun()
            else:
                st.error("من فضلك املي كل الحقول!")
    
    st.markdown("<hr style='border: 2px solid #FFB6C1; margin: 40px 0;'>", unsafe_allow_html=True)
    
    if st.session_state.resolutions:
        st.markdown(f"<h2 style='color: #E75480;'>أهدافي ({len(st.session_state.resolutions)})</h2>", unsafe_allow_html=True)
        
        filter_option = st.selectbox(
            "تصفية حسب",
            ["كل الأهداف", "الأهداف المكتملة", "الأهداف الجارية"],
            key="filter_resolutions"
        )
        
        for idx, resolution in enumerate(st.session_state.resolutions):
            if filter_option == "الأهداف المكتملة" and not resolution["completed"]:
                continue
            if filter_option == "الأهداف الجارية" and resolution["completed"]:
                continue
            
            completed_style = "opacity: 0.6;" if resolution["completed"] else ""
            checkmark = "✅ " if resolution["completed"] else ""
            
            st.markdown(f"""
            <div class='resolution-card' style='{completed_style}'>
                <h3 style='color: #FF69B4; margin-bottom: 10px;'>{resolution['category']} {checkmark}{resolution['title']}</h3>
                <p style='color: #4A4A4A; margin: 10px 0; line-height: 1.6;'>{resolution['details']}</p>
                <p style='color: #DA70D6; font-size: 14px; margin-top: 15px;'>تم الإضافة: {resolution['date_added']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if not resolution["completed"]:
                    if st.button(f"✅ تم الإنجاز", key=f"complete_{idx}"):
                        st.session_state.resolutions[idx]["completed"] = True
                        save_resolutions()
                        st.success("مبروك! 🎉")
                        st.rerun()
                else:
                    if st.button(f"↩️ إلغاء الإنجاز", key=f"uncomplete_{idx}"):
                        st.session_state.resolutions[idx]["completed"] = False
                        save_resolutions()
                        st.rerun()
            
            with col2:
                if st.button(f"🗑️ حذف", key=f"delete_{idx}"):
                    st.session_state.resolutions.pop(idx)
                    save_resolutions()
                    st.rerun()
    
    else:
        st.markdown("""
        <div style='text-align: center; padding: 60px; background: white; border-radius: 20px; box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);'>
            <h3 style='color: #FF69B4;'>لسه مفيش أهداف! ✨</h3>
            <p style='color: #4A4A4A;'>ابدأي بإضافة أول هدف ليكي في السنة الجديدة</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 2px solid #FFB6C1; margin: 40px 0;'>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='message-box'>
        <h3>💫 تذكري دائماً</h3>
        <p style='font-size: 20px;'>"قد الدنيا يا مريوم و ان شاء الله السنة الجاية اعملك واحد تاني بس و انتي برا مصر بقا</p>
        <p style='font-size: 18px;'>كل سنة وانتي بخير وإنجازات! </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🏠 العودة للصفحة الرئيسية", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()

# FRIENDSHIP TEST PAGE
elif st.session_state.page == 'friendship_test':
    st.markdown("<h1>اختبري صحابك</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: white; padding: 20px; border-radius: 15px; margin: 20px 0; box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);'>
        <p style='color: #4A4A4A; font-size: 16px; text-align: center;'>
            <strong>ملحوظة:</strong> مفيش إجابات صح أو غلط - مريم هي اللي هتحكم على الإجابات
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    total_questions = len(FRIENDSHIP_QUESTIONS)
    st.progress((st.session_state.current_question) / total_questions)
    st.markdown(f"<p style='text-align: center; color: #FF69B4; font-size: 18px; font-weight: bold;'>السؤال {st.session_state.current_question + 1} من {total_questions}</p>", unsafe_allow_html=True)
    
    current_q = FRIENDSHIP_QUESTIONS[st.session_state.current_question]
    
    st.markdown(f"""
    <div class='flashcard'>
        <div class='question-text'>{current_q}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: #DA70D6;'>إجابة صاحبك:</h3>", unsafe_allow_html=True)
    user_answer = st.text_area(
        "اكتب الإجابة هنا...",
        height=120,
        key=f"answer_{st.session_state.current_question}",
        placeholder="اكتب إجابتك واعرض على مريم تشوفها...",
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.session_state.current_question > 0:
            if st.button("⬅️ السؤال اللي فات", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
    
    with col2:
        if st.button("🔄 ابدأ من الأول", use_container_width=True):
            st.session_state.current_question = 0
            st.rerun()
    
    with col3:
        if st.session_state.current_question < total_questions - 1:
            if st.button("السؤال الجاي ➡️", use_container_width=True):
                st.session_state.current_question += 1
                st.rerun()
        else:
            if st.button("✅ خلصت!", use_container_width=True):
                st.balloons()
                st.success("تمام! دلوقتي ورّي الإجابات لمريم واعرف النتيجة")

# IMPORTANT PAGE - WITH ENVELOPE
elif st.session_state.page == 'important':
    st.markdown("<h1>Important Message</h1>", unsafe_allow_html=True)
    
    if not st.session_state.envelope_opened:
        # Show closed envelope
        st.markdown("""
        <div style='text-align: center; padding: 40px; background: white; border-radius: 20px; margin: 30px 0; box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);'>
            <h2 style='color: #FF69B4;'>لديك رسالة خاصة 💌</h2>
            <p style='color: #4A4A4A; font-size: 18px;'>اضغطي على الظرف لفتحه وقراءة الرسالة</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Envelope design
        st.markdown("""
        <div class='envelope'>
            <div class='envelope-body'>
                <div class='envelope-flap'></div>
                <div class='envelope-seal'>💝</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📬 افتحي الظرف", use_container_width=True):
                st.session_state.envelope_opened = True
                st.balloons()
                st.rerun()
    
    else:
        # Show the opened letter content
        st.markdown("""
        <div style='background: white; padding: 40px; border-radius: 20px; margin: 30px 0; box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3); text-align: center;'>
            <h2 style='color: #FF69B4;'>عندي هدايا ليكي!</h2>
            <p style='color: #4A4A4A; font-size: 18px;'>اختاري الهدية اللي عايزة تفتحيها</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #FFB6C1 0%, #FF9AA2 100%); 
                        padding: 30px; 
                        border-radius: 20px; 
                        text-align: center; 
                        box-shadow: 0 4px 15px rgba(255, 182, 193, 0.4);
                        margin: 10px;'>
                <h2 style='color: white; font-size: 60px; margin: 20px 0;'>🎁</h2>
                <h3 style='color: white;'>الهدية الأولى</h3>
                <p style='color: white;'>ورد افتراضي</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("افتح الهدية الأولى", key="gift1", use_container_width=True):
                st.session_state.show_flowers = True
                st.rerun()
        
        with col2:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #E6B8F5 0%, #DA70D6 100%); 
                        padding: 30px; 
                        border-radius: 20px; 
                        text-align: center; 
                        box-shadow: 0 4px 15px rgba(230, 184, 245, 0.4);
                        margin: 10px;'>
                <h2 style='color: white; font-size: 60px; margin: 20px 0;'>🎁</h2>
                <h3 style='color: white;'>الهدية التانية</h3>
                <p style='color: white;'>حضن افتراضي</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("افتح الهدية التانية", key="gift2", use_container_width=True):
                st.session_state.show_hug = True
                st.rerun()
        
        if st.session_state.show_flowers:
            st.markdown("<hr style='border: 2px solid #FFB6C1; margin: 40px 0;'>", unsafe_allow_html=True)
            
            st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <h2 style='color: #FF69B4;'> لأن مقدرش أديكي ورد حقيقي ف اتمنى تقبلي شوية الورد دول...</h2>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4, col5 = st.columns(5)
            flowers = ["🌹", "🌺", "🌻", "🌷", "🌸"]
            for i, col in enumerate([col1, col2, col3, col4, col5]):
                with col:
                    st.markdown(f"<h1 style='text-align: center; font-size: 48px;'>{flowers[i]}</h1>", unsafe_allow_html=True)
                    st.markdown(f"<h1 style='text-align: center; font-size: 48px;'>{flowers[(i+1)%5]}</h1>", unsafe_allow_html=True)
                    st.markdown(f"<h1 style='text-align: center; font-size: 48px;'>{flowers[(i+2)%5]}</h1>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div style='padding: 10px; background: white; border-radius: 15px; box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);'>
                    <img src='https://media.giphy.com/media/l0HU8V1CHKTUFtuFO/giphy.gif' style='width: 100%; border-radius: 10px;'>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style='padding: 10px; background: white; border-radius: 15px; box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);'>
                    <img src='https://media.giphy.com/media/cXFVCJt3vhUaY/giphy.gif' style='width: 100%; border-radius: 10px;'>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div style='padding: 10px; background: white; border-radius: 15px; box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);'>
                    <img src='https://media.giphy.com/media/3oKIPm9E94gszBPVdu/giphy.gif' style='width: 100%; border-radius: 10px;'>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style='text-align: center; font-size: 40px; margin: 30px 0;'>
                🌹 💐 🌺 🌻 🌷 🌸 🏵️ 🌼 🌹 💐 🌺 🌻 🌷 🌸 🏵️ 🌼
            </div>
            """, unsafe_allow_html=True)
        
        if st.session_state.show_hug:
            st.markdown("<hr style='border: 2px solid #E6B8F5; margin: 40px 0;'>", unsafe_allow_html=True)
            
            st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <h2 style='color: #DA70D6;'>   و عشان الحضن حرام للاسف ف خدي حضن الميجاباينس دا </h2>
                <h3 style='color: #BA55D3;'>كرينج اوي بصراحة </h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style='padding: 20px; background: white; border-radius: 20px; box-shadow: 0 4px 15px rgba(230, 184, 245, 0.4); margin: 20px auto; max-width: 600px;'>
                <img src='https://media.giphy.com/media/XpgOZHuDfIkoM/giphy.gif' style='width: 100%; border-radius: 15px;'>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="text-align: center; font-size: 60px; margin: 30px 0;">
                🤗 🫂 💝 🤗 🫂 💝
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<hr style='border: 2px solid #FFB6C1; margin: 40px 0;'>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='message-box'>
            <h2>💌 رسالة خاصة</h2>
            <h3>عزيزتي مريم</h3>
            <p>بعد كل العبط دا بقا احب اقولك شوية حاجات كدا</p>
            <p><strong>كنت اتمنى اننا نكون نعرف نتقابل و اكون معاكي بدل التواصل الممل دا</strong></p>
            <br>
            <p>في العادي لا بعرف احتفل بحد ولا أقول كلام حلو و مش شاطر في الهدايا للأسف بس قولت اعمل حاجه الي بعرف اعملها. كان نفسي اعمل حاجات اكتر من كدا كمان و نتقابل بس مشكلة لسه المستقبل طويل.</p>
            <br>
            <p>احب اعرفك انك من الأشخاص الجميلة الي الواحد عرفها في المكان الي ميتسماش دا (بالنسبالك) و نوعا ما دخلتي دايرة عندي مش أي بني ادم يعرف يخشها م بالك لو بنت بقا مش ممكن يعني، لو كنتي ولد بس كان زمانك اقرب و اقرب بس سليمة هنعمل ايه بقا.</p>
            <br>
            <p>أتمنى تستمتعي بهذا اليوم لانه يومك انتي يا اتنشن مشفاهم انا ايه الاتنشن دا. و أتمنى يكون الكلام الي عملته دا عجبك عارف انه مش احسن حاجه خالص للأسف بس قولت لازم اعمل حاجه طبعا.</p>
            <br>
            <p>اتمنى تكون السنة القادمة تكوني مبسوطة فيها و ترحمي نفسك شوية و تعيشي الدنيا من غير جلد و تقعدي مع الناس الي بيحبوكي و بتحبيهم و متخافيش من حاجه. بقا عندك 23 سنة مش ممكن عجوزة اوي يعني.</p>
            <br>
            <p>انتي شخص كويس يا مريم و مليانة صفات جميلة مش أي حد عنده. لو قعدت ارص الصفات الحلوة مش هخلص بس انتي عارفة بقا كل الكلام دا.</p>
            <br>
            <p>و اتمنالك في الاخر يوم ميلاد سعيد أتمنى تتبسطي فيه و تخرجي و تتفسحي (لو عرفتي ترني عليا في أي وقت ياريت اعيد عليكي) و أتمنى ليكي السعادة الأبدية يارب و كل سنة و انتي طيبة يا باشا.</p>
            <br>
            <p><em>نوت: كنت كاتبها بالانجلش بس عارفك فلاحة ف قولت عربي احسن </em></p>
            <br>

        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='text-align: center; margin: 40px 0;'><h2 style='color: #FF69B4;'>Happy Birthday Mariam!</h2><p style='font-size: 20px; color: #E75480;'>May all your dreams come true!</p></div>", unsafe_allow_html=True)
        
        if st.session_state.show_flowers or st.session_state.show_hug:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 إعادة فتح الهدايا", use_container_width=True):
                    st.session_state.show_flowers = False
                    st.session_state.show_hug = False
                    st.rerun()
            with col2:
                if st.button("🏠 العودة للصفحة الرئيسية", use_container_width=True):
                    st.session_state.page = 'home'
                    st.session_state.show_flowers = False
                    st.session_state.show_hug = False
                    st.session_state.envelope_opened = False
                    st.rerun()
        else:
            if st.button("🏠 العودة للصفحة الرئيسية", use_container_width=True):
                st.session_state.page = 'home'
                st.session_state.envelope_opened = False
                st.rerun()
