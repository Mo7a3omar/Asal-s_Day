import streamlit as st
import random
from pathlib import Path

# Page config
st.set_page_config(page_title="ستيكرات مريم", layout="centered")

# Initialize session state
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.all_stickers = []
    st.session_state.unused_stickers = []
    st.session_state.current_champion = None
    st.session_state.current_challenger = None
    st.session_state.comparisons_made = 0
    st.session_state.winner = None

def load_stickers():
    """Load all sticker images from a folder"""
    sticker_folder = Path("Mariam Stickers")  # Put your 36 sticker images here
    
    if not sticker_folder.exists():
        st.error(f"❌ Stickers folder not found! Please create a folder named 'stickers' in the same directory as this script.")
        return []
    
    stickers = list(sticker_folder.glob("*.png")) + \
               list(sticker_folder.glob("*.jpg")) + \
               list(sticker_folder.glob("*.jpeg")) + \
               list(sticker_folder.glob("*.gif"))
    
    if len(stickers) == 0:
        st.error(f"❌ No images found in the stickers folder! Please add your sticker images.")
        return []
    
    return [str(s) for s in stickers]

def start_game():
    """Initialize the game"""
    st.session_state.all_stickers = load_stickers()
    
    if len(st.session_state.all_stickers) < 2:
        st.error("❌ You need at least 2 stickers to play! Please add more images to the stickers folder.")
        return
    
    st.session_state.unused_stickers = st.session_state.all_stickers.copy()
    random.shuffle(st.session_state.unused_stickers)
    st.session_state.game_started = True
    st.session_state.comparisons_made = 0
    st.session_state.winner = None
    
    # Start with first two stickers
    st.session_state.current_champion = st.session_state.unused_stickers.pop(0)
    st.session_state.current_challenger = st.session_state.unused_stickers.pop(0)

def choose_sticker(chosen_is_champion):
    """Handle sticker selection - winner stays, loser is replaced"""
    st.session_state.comparisons_made += 1
    
    if chosen_is_champion:
        # Champion wins, keep it and get new challenger
        winner = st.session_state.current_champion
    else:
        # Challenger wins, it becomes new champion
        st.session_state.current_champion = st.session_state.current_challenger
        winner = st.session_state.current_champion
    
    # Check if there are more stickers
    if len(st.session_state.unused_stickers) > 0:
        st.session_state.current_challenger = st.session_state.unused_stickers.pop(0)
    else:
        # No more challengers - we have a winner!
        st.session_state.winner = winner
        st.session_state.current_challenger = None
    
    st.rerun()

# Main UI
st.title("🎮 ستيكرات مريم")
st.markdown("### لعبة التصفيات - اختار الستيكر المفضل!")

if not st.session_state.game_started:
    st.markdown("""
    **قواعد اللعبة:**
    - هيظهرلك ستيكرين في كل مرة
    - اختار الستيكر اللي بتحبه أكتر
    - الستيكر الفايز هيفضل موجود ويتنافس مع ستيكر جديد
    - الستيكر الخسران مش هيرجع تاني
    - وهكذا لحد ما نوصل للستيكر الفائز النهائي!
    
    عندنا 36 ستيكر جاهزين للمنافسة 🏆
    """)
    
    # Check if stickers exist before showing button
    sticker_folder = Path("stickers")
    if sticker_folder.exists():
        sticker_count = len(list(sticker_folder.glob("*.png"))) + \
                       len(list(sticker_folder.glob("*.jpg"))) + \
                       len(list(sticker_folder.glob("*.jpeg"))) + \
                       len(list(sticker_folder.glob("*.gif")))
        st.info(f"📁 Found {sticker_count} stickers ready to play!")
    else:
        st.warning("⚠️ Please create a 'stickers' folder and add your images!")
    
    if st.button("ابدأ اللعبة!", type="primary", use_container_width=True):
        start_game()
        if st.session_state.game_started:  # Only rerun if game actually started
            st.rerun()

else:
    # Show progress
    total_stickers = len(st.session_state.all_stickers)
    remaining_count = len(st.session_state.unused_stickers) + 2  # +2 for current pair
    
    if st.session_state.winner:
        remaining_count = 1
    
    st.markdown(f"**المقارنات:** {st.session_state.comparisons_made}")
    
    if total_stickers > 0:
        st.progress((total_stickers - remaining_count) / total_stickers)
    
    st.markdown(f"**متبقي:** {remaining_count} ستيكر")
    
    # Winner announcement
    if st.session_state.winner:
        st.balloons()
        st.success("🎉 عندنا فائز!")
        st.markdown(f"**الفائز بعد {st.session_state.comparisons_made} مقارنة!**")
        st.image(st.session_state.winner, caption="الستيكر الفائز! 🏆", use_container_width=True)
        
        if st.button("العب تاني!", type="primary", use_container_width=True):
            st.session_state.game_started = False
            st.rerun()
    
    # Show current pair
    elif st.session_state.current_champion and st.session_state.current_challenger:
        st.markdown("### اختار الستيكر المفضل:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(st.session_state.current_champion, use_container_width=True)
            if st.button("اختار ده", key="btn_champion", type="primary", use_container_width=True):
                choose_sticker(chosen_is_champion=True)
        
        with col2:
            st.image(st.session_state.current_challenger, use_container_width=True)
            if st.button("اختار ده", key="btn_challenger", type="primary", use_container_width=True):
                choose_sticker(chosen_is_champion=False)
    
    # Restart button
    st.markdown("---")
    if st.button("ابدأ من الأول", use_container_width=True):
        st.session_state.game_started = False
        st.rerun()
