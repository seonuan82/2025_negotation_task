### agent_web.py (Streamlit 기반 Negotiation 시뮬레이션 - 화면 분할 및 스크롤 추가)

import streamlit as st
from utility.llm import get_llm_response
from utility.logging import log

# 초기화
if 'round_number' not in st.session_state:
    st.session_state.round_number = 1
    st.session_state.opponent_offers = [
        [2, 3, 2], [2, 3, 3], [2, 4, 3],
        [3, 4, 3], [3, 4, 4], [4, 4, 4]
    ]
    st.session_state.accepted = False
    st.session_state.finished = False
    st.session_state.agent_log = []

st.title("🧠 Negotiation with John")

# 사용자 ID 입력
user_id = st.text_input("Enter your ID to begin:", key="user_id")

if user_id and not st.session_state.finished:
    round_num = st.session_state.round_number
    current_offer = st.session_state.opponent_offers[round_num - 1]

    col1, col2 = st.columns(2)

    # 왼쪽 - Opponent Offer 및 요약
    with col1:
        st.markdown(f"### 🤝 Round {round_num} - Opponent Offer")
        st.markdown(f"- Price: **{current_offer[0]}**")
        st.markdown(f"- Warranty: **{current_offer[1]}**")
        st.markdown(f"- Option: **{current_offer[2]}**")

        # 행동 선택: 수락 또는 카운터 오퍼
        st.markdown("---")
        col_accept, col_counter = st.columns(2)
        with col_accept:
            if st.button("✅ Accept Offer"):
                st.success("You accepted the offer.")
                st.session_state.accepted = True
                st.session_state.finished = True
                log("User accepted the offer", user_id)

        with col_counter:
            counter_offer = st.text_input("💬 Counter Offer (e.g., 3,4,2)", key=f"counter_{round_num}")
            if st.button("📨 Submit Counter Offer"):
                if counter_offer:
                    log(f"User Counter Offer: {counter_offer}", user_id)
                    st.session_state.round_number += 1
                    if st.session_state.round_number > 6:
                        st.session_state.finished = True
                else:
                    st.warning("Please enter a valid counter offer.")

    # 오른쪽 - Agent 대화 로그
    with col2:
        st.markdown("### 🤖 Agent Support")
        agent_box = st.container()

        user_question = st.text_input("Ask your agent something:", key=f"q_{round_num}")
        if user_question:
            response = get_llm_response(user_question)
            st.session_state.agent_log.append((user_question, response))
            log(f"User: {user_question}", user_id)
            log(f"Agent: {response}", user_id)

        with agent_box:
            st.markdown("<div style='max-height: 400px; overflow-y: auto;'>", unsafe_allow_html=True)
            for q, a in st.session_state.agent_log:
                st.markdown(f"<b>You:</b> {q}<br><b>Agent:</b> {a}<hr>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# 협상 종료 요약
if user_id and st.session_state.finished:
    final_offer = st.session_state.opponent_offers[st.session_state.round_number - 1 if st.session_state.round_number <= 6 else 5]
    final_response = "accept" if st.session_state.accepted else "no agreement"

    st.markdown("---")
    st.markdown("## 📋 Negotiation Summary")
    st.markdown(f"- User ID: `{user_id}`")
    st.markdown(f"- Rounds Played: `{min(st.session_state.round_number, 6)}`")
    st.markdown(f"- Final Opponent Offer: `{final_offer}`")
    st.markdown(f"- Final User Response: `{final_response}`")

    summary_prompt = f"""
Summary of negotiation:
- User ID: {user_id}
- Total Rounds: {min(st.session_state.round_number, 6)}
- Final Opponent Offer: {final_offer}
- Final User Response: {final_response}
How can I do better?
"""
    summary_response = get_llm_response(summary_prompt)
    st.markdown(f"**Agent Feedback:**\n{summary_response}")
    log(f"Summary: {summary_response}", user_id)
    st.stop()
