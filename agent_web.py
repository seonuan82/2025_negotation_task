import streamlit as st
from utility.llm import get_llm_response
from utility.logging import log

st.title("Negotiation Agent")

user_input = st.text_input("Your question to the agent:")
if user_input:
    response = get_llm_response(user_input)
    st.write("Agent:", response)
    
if 'round_number' not in st.session_state:
    st.session_state.round_number=1
    st.session_state.opponent_offers = [    # pre-set opponent's offer
        [2, 3, 2], [2, 3, 3], [2, 4, 3],
        [3, 4, 3], [3, 4, 4], [4, 4, 4]
    ]
    st.session_state.history = []
    st.session_state.accepted = False
    
st.title("Negotiation with John")

user_id = st.text_input("Enter your ID", key="user_id")  # enter user ID 

if user_id:
    current_offer = st.session_state.opponent_offers[st.session_state.round_number - 1]
    st.markdown(f"### Round {st.session_state.round_number}")
    st.markdown(f"**Opponent Offer**: Price-{current_offer[0]}, Warranty-{current_offer[1]}, Option-{current_offer[2]}")

    # Conversation with the Agent
    with st.expander("Need Help from Agent?"):
        user_question = st.text_input("Ask something to the Agent", key=f"question_{st.session_state.round_number}")
        if user_question:
            response = get_llm_response(user_question)
            st.write(f"**Agent**: {response}")
            log(f"User: {user_question}", user_id)
            log(f"Agent: {response}", user_id)

    # Accepting offer
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Accept Offer"):
            st.success("You accepted the offer.")
            st.session_state.accepted = True
            log("User accepted the offer", user_id)

    with col2:
        counter = st.text_input("Counter Offer (e.g., 3,4,2)", key=f"counter_{st.session_state.round_number}")
        if st.button("Submit Counter Offer"):
            log(f"User Counter Offer: {counter}", user_id)
            st.session_state.round_number += 1

    # End the negotiation
    if st.session_state.round_number > 6 or st.session_state.accepted:
        st.markdown("## Negotiation Summary")
        final_offer = current_offer
        final_response = "accept" if st.session_state.accepted else "no agreement"
        
        summary_prompt = f"""
Summary of negotiation:
- User ID: {user_id}
- Total Rounds: {min(st.session_state.round_number, 6)}
- Final Opponent Offer: {current_offer}
- Final User Response: {"accept" if st.session_state.accepted else "no agreement"}
How can I do better?
"""
        
        summary_agent = get_llm_response(summary_prompt)
               
        st.write(final_offer,"\n",final_response,"\n",summary_agent)
        log(f"Summary: {summary_agent}", user_id)
        st.stop()