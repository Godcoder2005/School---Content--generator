import streamlit as st
from backend import workflow

st.set_page_config(
    page_title="AI School Content Generator",
    page_icon="📚",
    layout="centered"
)

st.title("📚 AI Educational Content Generator")
st.markdown("Generate **grade-appropriate explanations and MCQs** with automatic review.")

# ---------------- INPUT SECTION ----------------

grade = st.number_input("Enter Grade", min_value=1, max_value=12, value=4)
topic = st.text_input("Enter Topic", placeholder="e.g., Types of Angles")

generate_btn = st.button("🚀 Generate Content")

# ---------------- GENERATION ----------------

if generate_btn:

    if not topic.strip():
        st.warning("⚠️ Please enter a topic.")
        st.stop()

    with st.spinner("Generating and reviewing content..."):

        result = workflow.invoke({
            "grade": grade,
            "topic": topic
        })

    # ---------------- DISPLAY EXPLANATION ----------------

    st.subheader("📖 Explanation")
    st.write(result.get("explanation", "No explanation generated."))

    # ---------------- DISPLAY MCQs ----------------

    st.subheader("📝 MCQ Questions")

    mcqs = result.get("mcq_questions", [])

    if mcqs:
        for i, q in enumerate(mcqs, start=1):
            st.markdown(f"**Q{i}. {q['question']}**")

            for opt_key, opt_val in q["options"].items():
                st.write(f"{opt_key}. {opt_val}")

            st.success(f"✔ Correct Answer: {q['answer']}")
            st.markdown("---")
    else:
        st.info("No MCQs generated.")

    # ---------------- REVIEW STATUS ----------------

    st.subheader("🔍 Review Result")

    status = result.get("status", "unknown")
    feedback = result.get("feedback", [])

    if status == "pass":
        st.success("✅ Content PASSED review")
    elif status == "fail":
        st.error("❌ Content FAILED review")
    else:
        st.warning("⚠️ Review status unknown")

    # ---------------- FEEDBACK ----------------

    if feedback:
        st.markdown("### 🛠 Feedback")
        for f in feedback:
            st.write(f"• {f}")