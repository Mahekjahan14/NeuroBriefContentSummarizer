import streamlit as st
import os
from google import genai
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Set page config for a widescreen high-end dashboard experience
st.set_page_config(
    page_title="NeuroBrief AI Pro - Cognitive Content Hub",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. PREMIUM CUSTOM STYLE INJECTION (DARK GLASSMORPHISM) ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    /* Global styling overrides */
    html, body, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 10% 20%, #0b0f19 0%, #04060a 100%) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #e2e8f0 !important;
    }
    
    /* Header/Top Bar adjustment */
    [data-testid="stHeader"] {
        background-color: rgba(11, 15, 25, 0.5) !important;
        backdrop-filter: blur(12px) !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #070a12 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.5);
    }
    
    /* Premium Headers */
    h1, h2, h3, .stHeading {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }
    
    /* Neon Glow & Gradient text */
    .glow-text {
        background: linear-gradient(135deg, #a855f7 0%, #6366f1 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(99, 102, 241, 0.2);
    }
    
    /* Custom Glassmorphism Containers */
    .glass-card {
        background: rgba(16, 22, 37, 0.65) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        margin-bottom: 24px !important;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4) !important;
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.3) !important;
        box-shadow: 0 12px 40px 0 rgba(99, 102, 241, 0.15) !important;
    }

    /* Metric visual design */
    .metric-box {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        transition: transform 0.2s ease;
    }
    .metric-box:hover {
        transform: translateY(-2px);
        background: rgba(255, 255, 255, 0.04);
    }
    .metric-value {
        font-family: 'Outfit', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 4px;
        background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-value.purple {
        background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-value.rose {
        background: linear-gradient(135deg, #f43f5e 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Native Input Styling Override */
    div.stTextArea textarea {
        background-color: rgba(9, 13, 24, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        padding: 16px !important;
        transition: all 0.3s ease !important;
    }
    div.stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 12px rgba(99, 102, 241, 0.35) !important;
    }
    
    /* Elegant Button Customization */
    div.stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.02em !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.35) !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 28px rgba(168, 85, 247, 0.55) !important;
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%) !important;
    }
    div.stButton > button:active {
        transform: translateY(0px) !important;
    }
    
    /* Secondary Style Buttons (e.g. quick samples, exports) */
    .secondary-btn button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #f1f5f9 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: none !important;
    }
    .secondary-btn button:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        box-shadow: none !important;
        transform: none !important;
    }

    /* Sentiment Gauge UI */
    .sentiment-bar-bg {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 99px;
        height: 10px;
        position: relative;
        overflow: visible;
        margin: 20px 0;
    }
    .sentiment-bar-fill {
        background: linear-gradient(90deg, #f43f5e 0%, #3b82f6 50%, #10b981 100%);
        border-radius: 99px;
        height: 100%;
        width: 100%;
    }
    .sentiment-indicator {
        position: absolute;
        top: -6px;
        width: 22px;
        height: 22px;
        background: #ffffff;
        border: 4px solid #6366f1;
        border-radius: 50%;
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.8);
        transform: translateX(-50%);
        transition: left 0.5s ease-out;
    }
    
    /* Footer & System info details */
    .system-status {
        font-size: 0.8rem;
        color: #64748b;
        font-family: 'Courier New', Courier, monospace;
        margin-top: 10px;
    }
    
    /* Badge styling */
    .custom-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 99px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .badge-primary { background-color: rgba(99, 102, 241, 0.2); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.3); }
    .badge-success { background-color: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-warning { background-color: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 2. API KEY VALIDATION & INITIALIZATION ---
# Session state initialization for holding results across slider/layout updates
if "summary" not in st.session_state:
    st.session_state.summary = None
if "sentiment_score" not in st.session_state:
    st.session_state.sentiment_score = 0.0
if "sentiment_label" not in st.session_state:
    st.session_state.sentiment_label = "Neutral"
if "original_words" not in st.session_state:
    st.session_state.original_words = 0
if "summary_words" not in st.session_state:
    st.session_state.summary_words = 0

# Retrieve API keys from env as a convenient fallback
env_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""

# --- 3. SIDEBAR CONFIGURATION PANEL ---
with st.sidebar:
    st.markdown('<h2 style="color: #ffffff;">⚙️ Control Hub</h2>', unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 0.9rem;'>Fine-tune the Cognitive Summarizer engine parameters.</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 15px 0;'/>", unsafe_allow_html=True)
    
    # API key password input
    api_key_input = st.text_input(
        "Gemini API Key", 
        value=env_key,
        type="password",
        help="Paste your Gemini API key from Google AI Studio. Stored strictly locally in session state."
    )
    
    # API Key Status indicator
    if api_key_input:
        st.markdown('<span class="custom-badge badge-success">● API Key Connected</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="custom-badge badge-warning">○ API Key Missing</span>', unsafe_allow_html=True)
        st.markdown(
            "[Get free Gemini API Key ↗](https://aistudio.google.com/)", 
            help="Navigate to Google AI Studio to retrieve a free api key."
        )
        
    st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 15px 0;'/>", unsafe_allow_html=True)

    # Engine Model Selection
    model_choice = st.selectbox(
        "Cognitive Model",
        options=["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        index=0,
        help="Gemini 2.5 Flash is the latest ultra-fast model, optimized for speed and quality. Pro models are better for heavy reasoning and complex text."
    )
    
    # Precise Summary Format Mode
    format_choice = st.selectbox(
        "Summary Format",
        options=[
            "TL;DR (Single Sentence Bullet)", 
            "Key Highlights (Bullet Points)", 
            "Executive Narrative (Professional Paragraphs)",
            "Action Plan (Structured Steps & Takeaways)"
        ],
        index=1
    )
    
    # Tone settings
    tone_choice = st.selectbox(
        "Communication Tone",
        options=["Professional & Analytical", "Direct & Concise", "Technical & Precise", "Creative & Informative"],
        index=0
    )
    
    # FIXED: Precision summary target word count slider
    st.markdown("<label style='font-size: 0.85rem; font-weight: 500;'>Target Word Length</label>", unsafe_allow_html=True)
    target_word_len = st.slider(
        "Target Word Length",
        min_value=30,
        max_value=500,
        value=150,
        step=10,
        label_visibility="collapsed"
    )
    
    # Optional Steering Prompts
    custom_steering = st.text_input(
        "Steering Instruction (Optional)",
        placeholder="e.g. Focus on financial metrics, simplify technical terms",
        help="Extra prompt instructions passed to Gemini to direct the visual focus."
    )
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 15px 0;'/>", unsafe_allow_html=True)
    st.markdown(
        f'<div class="system-status">NEUROBRIEF ENGINE PRO v2.1<br/>TIME: {datetime.now().strftime("%Y-%m-%d %H:%M")}<br/>STATUS: READY</div>', 
        unsafe_allow_html=True
    )

# --- 4. HEADER LOGO BANNER ---
col_logo_1, col_logo_2 = st.columns([1, 10])
with col_logo_1:
    st.markdown("<h1 style='text-align: center; margin-top: 5px; font-size: 3.5rem;'>🧠</h1>", unsafe_allow_html=True)
with col_logo_2:
    st.markdown(
        """
        <h1 style='margin-bottom: 0px;'><span class='glow-text'>NeuroBrief AI Pro</span></h1>
        <p style='color: #94a3b8; font-size: 1.1rem; margin-top: 0px;'>Cognitive Intelligence Platform powered by Gemini & Natural Language Processing</p>
        """, 
        unsafe_allow_html=True
    )

# Sample Text Database for premium UX
SAMPLE_TEXTS = {
    "Artificial Intelligence Evolution": (
        "Artificial intelligence (AI) has undergone dramatic changes since the advent of deep neural networks. "
        "Historically, early AI relied on hand-coded expert systems that succeeded in narrow mathematical domains "
        "but failed completely when presented with noisy, real-world data. The paradigm shifted with deep learning, "
        "where systems learn features directly from raw data. Today, Large Language Models (LLMs) built on the Transformer "
        "architecture represent the state of the art. These architectures employ self-attention mechanisms to weigh "
        "the importance of different words in a sentence, allowing them to comprehend context over thousands of tokens. "
        "However, as commercial applications swell, concerns regarding computational overhead, environmental impact, "
        "hallucinations, and data privacy have intensified. Organizations are now shifting focus toward smaller, "
        "highly tuned specialized open-source models, retrieval-augmented generation (RAG), and green computing strategies "
        "to maintain efficiency while curtailing massive infrastructure costs."
    ),
    "Quantum Computing Breakthrough": (
        "Quantum computing operates on the foundational principles of quantum physics, using qubits instead of classical binary bits. "
        "While classical bits can only exist in a state of 0 or 1, qubits utilize superposition to exist as a complex probability amplitude of both simultaneously. "
        "Furthermore, entanglement allows qubits separated by vast distances to interact instantly, yielding exponential computational pathways. "
        "This technological shift promises to revolutionize cryptography, molecule modeling, financial forecasting, and optimization problems that "
        "would take supercomputers millennia to process. Despite this potential, the physical assembly of quantum machines remains extremely difficult. "
        "Qubits are highly sensitive to environmental thermal noise, electromagnetic interference, and mechanical vibrations, "
        "leading to 'decoherence' where the fragile quantum state collapses entirely. Researchers worldwide are racing to pioneer robust fault-tolerant quantum error correction, "
        "cooling machines to temperatures colder than deep space to maintain stability and unlock true quantum supremacy."
    ),
    "Global Microchip Supply Chains": (
        "The global semiconductor industry sits at the center of modern geopolitics and technological manufacturing. "
        "Nearly every digital device, from smart appliances to hypersonic defense networks, depends on advanced integrated circuits. "
        "However, the microchip manufacturing pipeline is highly consolidated and fragile. A single company in Taiwan, TSMC, "
        "manufactures over 90% of the world's most advanced microchips. The extreme ultraviolet (EUV) lithography systems required "
        "to print nanoscale transistors onto silicon wafers are built exclusively by ASML in the Netherlands. "
        "Any regional disruption, shipping channel blockade, or natural disaster could immediately halt global tech assembly lines. "
        "In response to this vulnerability, major global superpowers have launched multi-billion dollar domestic chip initiatives "
        "aimed at building local fabrication foundries. Nevertheless, building localized, fully decoupled wafer fabrication ecosystems "
        "requires trillions of dollars, deep specialized workforces, and decades of scientific development, keeping the global supply chain tightly codependent."
    )
}

# --- 5. MAIN CONTENT AREA ---
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("### 📝 Enter Source Material")

# Sample text buttons layout
col_sample_lbl, col_sample_1, col_sample_2, col_sample_3 = st.columns([2, 3, 3, 3])
with col_sample_lbl:
    st.markdown("<p style='margin-top: 10px; font-weight: 600; color: #94a3b8;'>Try a curated sample:</p>", unsafe_allow_html=True)

# We use session state to populate the text area
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

with col_sample_1:
    if st.button("🤖 AI Evolution", key="btn_sample_ai", use_container_width=True):
        st.session_state.input_text = SAMPLE_TEXTS["Artificial Intelligence Evolution"]
with col_sample_2:
    if st.button("🌌 Quantum Breakthrough", key="btn_sample_q", use_container_width=True):
        st.session_state.input_text = SAMPLE_TEXTS["Quantum Computing Breakthrough"]
with col_sample_3:
    if st.button("🔌 Supply Chains", key="btn_sample_chip", use_container_width=True):
        st.session_state.input_text = SAMPLE_TEXTS["Global Microchip Supply Chains"]

# Core Text input area
text = st.text_area(
    "Paste your content",
    value=st.session_state.input_text,
    placeholder="Paste long articles, academic transcripts, or technical specifications here (Up to 100,000 words)...",
    height=250,
    label_visibility="collapsed"
)
# Keep session state updated with text changes
st.session_state.input_text = text

# Core generation action
col_btn, col_empty = st.columns([1, 2])
with col_btn:
    generate_btn = st.button("🧠 Synthesize Knowledge", key="btn_generate")

st.markdown("</div>", unsafe_allow_html=True) # Close glass card

# --- 6. SUMMARIZATION ENGINE TRIGGER ---
if generate_btn:
    if not text.strip():
        st.error("⚠️ Content is empty. Please enter or paste some text to synthesize.")
    elif not api_key_input:
        st.error("🔑 Gemini API Key is missing! Please paste your key in the sidebar Control Hub to execute.")
    else:
        with st.spinner("🧠 Connecting to Cognitive Grid... Parsing syntax and executing summaries..."):
            try:
                # Initialize Gemini Client
                client = genai.Client(api_key=api_key_input)
                
                # Format prompts based on user custom constraints and sliders
                format_prompts = {
                    "TL;DR (Single Sentence Bullet)": "A single extremely dense, comprehensive one-sentence takeaway summarizing the entire text.",
                    "Key Highlights (Bullet Points)": "A bulleted list highlighting the most critical core arguments, key facts, and data points, styled in a clean logical layout.",
                    "Executive Narrative (Professional Paragraphs)": "A cohesive, rich, and highly professional narrative summary written in formal paragraphs.",
                    "Action Plan (Structured Steps & Takeaways)": "A structured action plan containing clear action items, lessons learned, and next steps extracted from the text."
                }
                
                format_instruction = format_prompts.get(format_choice, "A comprehensive bulleted summary of key facts.")
                
                prompt = f"""
                You are an elite research summarizer and high-frequency intelligence analyst.
                Your task is to summarize the following input text precisely.
                
                ### SUMMARY FORMAT:
                {format_instruction}
                
                ### COMMUNICATION TONE:
                {tone_choice}
                
                ### STRICT LENGTH REQUIREMENT:
                - The summary MUST be approximately {target_word_len} words long.
                - Please strictly obey this constraint. Do not output less than {max(20, target_word_len - 25)} words or more than {target_word_len + 30} words.
                """
                
                if custom_steering.strip():
                    prompt += f"\n\n### EXTRA CUSTOM STEERING INSTRUCTION:\n{custom_steering.strip()}"
                    
                prompt += f"\n\n### INPUT TEXT FOR ANALYSIS:\n{text}\n\nProvide only the final, styled markdown output without conversational intros or outros."
                
                # Generate content using modern Client
                response = client.models.generate_content(
                    model=model_choice,
                    contents=prompt
                )
                
                if response.text:
                    st.session_state.summary = response.text
                    
                    # Run TextBlob Sentiment Analysis
                    blob = TextBlob(response.text)
                    sentiment_score = blob.sentiment.polarity
                    st.session_state.sentiment_score = sentiment_score
                    
                    if sentiment_score > 0.15:
                        st.session_state.sentiment_label = "Positive 😊"
                    elif sentiment_score < -0.15:
                        st.session_state.sentiment_label = "Negative 😔"
                    else:
                        st.session_state.sentiment_label = "Neutral 😐"
                        
                    st.session_state.original_words = len(text.split())
                    st.session_state.summary_words = len(response.text.split())
                else:
                    st.error("Failed to generate response. The model returned empty content.")
                    
            except Exception as e:
                # Catch-all fallback for incorrect API keys or generic API glitches
                st.error(f"❌ Cognitive Engine Error: {str(e)}")
                st.markdown(
                    """
                    <div style='background: rgba(244, 63, 94, 0.1); border: 1px solid rgba(244, 63, 94, 0.3); padding: 16px; border-radius: 12px;'>
                        <strong style='color: #f43f5e;'>Troubleshooting Steps:</strong>
                        <ol style='margin-top: 8px; color: #cbd5e1;'>
                            <li>Verify your API Key in the sidebar has no trailing/leading spaces.</li>
                            <li>Ensure your network connection allows access to `generativelanguage.googleapis.com`.</li>
                            <li>If you have reached model rate limits, switch to <strong>gemini-2.5-flash</strong> or <strong>gemini-1.5-flash</strong> for better quota.</li>
                        </ol>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

# --- 7. DUAL-COLUMN RESULTS DASHBOARD ---
if st.session_state.summary:
    st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 30px 0;'/>", unsafe_allow_html=True)
    
    col_out_left, col_out_right = st.columns([5, 4])
    
    # --- LEFT COLUMN: COGNITIVE SUMMARY OUTPUT ---
    with col_out_left:
        st.markdown("<div class='glass-card' style='height: 100%;'>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <h3 style='margin: 0;'><span class='glow-text'>🧠 Executive Summary</span></h3>
                <span class='custom-badge badge-primary'>{format_choice.split(' ')[0]}</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Display the formatted Markdown Summary beautifully
        st.markdown(
            f"""
            <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 20px; min-height: 250px; margin-top: 15px; line-height: 1.7;'>
                {st.session_state.summary}
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Action actions row
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        col_act_1, col_act_2 = st.columns([1, 1])
        
        with col_act_1:
            st.download_button(
                label="📥 Download Text Briefing",
                data=st.session_state.summary,
                file_name=f"NeuroBrief_Summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True,
                key="btn_dl_summary"
            )
            
        with col_act_2:
            # Clipboard helper note: streamlit doesn't support writing to client clipboard natively without js
            # We can use a neat raw HTML workaround or simply provide an input text block that can be selected/copied easily.
            st.markdown(
                """
                <div style='text-align: center; margin-top: 8px;'>
                    <span style='color: #64748b; font-size: 0.85rem;'>💡 Double-click text above to select and copy</span>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
        st.markdown("</div>", unsafe_allow_html=True)
        
    # --- RIGHT COLUMN: INTELLECTUAL ANALYTICS ---
    with col_out_right:
        st.markdown("<div class='glass-card' style='height: 100%;'>", unsafe_allow_html=True)
        st.markdown("### 📊 Intellectual Analytics")
        
        # Compression ratio mathematics
        orig_cnt = max(1, st.session_state.original_words)
        summ_cnt = st.session_state.summary_words
        reduction_percentage = round((1 - (summ_cnt / orig_cnt)) * 100)
        
        # Grid layout for beautiful metric cards
        col_met_1, col_met_2, col_met_3 = st.columns(3)
        with col_met_1:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-value">{orig_cnt}</div>
                    <div class="metric-label">Original Words</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_met_2:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-value purple">{summ_cnt}</div>
                    <div class="metric-label">Brief Words</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_met_3:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-value rose">-{reduction_percentage}%</div>
                    <div class="metric-label">Reduction Ratio</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 20px 0;'/>", unsafe_allow_html=True)
        
        # Sentiment Gauges
        st.markdown(
            f"""
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <strong style='color: #94a3b8; font-size: 0.95rem;'>🎭 Brief Sentiment Analysis</strong>
                <span class='custom-badge badge-primary'>{st.session_state.sentiment_label}</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Convert sentiment polarity (-1.0 to +1.0) into gauge coordinates (0% to 100%)
        # Formula: (polarity + 1) / 2 * 100
        gauge_pos = int((st.session_state.sentiment_score + 1.0) / 2.0 * 100)
        
        st.markdown(
            f"""
            <div class="sentiment-bar-bg">
                <div class="sentiment-bar-fill"></div>
                <div class="sentiment-indicator" style="left: {gauge_pos}%;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; color: #64748b; font-size: 0.8rem; margin-top: -10px;">
                <span>Negative (-1.0)</span>
                <span>Neutral (0.0)</span>
                <span>Positive (+1.0)</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 20px 0;'/>", unsafe_allow_html=True)
        
        # Word Cloud visualization with theme matching colors
        st.markdown("<strong style='color: #94a3b8; font-size: 0.95rem; display: block; margin-bottom: 10px;'>☁️ Cognitive Word Frequency</strong>", unsafe_allow_html=True)
        
        try:
            # Generate word cloud using summary text
            text_for_cloud = st.session_state.summary
            # Clean generic symbols/markdown syntax
            for char in ["*", "#", "-", ">", "`", "[", "]", "(", ")"]:
                text_for_cloud = text_for_cloud.replace(char, "")
                
            # Create word cloud with nice matching dark/purple aesthetics
            # Background transparency / dark background matching body
            wordcloud = WordCloud(
                width=800, 
                height=380, 
                background_color="#0d111b",
                colormap="cool", # custom theme matching cool neon palette
                max_words=45,
                contour_color="rgba(99, 102, 241, 0.3)",
                contour_width=1,
                prefer_horizontal=0.85
            ).generate(text_for_cloud)
            
            fig, ax = plt.subplots(figsize=(8, 3.8), facecolor='#0d111b')
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            plt.tight_layout(pad=0)
            
            # Render to streamlit cleanly
            st.pyplot(fig)
            
        except Exception as e:
            st.warning(f"Could not generate word cloud visual: {str(e)}")
            
        st.markdown("</div>", unsafe_allow_html=True)
