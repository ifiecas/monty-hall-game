import streamlit as st
import numpy as np
import random

# Page configuration with custom theme
st.set_page_config(
    page_title="Monty Hall Game", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Restore the original banner image
st.image("https://i.postimg.cc/hP4tGy57/Picture-2.png", use_container_width=True)

# Custom CSS for better styling
st.markdown("""
    <style>
        /* Global font settings */
        * {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }
        
        /* Header styling */
        h1, h2, h3, h4, h5, h6 {
            font-weight: 600;
            color: #2c3e50;
        }
        
        /* Make buttons more appealing */
        .stButton button {
            font-weight: 500;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        /* Add hover effects to buttons */
        .stButton button:hover:enabled {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Improve radio buttons */
        .stRadio > div {
            padding: 10px;
            border-radius: 8px;
            background-color: #f8f9fa;
        }
        
        /* Door buttons styling */
        .door-button {
            padding: 30px 0 !important;
            font-size: 18px !important;
            margin: 10px 0 !important;
        }
        
        /* Make success and error messages more prominent */
        .stSuccess, .stError, .stInfo {
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }
        
        /* Game info box */
        .game-info {
            padding: 25px;
            background-color: #f8f9fa;
            border-radius: 10px;
            width: 100%;
            line-height: 1.6;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            word-break: break-word;
            border-left: 5px solid #3498db;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        
        /* Door container */
        .door-container {
            display: flex;
            justify-content: space-around;
            padding: 20px 0;
        }
        
        /* Door item */
        .door {
            text-align: center;
            transition: all 0.3s ease;
        }
        
        /* Footer styling */
        .footer-text {
            font-size: 13px;
            color: #7f8c8d;
            line-height: 1.5;
        }
        
        .footer-text a, .footer-text a:visited, .footer-text a:active {
            font-size: 13px !important;
            text-decoration: none;
            color: #e67e22 !important;
            font-weight: bold;
            transition: color 0.2s ease;
        }
        
        .footer-text a:hover {
            color: #d35400 !important;
        }
        
        /* Divider */
        hr {
            margin: 30px 0;
            border: 0;
            height: 1px;
            background-image: linear-gradient(to right, rgba(0,0,0,0), rgba(0,0,0,0.1), rgba(0,0,0,0));
        }
        
        /* Section separator */
        .section {
            margin: 30px 0;
        }
        
        /* Results animation */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .result-animation {
            animation: fadeIn 0.5s ease-out forwards;
        }
    </style>
""", unsafe_allow_html=True)

# Main content layout
col1, col2 = st.columns([1, 1.8], gap="large")

with col1:
    # Game instructions box
    st.markdown("""
        <div class="game-info">
            <h4 style="text-align: center; margin-bottom: 15px; color: #3498db;">🎮 How to Play: Read First!</h4>
            <div style="text-align: justify; margin-bottom: 15px;">
                Imagine you're on a thrilling game show, standing in front of three closed doors. 
                Behind one of them is the <b>grand prize – a brand-new car</b>! The other two hide goats. 
                Your goal? To drive away in that car!
            </div>
            <div style="margin: 20px 0;">
                <div style="margin-bottom: 10px;"><span style="display:inline-block; background-color: #3498db; color: white; border-radius: 50%; width: 25px; height: 25px; text-align: center; margin-right: 10px;">1</span> Pick a door (1, 2, or 3) – one of them hides the grand prize!</div>
                <div style="margin-bottom: 10px;"><span style="display:inline-block; background-color: #3498db; color: white; border-radius: 50%; width: 25px; height: 25px; text-align: center; margin-right: 10px;">2</span> The host, Monty Hall, who knows exactly where the car is, will open a different door to reveal a goat.</div>
                <div style="margin-bottom: 10px;"><span style="display:inline-block; background-color: #3498db; color: white; border-radius: 50%; width: 25px; height: 25px; text-align: center; margin-right: 10px;">3</span> Now, you have a decision to make: Stick with your original choice or switch to the remaining closed door.</div>
                <div style="margin-bottom: 10px;"><span style="display:inline-block; background-color: #3498db; color: white; border-radius: 50%; width: 25px; height: 25px; text-align: center; margin-right: 10px;">4</span> Final reveal: The door you chose is opened – did you win the car or end up with a goat?</div>
            </div>
            <div style="text-align: justify; font-size: 15px; margin-top: 15px; padding: 10px; background-color: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;">
                ⚠️ <b>Heads up!</b> This app follows probability rules—the door with the highest probability will always have the car behind it!
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Game area
    game_container = st.container()
    
    with game_container:
        if "prizes" not in st.session_state:
            car_position = random.randint(0, 2)
            st.session_state.prizes = ['🐐', '🐐', '🐐']
            st.session_state.prizes[car_position] = '🚗'
            st.session_state.selected_door = None
            st.session_state.revealed_door = None
            st.session_state.final_choice = None
            st.session_state.result = None
            st.session_state.switch_decision = None
            st.session_state.original_prizes = st.session_state.prizes.copy()

        # Door selection area
        st.markdown("<h3 style='color: #2c3e50;'>🚪 Choose a Door</h3>", unsafe_allow_html=True)
        
        # Door display with improved styling
        cols = st.columns([1, 1, 1])
        
        def select_door(door):
            st.session_state.selected_door = door
            available_goat_doors = [i for i in range(3) if i != door and st.session_state.prizes[i] == '🐐']
            st.session_state.revealed_door = random.choice(available_goat_doors)
            st.session_state.final_choice = None
            st.session_state.result = None
            st.session_state.switch_decision = None
        
        # Custom styled door buttons
        for i, col in enumerate(cols):
            door_label = f"Door {i + 1}"
            door_state = ""
            is_disabled = False
            
            if st.session_state.selected_door is not None:
                if i == st.session_state.selected_door:
                    door_label = f"Door {i + 1} (Your choice)"
                    door_state = "chosen"
                elif i == st.session_state.revealed_door:
                    door_label = f"Door {i + 1} (Goat revealed)"
                    door_state = "revealed"
                is_disabled = True
            
            # Door styling based on state
            if door_state == "chosen":
                door_style = "background-color: #e3f2fd; border: 2px solid #2196f3;"
            elif door_state == "revealed":
                door_style = "background-color: #ffebee; border: 2px solid #f44336;"
            else:
                door_style = "background-color: #f5f5f5; border: 2px solid #9e9e9e;"
            
            col.markdown(f"""
                <div style="text-align: center; padding: 10px;">
                    <div style="{door_style} border-radius: 8px; padding: 40px 10px; margin-bottom: 10px; text-align: center;">
                        <div style="font-size: 24px;">{'🚪' if door_state != 'revealed' else '🐐'}</div>
                        <div style="margin-top: 10px;">{door_label}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Button below the door display
            col.button(
                f"Select Door {i + 1}" if door_state == "" else door_label,
                key=f"door_{i}",
                on_click=select_door if door_state == "" else None,
                args=(i,) if door_state == "" else None,
                disabled=is_disabled,
                use_container_width=True
            )
        
        # Show host reveal and decision section
        if st.session_state.selected_door is not None and st.session_state.revealed_door is not None:
            st.markdown(f"""
                <div class="result-animation" style="background-color: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ffc107;">
                    <h4 style="color: #856404;">🐐 The host reveals a goat behind Door {st.session_state.revealed_door + 1}!</h4>
                    <p>Now comes the critical decision...</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Create a nicer decision box
            st.markdown("""
                <div style="background-color: #e8f4f8; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3498db;">
                    <h4 style="color: #2980b9;">🤔 Do you want to switch your choice?</h4>
                </div>
            """, unsafe_allow_html=True)
            
            remaining_door = [i for i in range(3) if i not in (st.session_state.selected_door, st.session_state.revealed_door)][0]
            
            # Better radio buttons for decision
            cols = st.columns(2)
            with cols[0]:
                stay_button = st.button(
                    f"STAY with Door {st.session_state.selected_door + 1}", 
                    use_container_width=True,
                    type="primary"
                )
                if stay_button:
                    st.session_state.switch_decision = "Stay"
                    st.session_state.final_choice = st.session_state.selected_door
                    # Always set the selected door to have a goat (for demonstration purposes)
                    st.session_state.prizes = ['🐐', '🐐', '🐐']
            
            with cols[1]:
                switch_button = st.button(
                    f"SWITCH to Door {remaining_door + 1}", 
                    use_container_width=True,
                    type="secondary"
                )
                if switch_button:
                    st.session_state.switch_decision = "Switch"
                    st.session_state.final_choice = remaining_door
                    # Always set the remaining door to have the car (for demonstration purposes)
                    st.session_state.prizes = ['🐐', '🐐', '🐐']
                    st.session_state.prizes[remaining_door] = '🚗'
        
        # Display the final result
        if st.session_state.final_choice is not None:
            final_choice = st.session_state.final_choice
            prize = st.session_state.prizes[final_choice]
            
            # Fancy result display
            st.markdown("""
                <div class="result-animation" style="background-color: #f0f7ff; padding: 25px; border-radius: 10px; margin: 30px 0; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                    <h3 style="color: #3498db; margin-bottom: 20px;">🎉 Final Result</h3>
                    <p style="font-size: 18px; margin-bottom: 15px;">You chose <b>Door {}</b>...</p>
                    <div style="font-size: 60px; margin: 20px 0;">{}</div>
                </div>
            """.format(final_choice + 1, prize), unsafe_allow_html=True)
            
            if prize == '🚗':
                st.success("🏆 **Congratulations!** You won the **car**! 🚗")
                explanation = """
                    <div style="padding: 20px; background-color: #e1f5fe; border-radius: 8px; margin: 20px 0; border-left: 4px solid #03a9f4;">
                        <h4 style="color: #0277bd;">📊 By switching, you had a <b>2/3 (67%)</b> chance of winning the car.</h4>
                        <p>This happens because:</p>
                        <ul>
                            <li>Your first pick had a <b>1/3 (33%)</b> chance of being the car</li>
                            <li>The other two doors together had a <b>2/3 (67%)</b> chance</li>
                            <li>When Monty reveals a goat, that <b>2/3 (67%)</b> probability shifts to the remaining door</li>
                            <li>Switching means you're betting that your original choice was wrong—which is statistically more likely</li>
                        </ul>
                        <p>The Monty Hall Problem demonstrates how our intuition about probability can be misleading!</p>
                    </div>
                    <div style="padding: 20px; background-color: #ffebee; border-radius: 8px; margin: 20px 0; border-left: 4px solid #f44336;">
                        <h4 style="color: #c62828;">📊 By staying, you only had a <b>1/3 (33%)</b> chance of winning the car.</h4>
                        <p>This happens because:</p>
                        <ul>
                            <li>Your initial choice was random with only a <b>1/3 (33%)</b> chance of being correct</li>
                            <li>Revealing a goat doesn't change this initial probability</li>
                            <li>The remaining door has a <b>2/3 (67%)</b> probability of hiding the car</li>
                            <li>This is why switching is the mathematically optimal strategy!</li>
                        </ul>
                        <p>The Monty Hall Problem is counter-intuitive, but the math doesn't lie!</p>
                    </div>
                """
                st.markdown(explanation, unsafe_allow_html=True)
            else:
                st.error("🐐 **Oh no!** You got a **goat**! Better luck next time!")
                explanation = """
                    <div style="padding: 20px; background-color: #ffebee; border-radius: 8px; margin: 20px 0; border-left: 4px solid #f44336;">
                        <h4 style="color: #c62828;">📊 By staying, you only had a <b>1/3 (33%)</b> chance of winning the car.</h4>
                        <p>This happens because:</p>
                        <ul>
                            <li>Your initial choice was random with only a <b>1/3 (33%)</b> chance of being correct</li>
                            <li>Revealing a goat doesn't change this initial probability</li>
                            <li>The remaining door has a <b>2/3 (67%)</b> probability of hiding the car</li>
                            <li>This is why switching is the mathematically optimal strategy!</li>
                        </ul>
                        <p>The Monty Hall Problem is counter-intuitive, but the math doesn't lie!</p>
                    </div>
                    <div style="padding: 20px; background-color: #e1f5fe; border-radius: 8px; margin: 20px 0; border-left: 4px solid #03a9f4;">
                        <h4 style="color: #0277bd;">📊 By switching, you had a <b>2/3 (67%)</b> chance of winning the car.</h4>
                        <p>This happens because:</p>
                        <ul>
                            <li>Your first pick had a <b>1/3 (33%)</b> chance of being the car</li>
                            <li>The other two doors together had a <b>2/3 (67%)</b> chance</li>
                            <li>When Monty reveals a goat, that <b>2/3 (67%)</b> probability shifts to the remaining door</li>
                            <li>Switching means you're betting that your original choice was wrong—which is statistically more likely</li>
                        </ul>
                        <p>The Monty Hall Problem demonstrates how our intuition about probability can be misleading!</p>
                    </div>
                """
                st.markdown(explanation, unsafe_allow_html=True)
            
            # Play again button with better styling
            if st.button("🔄 Restart Game", use_container_width=True, type="primary"):
                st.session_state.prizes = ['🐐', '🐐', '🐐']
                car_position = random.randint(0, 2)
                st.session_state.prizes[car_position] = '🚗'
                st.session_state.selected_door = None
                st.session_state.revealed_door = None
                st.session_state.final_choice = None
                st.session_state.result = None
                st.session_state.switch_decision = None
                st.session_state.original_prizes = st.session_state.prizes.copy()
                st.rerun()

# Footer section with improved styling
st.markdown("<hr>", unsafe_allow_html=True)
footer_cols = st.columns(3, gap="large")

with footer_cols[0]:
    st.markdown("<p class='footer-text'><b>The Monty Hall Problem Explained</b></p>", unsafe_allow_html=True)
    st.markdown("<p class='footer-text'>The Monty Hall problem reveals how human intuition often struggles with probability and decision-making under uncertainty. It highlights several cognitive biases and reasoning errors that influence how we think.</p>", unsafe_allow_html=True)
    st.markdown("<p class='footer-text'><a href='https://behavioralscientist.org/steven-pinker-rationality-why-you-should-always-switch-the-monty-hall-problem-finally-explained/'>Read more</a></p>", unsafe_allow_html=True)

with footer_cols[1]:
    st.markdown("<p class='footer-text'><b>How can this improve your everyday choices?</b></p>", unsafe_allow_html=True)
    st.markdown("<p class='footer-text'>Think of it like picking a checkout line at the grocery store. If a new lane opens up and is moving faster, switching could increase your chances of getting through quicker. The Monty Hall concept teaches us that sometimes, reconsidering our choices based on new information can lead to better outcomes.</p>", unsafe_allow_html=True)

with footer_cols[2]:
    st.markdown("<p class='footer-text'><b>Behind the Build</b></p>", unsafe_allow_html=True)
    st.markdown("<p class='footer-text'>Created by <a href='https://ifiecas.com/'><b>Ivy Fiecas-Borjal</b></a></p>", unsafe_allow_html=True)
    st.markdown("<p class='footer-text'>Inspired by the Predictive Analytics class discussion with Dr. Omid Sianaki from Victoria University, Melbourne, Australia (Feb 2025).</p>", unsafe_allow_html=True)
