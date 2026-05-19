import streamlit as st
import json
import os
from google import genai
from google.genai import types

# ==========================================
# 1. PAGE CONFIGURATION & SIDEBAR (BIA UI)
# ==========================================
st.set_page_config(page_title="Smart E-Commerce Agent", page_icon="🛍️", layout="wide")

# Beautiful left-hand status panel for your presentation
with st.sidebar:
    st.title("⚙️ Agent Dashboard")
    st.markdown("---")
    st.markdown("### **System Status**")
    st.success("🟢 Autonomous Agent Live")
    
    st.markdown("### **Model Architecture**")
    st.info("🧠 Gemini 2.5 Flash")
    
    st.markdown("### **Active Capabilities**")
    st.markdown("- 📚 **RAG:** Product & Policy Database")
    st.markdown("- 🛠️ **Tools:** Order Lookup (`get_order_status`)")
    st.markdown("- 🛠️ **Tools:** Returns (`create_return_request`)")
    st.markdown("- 🛡️ **Guardrails:** Human Escalation Fallback")
    
    st.markdown("---")
    st.caption("BIA Capstone Project • Developer: Hemant Sharma")

# ==========================================
# 2. MAIN HEADER INTERFACE
# ==========================================
st.title("🛍️ Smart E-Commerce Assistant")
st.write("Welcome! I am an autonomous AI agent capable of answering catalog questions, checking live orders, or routing you to human support if needed.")
st.markdown("---")

# Environment Check
if "GEMINI_API_KEY" not in os.environ:
    st.warning("Please set your GEMINI_API_KEY environment variable to run the agent.")
    st.stop()

client = genai.Client()

# ==========================================
# 3. KNOWLEDGE BASE & TOOLS DEFINITION
# ==========================================
@st.cache_data
def load_knowledge_base():
    policies, faq, products = "", "", ""
    if os.path.exists("Policies.md"):
        with open("Policies.md", "r", encoding="utf-8") as f: policies = f.read()
    if os.path.exists("FAQ.md"):
        with open("FAQ.md", "r", encoding="utf-8") as f: faq = f.read()
    if os.path.exists("Products.json"):
        with open("Products.json", "r", encoding="utf-8") as f: products = f.read()
    return f"--- STORE POLICIES ---\n{policies}\n\n--- FAQs ---\n{faq}\n\n--- PRODUCT CATALOG ---\n{products}"

knowledge_context = load_knowledge_base()

def get_order_status(order_id: str) -> str:
    """Retrieves the live delivery and shipping status of a customer's order using their Order ID."""
    mock_orders = {
        "12345": "Order #12345 has been SHIPPED. It arrives this Thursday.",
        "67890": "Order #67890 is currently PROCESSING at our warehouse.",
        "ABCDE": "Order #ABCDE has been DELIVERED to your front porch."
    }
    return mock_orders.get(order_id, f"Order ID '{order_id}' was not found. Please double-check.")

def create_return_request(order_id: str, reason: str) -> str:
    """Initiates and registers a formal return/refund request for an order given an order ID and a reason."""
    return f"Success! A return request for Order #{order_id} has been generated because: '{reason}'."

tools_map = {"get_order_status": get_order_status, "create_return_request": create_return_request}

# ==========================================
# 4. CHAT HISTORY DISPLAY
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Using native Streamlit markdown layout instead of raw text blocks
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# 5. AGENT LOGIC & EXECUTION
# ==========================================
if user_input := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Core System Instruction: Notice Guardrail #4 is now securely packed inside the system prompt string
    system_instruction = f"""
    You are an expert E-Commerce Customer Support AI Agent. Tone: polite and professional.
    
    1. RAG KNOWLEDGE: Use the context below to answer queries (e.g. shipping fees, monitor specs).
    {knowledge_context}
    
    2. TOOL CALLING: For order status or returns, ask for Order ID and use your tools.
    
    3. FALLBACK: If unresolved, say exactly: 'I am routing you to a live human support specialist who can assist you further.'
    
    4. SAFETY GUARDRAIL: If the user uses profanity, asks for competitor information, or displays abusive behavior, do not argue. Politely state: 'I am routing you to a manager to resolve this issue immediately' and stop.
    """

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=[get_order_status, create_return_request],
                temperature=0.3
            )
        )
        
        if response.function_calls:
            for function_call in response.function_calls:
                tool_name = function_call.name
                tool_args = function_call.args
                if tool_name in tools_map:
                    with st.spinner(f"Agent executing tool..."):
                        tool_result = tools_map[tool_name](**tool_args)
                    final_response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=f"The tool '{tool_name}' returned: {tool_result}. Summarize this for the customer.",
                        config=types.GenerateContentConfig(system_instruction=system_instruction)
                    )
                    ai_reply = final_response.text
                else:
                    ai_reply = "Routing you to human support."
        else:
            ai_reply = response.text

        response_placeholder.markdown(ai_reply)
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})