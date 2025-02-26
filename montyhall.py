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
        <p>1️⃣ <b>Pick a door</b>(1, 2, or 3) – one of them hides a brand new car!</p>
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
        st.session_state.result = None
        st.session_state.switch_decision = None

    st.write("### 🚪 Choose a door")
    columns = st.columns([1, 1, 1])
    
    def select_door(door):
        st.session_state.selected_door = door
        available_goat_doors = [i for i in range(3) if i != door and st.session_state.prizes[i] == '🐐']
        st.session_state.revealed_door = random.choice(available_goat_doors)
        st.session_state.final_choice = None
        st.session_state.result = None
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
                st.session_state.final_choice = remaining_door  # Switching always results in winning the car
            else:
                st.session_state.final_choice = st.session_state.selected_door  # Staying always results in getting a goat
    
    if st.session_state.final_choice is not None:
        final_choice = st.session_state.final_choice
        st.write("### 🎉 Final Result")
        st.write(f"You chose door **{final_choice + 1}**...")
        st.write(f"Behind the door: **{st.session_state.prizes[final_choice]}**")
        
        if switch_decision == "Switch":
            st.success("🏆 Congratulations! You won the **car**! 🚗")
            st.info("📊 By switching, you had a **2/3 chance** of winning the car. Since you first picked randomly, there was only a 1/3 chance the car was behind your door. The other two doors together had a 2/3 chance. When a goat is revealed, that 2/3 chance shifts to the remaining closed door, making switching the smarter move.")
        else:
            st.error("🐐 Oh no! You got a **goat**! Better luck next time!")
            st.info("📊 By staying, you only had a **1/3 chance** of winning the car. Your first pick was random, so you only had a 1 in 3 chance of choosing the car. Even after a goat is revealed, that probability doesn't change—it stays at 1/3, making switching the better option.")
        
        if st.button("🔄 Restart Game"):
            st.session_state.clear()
            st.rerun()



st.write("---")
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown('<p style="font-size:14px; font-weight:bold;">📖 What is the Monty Hall Problem?</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:14px;">The Monty Hall problem is a well-known probability puzzle from a game show. It challenges how we think about choices, uncertainty, and probability, often leading to surprising results.</p>', unsafe_allow_html=True)
    st.markdown('<a href="https://behavioralscientist.org/steven-pinker-rationality-why-you-should-always-switch-the-monty-hall-problem-finally-explained/" style="font-size:14px;">Read more</a>', unsafe_allow_html=True)

with col2:
    st.markdown('<p style="font-size:14px; font-weight:bold;">💡 How can this improve your everyday choices?</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:14px;">Think of it like picking a checkout line at the grocery store. If a new lane opens up and is moving faster, switching could increase your chances of getting through quicker. The Monty Hall concept teaches us that sometimes, reconsidering our choices based on new information can lead to better outcomes.</p>', unsafe_allow_html=True)

with col3:
    st.markdown('<p style="font-size:14px; font-weight:bold;">Behind the Build</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:14px;">Created by <a href="https://ifiecas.com/" style="font-size:14px;"><b>Ivy Fiecas-Borjal</b></a></p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:14px;">Inspired by the Predictive Analytics class discussion with Dr. Omid Sianaki from Victoria University, Melbourne, Australia (Feb 2025).</p>', unsafe_allow_html=True)
