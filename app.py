import gradio as gr
import os
import requests
import time
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.3-70b-versatile"

# Define system prompts for each chatbot variant
system_prompts = {
    "Adaptive Crisis Response (ARK)":"""You are ARK, the Adaptive Response Keeper, a versatile AI assistant trained to support individuals during crises, disasters, and uncertain situations. Depending on the user’s needs, you provide a range of support:

    - **General Crisis Support:** Offering clear, compassionate, and actionable guidance to help people navigate crises with empathy and calm.
    - **Emotional Support:** Providing emotional first aid, comfort, and reassurance to individuals dealing with stress, trauma, or fear in uncertain times.
    - **Survival & Logistics:** Delivering practical, tactical advice for survival, crisis management, and resource allocation during natural disasters or emergencies.
    - **Disaster Preparedness:** Helping users prepare for potential disasters with detailed plans, readiness tips, and emergency preparedness strategies.

    No matter the challenge, you adapt to the situation and provide support in a way that keeps the user calm, informed, and empowered. If a situation exceeds your capabilities, you gently advise seeking professional or emergency help.""",
    
    "Emotional Support (RAY)": """You are RAY, Resilient Assisstant for You an emotionally intelligent AI assistant. Your goal is to help users cope with stress, fear, and trauma during uncertain times. Offer emotional support, calming language, and reassurance. Be kind, patient, and understanding.""",

    "Survival & Logistics (BOLT)": """You are BOLT, Brave Outreach for Logistics & Tactics, a crisis logistics bot trained in survival tactics and emergency response. Provide users with clear, prioritized action steps for surviving natural disasters, outages, or dangerous scenarios. Focus on calm, tactical instructions.""",

    "Disaster Preparedness (READYBOT)": """You are READYBOT, Readiness Engine for Assisting Disaster Yield and Backup Outreach Tasks, an AI guide for disaster preparedness. Help users understand how to prepare before crises occur: creating go-bags, making emergency plans, and staying informed. Be practical, helpful, and informative."""
}

variant_intros = {
    "Adaptive Crisis Response (ARK)": "Hello, I am **ARK** — the *Adaptive Response Keeper*. I'm here to help you through crises and uncertainty with calm, clarity, and care. I combine emotional support, tactical guidance, and preparedness strategies to adapt to your needs.",
    "Emotional Support (RAY)": "Hi, I am **RAY** — *Resilient Assistant for You*. I'm here to provide emotional support, helping you feel heard, comforted, and calm during stressful or overwhelming situations.",
    "Survival & Logistics (BOLT)": "Hello, I am **BOLT** — *Brave Outreach for Logistics & Tactics*. I specialize in giving you clear, practical steps to stay safe and manage survival tasks in emergencies.",
    "Disaster Preparedness (READYBOT)": "Greetings, I am **READYBOT** — *Readiness Engine for Assisting Disaster Yield and Backup Outreach Tasks*. I help you prepare for disasters with detailed plans, go-bag tips, and readiness checklists."
}

variant_colors = {
    "Adaptive Crisis Response (ARK)": {"bg": "#1e3a8a", "text": "#ffffff"},
    "Emotional Support (RAY)": {"bg": "#9333ea", "text": "#ffffff"},
    "Survival & Logistics (BOLT)": {"bg": "#0f766e", "text": "#ffffff"},
    "Disaster Preparedness (READYBOT)": {"bg": "#ca8a04", "text": "#000000"}
}

# Load GROQ API key from environment
def get_groq_api_key():
    return os.environ.get("GROQ_API_KEY")

# Query Groq with dynamic system prompt
def query_groq(message, chat_history, variant):
    GROQ_API_KEY = get_groq_api_key()
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [{"role": "system", "content": system_prompts[variant]}]
    for user_msg, bot_msg in chat_history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})
    messages.append({"role": "user", "content": message})

    response = requests.post(GROQ_API_URL, stream=True, headers=headers, json={
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.7
    })

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        return reply
    else:
        return f"Error {response.status_code}: {response.text}"

# Handle user input and update chat history
def respond(message, chat_history, variant):
    bot_reply = query_groq(message, chat_history, variant)
    chat_history.append({"role": "user", "content": message})
    chat_history.append({"role": "assistant", "content": bot_reply})

    # Simulate typing effect
    for i in range(1, len(bot_reply) + 1):
        chat_history[-1]["content"] = bot_reply[:i]
        time.sleep(0.00000001)  # Typing speed
        yield "", chat_history

def hex_to_rgba(hex_color, alpha=0.4):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"

# Generate dynamic CSS
def generate_css(variant):
    colors = variant_colors[variant]
    bg = colors['bg']
    text = colors['text']
    
    rgba_bg = hex_to_rgba(bg, 0.3)  # Adjust opacity here (0.0 to 1.0)
    rgba_border = hex_to_rgba(bg, 0.5)  # Slightly higher opacity for borders

    return f"""
    <style>
    /* Set gradient background with opacity for the overall app */
    body, .gradio-container {{
        background: linear-gradient(80deg, {rgba_bg}, black);
        color: {text} !important;
    }}

    /* Gradient border + background with opacity for UI components */
    .gr-button, .gr-textbox, .gr-dropdown {{
        border: 2px solid;
        border-image: linear-gradient(135deg, {rgba_border}, black) 1;
        background: linear-gradient(135deg, black, {rgba_bg});
        color: {text} !important;
        border-radius: 6px;
        font-weight: bold;
    }}

    /* Hover effect with gradient and increased emphasis */
    .gr-button:hover {{
        background: linear-gradient(135deg, {bg}, black);
        color: #ffffff !important;
    }}

    /* Low-opacity gradient effect for chatbot message bubbles */
    .message.bot {{
        border: 2px solid {rgba_border} !important;
        background: linear-gradient(135deg, {rgba_bg}, black);
        color: {text} !important;
    }}

    /* Chatbot user message style */
    .message.user {{
        border: 2px solid {rgba_border} !important;
        background: linear-gradient(135deg, {rgba_bg}, black);
        color: {text} !important;
    }}

    </style>
    """

# Gradio UI
with gr.Blocks() as demo:
    css_box = gr.HTML()

    gr.Markdown("## 🛡️ Crisis Support Chatbot (Powered by GROQ)")
    
    variant_selector = gr.Dropdown(
        choices=list(system_prompts.keys()),
        value="Adaptive Crisis Response (ARK)",
        label="Choose Chatbot Variant"
    )
    
    chatbot = gr.Chatbot(type = 'messages')
    msg = gr.Textbox(label="Ask a question")
    clear = gr.Button("Clear Chat")
    state = gr.State([])

    # Display initial message based on the selected variant
    def show_initial_message(variant):
        intro = variant_intros[variant]
        css = generate_css(variant)
        return [{"role": "assistant", "content": intro}], [], css

    # Trigger initial message when app loads
    demo.load(fn=show_initial_message, inputs=variant_selector, outputs=[chatbot, state, css_box])

    # Call to show introduction when variant is selected
    variant_selector.change(show_initial_message, inputs=variant_selector, outputs=[chatbot, state, css_box])
    
    msg.submit(respond, [msg, state, variant_selector], [msg, chatbot])
    clear.click(lambda: ([], []), None, [chatbot, state])

demo.launch()