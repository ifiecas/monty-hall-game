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

import streamlit.components.v1 as components

with col1:
    st.markdown(
        """
        <div style="
            padding: 25px; 
            background-color: #f8f9fa; 
            border-radius: 10px; 
            width: 100%; 
            line-height: 1.6;
            font-family: Arial, sans-serif;
            word-break: break-word;
        ">
            <h4 style="text-align: center; margin-bottom: 15px;">🎮 Welcome to the Monty Hall Game!</h4>
            <p style="text-align: justify;">
                Imagine you're on a thrilling game show, standing in front of three closed doors. 
                Behind one of them is the <b>grand prize – a brand-new car</b>! The other two hide goats. 
                Your goal? To drive away in that car!
            
            <h4 style="margin-top: 20px;">📜 How to Play: Read First!</h4>
            <p><b>1️⃣ Pick a door</b> (1, 2, or 3) – one of them hides the grand prize!</p>
            <p><b>2️⃣ The host, Monty Hall, who knows exactly where the car is</b>, will open a different door to reveal a goat.</p>
            <p><b>3️⃣ Now, you have a decision to make:</b> Stick with your original choice or switch to the remaining closed door.</p>
            <p><b>4️⃣ Final reveal:</b> The door you chose is opened – did you win the car or end up with a goat?</p>
            
            <p style="text-align: justify; font-size: 16px; margin-top: 20px;">
                🎲 <b>This app follows probability rules—</b>the door with the <b>highest probability</b> 
                will <b>always</b> have the car behind it!
            </p>            </p>
        </div>
        """,
        unsafe_allow_html=True
    )




with col2:
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
        st.write(f"Behind the door: {st.session_state.prizes[final_choice]}")
        
        if switch_decision == "Switch":
            st.success("🏆 Congratulations! You won the **car**! 🚗")
            st.info("📊 By switching, you had a **2/3 (67%) chance** of winning the car. Since you first picked randomly, there was only a 1/3 (33%) chance the car was behind your door. The other two doors together had a 2/3 (67%) chance. When a goat is revealed, that 2/3 chance shifts to the remaining closed door, **making switching the smarter move**.")
            st.info("📊 By staying, you only had a **1/3 (33%) chance** of winning the car. Your first pick was random, so you only had a 1 in 3 chance of choosing the car. Even after a goat is revealed, that probability doesn't change—it stays at 1/3 (33%), making switching the better option.")
        else:
            st.error("🐐 Oh no! You got a **goat**! Better luck next time!")
            st.info("📊 By staying, you only had a **1/3 (33%) chance** of winning the car. Your first pick was random, so you only had a 1 in 3 chance of choosing the car. Even after a goat is revealed, that probability doesn't change—it stays at 1/3 (33%), **making switching the better option**.")
            st.info("📊 By switching, you had a **2/3 (67%) chance** of winning the car. Since you first picked randomly, there was only a 1/3 chance the car was behind your door. The other two doors together had a 2/3 (67%) chance. When a goat is revealed, that 2/3 (67%) chance shifts to the remaining closed door, making switching the smarter move.")
        if st.button("🔄 Restart Game"):
            st.session_state.clear()
            st.rerun()

st.markdown("""
    <style>
        .footer-text {
            font-size: 13px;
            text-decoration: none;
        }
        .footer-text a, .footer-text a:visited, .footer-text a:active {
            font-size: 13px !important;  /* Force same font size */
            text-decoration: none;
            color: orange !important;  /* Ensure orange links */
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.write("---")
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("<p class='footer-text'><b>The Monty Hall Problem Explained</b></p>", unsafe_allow_html=True)
    st.markdown("<p class='footer-text'>The Monty Hall problem reveals how human intuition often struggles with probability and decision-making under uncertainty. It highlights several cognitive biases and reasoning errors that influence how we think.</p>", unsafe_allow_html=True)
    st.markdown("<p class='footer-text'><a href='https://behavioralscientist.org/steven-pinker-rationality-why-you-should-always-switch-the-monty-hall-problem-finally-explained/'>Read more</a></p>", unsafe_allow_html=True)

with col2:
    st.markdown("<p class='footer-text'><b>How can this improve your everyday choices?</b></p>", unsafe_allow_html=True)
    st.markdown("<p class='footer-text'>Think of it like picking a checkout line at the grocery store. If a new lane opens up and is moving faster, switching could increase your chances of getting through quicker. The Monty Hall concept teaches us that sometimes, reconsidering our choices based on new information can lead to better outcomes.</p>", unsafe_allow_html=True)

with col3:
    st.markdown("<p class='footer-text'><b>Behind the Build</b></p>", unsafe_allow_html=True)
    st.markdown("<p class='footer-text'>Created by <a href='https://ifiecas.com/'>Ivy Fiecas-Borjal</a></p>", unsafe_allow_html=True)
    st.markdown("<p class='footer-text'>Inspired by the Predictive Analytics class discussion with Dr. Omid Sianaki from Victoria University, Melbourne, Australia (Feb 2025).</p>", unsafe_allow_html=True)
