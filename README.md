# 🛡️ Crisis Support Chatbot — Powered by GROQ & LLaMA 3

This project hosts an advanced, adaptable chatbot built using **Gradio**, integrated with the **GROQ API** running **LLaMA 3**. Designed to assist users during times of crisis, the chatbot dynamically adapts to a user's needs by switching between four specialized variants — offering emotional support, survival logistics, disaster preparedness, and general crisis response.

## 🤖 Chatbot Variants

The chatbot, codenamed **ARK** (*Adaptive Response Keeper*), supports four intelligent personas:

### 🔵 Adaptive Crisis Response (**ARK**)
A versatile assistant trained to support individuals in all types of crises. Combines emotional support, practical advice, and preparedness strategies.  
> *"Calm, clear, and compassionate — ARK adapts to your situation."*

### 🟣 Emotional Support (**RAY**)
A gentle AI companion offering empathetic, kind, and reassuring dialogue during emotional stress or trauma.  
> *"RAY listens, comforts, and uplifts."*

### 🟢 Survival & Logistics (**BOLT**)
A tactical assistant offering step-by-step survival tips and emergency action plans.  
> *"BOLT delivers calm, clear, mission-critical survival guidance."*

### 🟡 Disaster Preparedness (**READYBOT**)
An AI focused on proactive planning and preparation before disaster strikes.  
> *"READYBOT helps you get ready, stay safe, and plan ahead."*

---

## 🧠 Features

- **Dynamic AI Behavior:** Tailors responses based on selected chatbot variant.
- **GROQ Integration:** Uses the `llama-3-70b-versatile` model for intelligent dialogue.
- **Gradio UI:** Clean and responsive interface built with `gr.Blocks`.
- **Custom Styling:** Each variant has its own background, color theme, and personality.
- **Streamed Replies:** Simulated typing for enhanced conversational feel.

---

## 🚀 Getting Started

1. **Clone the repo**  
   ```bash
    git clone https://github.com/your-username/your-chatbot-repo.git
    
    cd your-chatbot-repo
2. **Install Dependencies**
    ```
    pip install -r requirements.txt
3. **Generate API Key From Groq**
4. **Run the app**
5. ```
    Python app.py

## 🖼️ UI Preview
Each chatbot variant is color-coded and includes unique intro messages and styles. The app uses dynamic CSS generation to reflect the tone of the selected assistant.

## 🧩 Tech Stack
- Gradio

- GROQ API

- LLaMA 3 (via GroqCloud)

- Python 3.10+