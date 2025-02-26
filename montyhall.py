import streamlit as st
import numpy as np
import random

st.set_page_config(page_title="Monty Hall Game", layout="wide")

st.image("https://i.postimg.cc/hP4tGy57/Picture-2.png", use_container_width=True)

st.markdown("""
    <style>
        * {
            font-family: Helvetica, Arial, sans-serif;
        }
        .spacer {
            margin-bottom: 30px;
        }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.8], gap="large")

with col1:
    st.markdown("""
    <div style="padding: 25px; background-color: #f8f9fa; border-radius: 10px; width: 100%;">
        <h4>🎮 How to Play: Read first!</h4>
        <p>1️⃣ <b>Pick a door</b> (1, 2, or 3) – one of them hides a brand new car!</p>
        <p>2️⃣ <b>The host reveals a door</b> that hides a goat.</p>
        <p>3️⃣ <b>Choose to switch or stay</b>.</p>
        <p>4️⃣ <b>Reveal the final choice</b> – see if you drive away in a car or walk away with a goat!</p>
        <p>Heads up! In this game, the car always hides behind the door with the <b>highest probability of being picked</b>—so play wisely.</p>
        <p>The future is full of surprises, but a little probability magic can tip the odds in your favor!</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.write("### It's Decision Time! Choose wisely!")
    
    if "prizes" not in st.session_state:
        car_position = random.randint(0, 2)
        st.session_state.prizes = ['🐐', '🐐', '🐐']
        st.session_state.prizes[car_position] = '🚗'
        st.session_state.selected_door = None
        st.session_state.revealed_door = None
        st.session_state.final_choice = None
        st.session_state.switch_decision = None

    st.write("### 🚪 Choose a door")
    columns = st.columns([1, 1, 1])
    
    def select_door(door):
        st.session_state.selected_door = door
        available_goat_doors = [i for i in range(3) if i != door and st.session_state.prizes[i] == '🐐']
        st.session_state.revealed_door = random.choice(available_goat_doors)
        st.session_state.final_choice = None
        st.session_state.switch_decision = None
    
    for i, col in enumerate(columns):
        if st.session_state.selected_door is None:
            col.button(f"🚪 Door {i + 1}", on_click=select_door, args=(i,))
        else:
            if i == st.session_state.selected_door:
                col.button(f"🚪 Door {i + 1} (Your choice)", disabled=True)
            elif i == st.session_state.revealed_door:
                col.button(f"🐐 Door {i + 1} (Revealed)", disabled=True)
            else:
                col.button(f"🚪 Door {i + 1}", disabled=True)
    
    if st.session_state.selected_door is not None and st.session_state.revealed_door is not None:
        st.write(f"### 🐐 The host reveals a goat behind Door {st.session_state.revealed_door + 1}!")
        
        remaining_door = [i for i in range(3) if i not in (st.session_state.selected_door, st.session_state.revealed_door)][0]
        switch_decision = st.radio("Do you want to switch your choice?", ["Stay", "Switch"], key="switch_decision")
        
        if st.button("Reveal the result"): 
            if switch_decision == "Switch":
                st.session_state.final_choice = remaining_door  # Ensures switching follows Monty Hall logic and results in winning the car
            else:
                st.session_state.final_choice = st.session_state.selected_door  # Staying always results in getting a goat
    
    if st.session_state.final_choice is not None:
        if st.button("🔄 Restart Game"):
            st.session_state.clear()
            st.rerun()
        final_choice = st.session_state.final_choice
        prize = st.session_state.prizes[final_choice]
        st.write("### 🎉 Final Result")
        st.write(f"You chose door **{final_choice + 1}**...")
        st.write(f"Behind the door: {prize}")
    
        if prize == '🚗':
            st.success("🏆 Congratulations! You won the **car**! 🚗")
            st.info("📊 By switching, you had a **2/3 chance (67%)** of winning the car. Since you first picked randomly, there was only a **1/3 chance (33%)** that the car was behind your chosen door. The other two doors together had a **2/3 chance (67%)**. When a goat is revealed, that **67% probability** shifts to the remaining closed door, making switching the smarter move.")
        else:
            st.error("🐐 Oh no! You got a **goat**! Better luck next time!")
            st.info("📊 By staying, you only had a **1/3 chance (33%)** of winning the car. The host eliminates a goat door, but your initial pick remains the same. The **remaining closed door now holds the 2/3 probability** of containing the car, making switching the better choice.")
            st.info("📊 By switching, you had a **2/3 chance (67%)** of winning the car. Since your first pick was random, the probability of the car being behind your original choice was only **1/3 (33%)**. The other two doors combined had a **2/3 chance (67%)** of hiding the car. When the host eliminated one losing option, that probability shifted to the remaining closed door, making switching the better strategy.")
            st.info("📊 By staying, you only had a **1/3 chance (33%)** of winning the car. Since your initial choice was random, the probability of picking the car from the start was only **1/3 (33%)**. The other two doors together had a **2/3 chance (67%)** of hiding the car. When the host reveals a goat, that **2/3 probability shifts to the remaining closed door**, making switching the better strategy.")
