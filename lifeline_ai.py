"""
LifeLine AI – Pre-Hospital Emergency Decision Support System
A comprehensive emergency response application with multimodal AI support
"""

import streamlit as st
import time
import base64
import json
from datetime import datetime, timedelta
from io import BytesIO
import re

# Page Configuration
st.set_page_config(
    page_title="LifeLine AI - Emergency Support",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Glassmorphism + Pastel Emergency Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Pastel gradient background - Emergency theme */
    .main {
        background: linear-gradient(135deg, #ff6b6b 0%, #ffd93d 100%);
        background-attachment: fixed;
    }
    
    /* Glassmorphism sidebar */
    [data-testid="stSidebar"] {
        background: rgba(255, 240, 245, 0.7);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Headers with gradient - Emergency colors */
    h1, h2, h3, h4, h5, h6 {
        color: #b71c1c !important;
        font-weight: 700;
    }
    
    h1 {
        background: linear-gradient(135deg, #d32f2f 0%, #ff6b6b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.4);
        transition: all 0.3s ease;
        animation: fadeIn 0.6s ease-out;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Hero section with glassmorphism */
    .hero-section {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.8), rgba(255, 217, 61, 0.8));
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 3rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-bottom: 2rem;
        animation: heroFadeIn 1s ease-out;
    }
    
    @keyframes heroFadeIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .hero-logo {
        font-size: 4rem;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .hero-title {
        color: white !important;
        font-size: 3.5rem;
        font-weight: 900;
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .hero-subtitle {
        color: white;
        font-size: 1.5rem;
        font-weight: 400;
        opacity: 0.95;
    }
    
    /* Pastel buttons - Emergency theme */
    .stButton>button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8787 100%);
        color: white;
        border-radius: 15px;
        height: 3.5em;
        width: 100%;
        font-size: 1.1em;
        font-weight: 700;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #ff5252 0%, #ff6b6b 100%);
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.5);
    }
    
    .stButton>button:active {
        transform: translateY(0px);
    }
    
    /* Metric cards with glassmorphism */
    .metric-glass-card {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.85), rgba(255, 135, 135, 0.85));
        backdrop-filter: blur(15px);
        padding: 1.8rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .metric-glass-card:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 12px 40px rgba(255, 107, 107, 0.4);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 900;
        margin: 0.5rem 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .metric-label {
        font-size: 1rem;
        font-weight: 600;
        opacity: 0.95;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Alert boxes with glassmorphism */
    .glass-alert-success {
        background: rgba(76, 175, 80, 0.15);
        backdrop-filter: blur(10px);
        border-left: 4px solid #4CAF50;
        padding: 1.5rem;
        border-radius: 15px;
        color: #2e7d32;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.1);
        animation: fadeIn 0.5s ease-out;
    }
    
    .glass-alert-warning {
        background: rgba(255, 152, 0, 0.15);
        backdrop-filter: blur(10px);
        border-left: 4px solid #FF9800;
        padding: 1.5rem;
        border-radius: 15px;
        color: #e65100;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(255, 152, 0, 0.1);
        animation: fadeIn 0.5s ease-out;
    }
    
    .glass-alert-info {
        background: rgba(33, 150, 243, 0.15);
        backdrop-filter: blur(10px);
        border-left: 4px solid #2196F3;
        padding: 1.5rem;
        border-radius: 15px;
        color: #0d47a1;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(33, 150, 243, 0.1);
        animation: fadeIn 0.5s ease-out;
    }
    
    .glass-alert-danger {
        background: rgba(244, 67, 54, 0.15);
        backdrop-filter: blur(10px);
        border-left: 4px solid #F44336;
        padding: 1.5rem;
        border-radius: 15px;
        color: #b71c1c;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(244, 67, 54, 0.1);
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Tech badges */
    .tech-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
        backdrop-filter: blur(10px);
        padding: 0.5rem 1rem;
        border-radius: 12px;
        margin: 0.3rem;
        font-size: 0.85rem;
        font-weight: 600;
        color: #b71c1c;
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .tech-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 240, 245, 0.9));
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 3rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-top: 3rem;
    }
    
    /* Critical Alert Box */
    .critical-alert {
        background: linear-gradient(135deg, #ff0000, #cc0000);
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin: 20px 0;
        border: 4px solid white;
        box-shadow: 0 0 30px rgba(255,0,0,0.5);
        animation: pulse 2s infinite;
        backdrop-filter: blur(10px);
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* Urgent Alert Box */
    .urgent-alert {
        background: linear-gradient(135deg, rgba(255, 140, 0, 0.9), rgba(255, 102, 0, 0.9));
        backdrop-filter: blur(15px);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin: 20px 0;
        border: 3px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 8px 32px rgba(255, 140, 0, 0.3);
    }
    
    /* Monitor Alert Box */
    .monitor-alert {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.9), rgba(255, 183, 0, 0.9));
        backdrop-filter: blur(15px);
        color: #1a1a2e;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        margin: 20px 0;
        border: 3px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 8px 32px rgba(255, 215, 0, 0.3);
    }
    
    /* Step Card */
    .step-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(15px);
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        border-left: 8px solid #00ff88;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.4);
        transition: all 0.3s ease;
    }
    
    .step-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    .step-number {
        background: linear-gradient(135deg, #00ff88 0%, #00d4aa 100%);
        color: white;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: bold;
        margin-right: 15px;
        box-shadow: 0 4px 15px rgba(0, 255, 136, 0.3);
    }
    
    /* Timer Display */
    .timer-display {
        background: rgba(0, 0, 0, 0.85);
        backdrop-filter: blur(15px);
        color: #00ff88;
        padding: 15px 30px;
        border-radius: 15px;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
        border: 2px solid #00ff88;
        box-shadow: 0 4px 15px rgba(0, 255, 136, 0.3);
    }
    
    /* Warning Banner */
    .warning-banner {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.95), rgba(255, 82, 82, 0.95));
        backdrop-filter: blur(15px);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        text-align: center;
        font-weight: bold;
        border: 3px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 8px 32px rgba(255, 107, 107, 0.3);
    }
    
    /* Info Card */
    .info-card {
        background: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border-left: 5px solid #00ff88;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Summary Box */
    .summary-box {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(15px);
        color: #1a1a2e;
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        border: 3px solid #00ff88;
        font-family: monospace;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Large Text for Accessibility */
    .large-text {
        font-size: 20px;
        line-height: 1.6;
    }
    
    /* Input fields styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 2px solid rgba(255, 107, 107, 0.3);
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #ff6b6b;
        box-shadow: 0 0 20px rgba(255, 107, 107, 0.3);
    }
    
    /* Radio buttons */
    .stRadio>div {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
def init_session_state():
    """Initialize all session state variables"""
    if 'emergency_active' not in st.session_state:
        st.session_state.emergency_active = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'steps_completed' not in st.session_state:
        st.session_state.steps_completed = []
    if 'emergency_data' not in st.session_state:
        st.session_state.emergency_data = {}
    if 'severity_level' not in st.session_state:
        st.session_state.severity_level = None
    if 'emergency_type' not in st.session_state:
        st.session_state.emergency_type = None
    if 'user_actions' not in st.session_state:
        st.session_state.user_actions = []
    if 'show_summary' not in st.session_state:
        st.session_state.show_summary = False
    if 'classification_reasoning' not in st.session_state:
        st.session_state.classification_reasoning = None

init_session_state()

# ============================================================================
# AI-ASSISTED TRIAGE ENGINE
# ============================================================================

class EmergencyClassifier:
    """AI-assisted emergency triage and classification system"""
    
    # Emergency keywords and patterns
    CRITICAL_KEYWORDS = [
        'not breathing', 'unconscious', 'collapsed', 'unresponsive',
        'severe bleeding', 'chest pain', 'heart attack', 'stroke',
        'seizure', 'heavy bleeding', 'can\'t breathe', 'choking badly'
    ]
    
    URGENT_KEYWORDS = [
        'bleeding', 'burn', 'broken bone', 'fracture', 'choking',
        'difficulty breathing', 'severe pain', 'head injury',
        'allergic reaction', 'high fever', 'vomiting blood'
    ]
    
    MONITOR_KEYWORDS = [
        'minor cut', 'small burn', 'sprain', 'bruise', 'headache',
        'nausea', 'dizziness', 'minor pain', 'small wound'
    ]
    
    # Emergency type patterns
    EMERGENCY_TYPES = {
        'cardiac_arrest': ['not breathing', 'unconscious', 'no pulse', 'collapsed', 'unresponsive', 'heart stopped'],
        'severe_bleeding': ['severe bleeding', 'heavy bleeding', 'blood gushing', 'arterial bleeding', 'profuse bleeding'],
        'choking': ['choking', 'can\'t breathe', 'something stuck', 'airway blocked'],
        'burns': ['burn', 'burned', 'scalded', 'fire', 'hot liquid'],
        'fracture': ['broken bone', 'fracture', 'bone broke', 'deformed limb'],
        'head_injury': ['head injury', 'hit head', 'head trauma', 'fell on head'],
        'breathing_difficulty': ['difficulty breathing', 'hard to breathe', 'gasping', 'wheezing'],
        'allergic_reaction': ['allergic reaction', 'swelling', 'hives', 'anaphylaxis'],
        'stroke': ['stroke', 'face drooping', 'arm weakness', 'speech difficulty'],
        'poisoning': ['poisoning', 'swallowed', 'overdose', 'toxic']
    }
    
    @staticmethod
    def classify_emergency(description, image_analysis=None):
        """
        Classify emergency based on text description and optional image analysis
        Returns: (severity_level, emergency_type, reasoning)
        """
        description_lower = description.lower()
        
        # FAIL-SAFE FIRST: If input is unclear or empty, default to URGENT + recommend 911
        if not description or len(description.strip()) < 5:
            return ('urgent', 'general_emergency', 'Unclear situation - recommending urgent assessment')
        
        # Check for critical keywords
        for keyword in EmergencyClassifier.CRITICAL_KEYWORDS:
            if keyword in description_lower:
                emergency_type = EmergencyClassifier._detect_emergency_type(description_lower)
                reasoning = f'Critical keywords detected: life-threatening indicators present'
                return ('critical', emergency_type, reasoning)
        
        # Check for urgent keywords
        for keyword in EmergencyClassifier.URGENT_KEYWORDS:
            if keyword in description_lower:
                emergency_type = EmergencyClassifier._detect_emergency_type(description_lower)
                reasoning = f'Urgent keywords detected: prompt medical attention needed'
                return ('urgent', emergency_type, reasoning)
        
        # Check for monitor keywords
        for keyword in EmergencyClassifier.MONITOR_KEYWORDS:
            if keyword in description_lower:
                emergency_type = EmergencyClassifier._detect_emergency_type(description_lower)
                reasoning = f'Monitoring keywords detected: assess and watch situation'
                return ('monitor', emergency_type, reasoning)
        
        # FAIL-SAFE DEFAULT: When unclear, always err on side of caution
        emergency_type = EmergencyClassifier._detect_emergency_type(description_lower)
        reasoning = 'Unable to determine clear severity - defaulting to urgent for safety'
        return ('urgent', emergency_type, reasoning)
    
    @staticmethod
    def _detect_emergency_type(description):
        """Detect specific emergency type from description"""
        for emergency_type, keywords in EmergencyClassifier.EMERGENCY_TYPES.items():
            for keyword in keywords:
                if keyword in description:
                    return emergency_type
        return 'general_emergency'
    
    @staticmethod
    def analyze_image_for_injuries(image_data):
        """
        Image analysis for PRESENCE of visible injury patterns only.
        
        This detects whether visible injury patterns are present (blood, burns, wounds)
        but does NOT assess severity, make diagnoses, or provide medical interpretation.
        
        Purpose: Help triage by confirming visual evidence mentioned in description.
        
        Returns basic presence indicators only.
        
        IMPORTANT: Image analysis is optional and never changes severity classification alone.
        The classification is always primarily based on the text description.
        """
        # If no image provided, return no injury detected
        if image_data is None:
            return {
                'visible_injury_present': False,
                'pattern_type': None,
                'note': 'No image provided for analysis'
            }
        
        # Simulated analysis - in production, this would use computer vision
        # to detect PRESENCE (not severity) of injury patterns
        # For demo purposes, we simulate detection of visible patterns
        
        # CRITICAL: Image analysis never escalates severity by itself
        # Text description always drives the classification decision
        return {
            'visible_injury_present': True,
            'pattern_type': 'visible_wound_pattern',  # Not a diagnosis
            'note': 'Visual confirmation only - not diagnostic'
        }

# ============================================================================
# EMERGENCY GUIDANCE MODULES
# ============================================================================

class EmergencyGuidance:
    """Rule-based emergency guidance with step-by-step instructions"""
    
    @staticmethod
    def get_guidance_steps(emergency_type):
        """Get step-by-step guidance for emergency type"""
        guidance_map = {
            'cardiac_arrest': EmergencyGuidance.cpr_steps(),
            'severe_bleeding': EmergencyGuidance.bleeding_control_steps(),
            'choking': EmergencyGuidance.choking_steps(),
            'burns': EmergencyGuidance.burn_first_aid_steps(),
            'breathing_difficulty': EmergencyGuidance.breathing_assistance_steps(),
            'fracture': EmergencyGuidance.fracture_care_steps(),
            'head_injury': EmergencyGuidance.head_injury_steps(),
            'allergic_reaction': EmergencyGuidance.allergic_reaction_steps(),
            'stroke': EmergencyGuidance.stroke_steps(),
            'general_emergency': EmergencyGuidance.general_emergency_steps()
        }
        
        return guidance_map.get(emergency_type, EmergencyGuidance.general_emergency_steps())
    
    @staticmethod
    def cpr_steps():
        """CPR guidance steps"""
        return [
            {
                'title': 'Check Responsiveness & Call for Help',
                'instruction': 'Tap the person\'s shoulders and shout "Are you OK?" If no response, immediately call emergency services (911 or local number). Put your phone on speaker.',
                'details': [
                    'Ensure the scene is safe',
                    'Check if person is breathing normally',
                    '⚠️ IF YOU ARE ALONE: Call 911 first, put phone on speaker, then start CPR',
                    'IF OTHERS PRESENT: Have someone else call while you start CPR'
                ],
                'warning': 'Do not delay calling emergency services. If alone, use speaker phone so you can continue CPR while talking to dispatcher'
            },
            {
                'title': 'Position the Person',
                'instruction': 'Place the person on their back on a firm, flat surface. Kneel beside their chest.',
                'details': [
                    'Remove any pillows from under head',
                    'Ensure head, neck, and spine are aligned',
                    'Clear area around the person'
                ],
                'warning': None
            },
            {
                'title': 'Hand Position for Compressions',
                'instruction': 'Place the heel of one hand on the center of the chest (between nipples). Place your other hand on top and interlock fingers.',
                'details': [
                    'Keep your arms straight',
                    'Position your shoulders directly above your hands',
                    'Keep fingers off the chest'
                ],
                'warning': 'Compressions must be on the breastbone, not the ribs'
            },
            {
                'title': 'Begin Chest Compressions',
                'instruction': 'Push hard and fast in the center of the chest at least 2 inches deep. Do 30 compressions at a rate of 100-120 per minute (think of the beat of "Stayin\' Alive").',
                'details': [
                    'Allow chest to fully recoil between compressions',
                    'Minimize interruptions',
                    'Count out loud: 1, 2, 3... up to 30'
                ],
                'warning': 'Compressions must be continuous and at correct depth'
            },
            {
                'title': 'Continue CPR Cycles',
                'instruction': 'Continue cycles of 30 compressions. Do NOT stop until help arrives or person shows signs of life.',
                'details': [
                    'Keep going - you cannot harm someone who needs CPR',
                    'Switch with another person if available to avoid fatigue',
                    'Continue until paramedics arrive'
                ],
                'warning': 'Do not stop CPR unless person starts breathing or moving'
            }
        ]
    
    @staticmethod
    def bleeding_control_steps():
        """Bleeding control guidance"""
        return [
            {
                'title': 'Ensure Your Safety First',
                'instruction': 'Protect yourself with gloves if available. If not available, use plastic bags, clean cloth, or multiple layers of fabric.',
                'details': [
                    'Avoid direct contact with blood when possible',
                    'Call emergency services immediately for severe bleeding'
                ],
                'warning': 'Your safety is important - protect yourself first'
            },
            {
                'title': 'Apply Direct Pressure',
                'instruction': 'Place a clean cloth or gauze directly on the wound and press firmly with your hand. Do not peek to see if bleeding has stopped.',
                'details': [
                    'Use both hands if needed',
                    'Apply steady, firm pressure',
                    'Do not remove the cloth even if blood soaks through'
                ],
                'warning': 'Maintain constant pressure - do not lift to check'
            },
            {
                'title': 'Add More Material if Needed',
                'instruction': 'If blood soaks through, add more cloth or gauze on top. Do NOT remove the original cloth.',
                'details': [
                    'Keep applying firm pressure',
                    'Use heavier pressure if bleeding continues',
                    'Elevate the wound above heart level if possible'
                ],
                'warning': 'Never remove blood-soaked material'
            },
            {
                'title': 'Secure the Dressing',
                'instruction': 'Once bleeding slows, wrap the wound firmly with bandage or cloth. Keep the pressure on.',
                'details': [
                    'Wrap snugly but not too tight',
                    'Check that fingers/toes remain pink and warm',
                    'Keep the person calm and still'
                ],
                'warning': 'Watch for signs of shock: pale skin, rapid breathing, weakness'
            },
            {
                'title': 'Monitor Until Help Arrives',
                'instruction': 'Keep the person lying down. Watch for signs of shock. Reassure them. Do not give anything to eat or drink.',
                'details': [
                    'Cover with blanket to keep warm',
                    'Talk to them - keep them conscious if possible',
                    'Recheck bandages regularly'
                ],
                'warning': 'If bleeding restarts, apply more pressure immediately'
            }
        ]
    
    @staticmethod
    def choking_steps():
        """Choking assistance steps"""
        return [
            {
                'title': 'Assess the Situation',
                'instruction': 'Ask "Are you choking?" If person can cough or speak, encourage coughing. If person cannot breathe, cough, or speak, begin abdominal thrusts immediately.',
                'details': [
                    'Universal sign of choking: hands clutching throat',
                    'Person may be unable to speak',
                    'Skin may turn blue'
                ],
                'warning': 'If person can breathe or cough, do NOT perform abdominal thrusts'
            },
            {
                'title': 'Call for Help',
                'instruction': 'Have someone call emergency services. If alone, perform abdominal thrusts first, then call.',
                'details': [
                    '⚠️ IF ALONE: Do 5 abdominal thrusts first, then call 911 on speaker and continue',
                    'IF OTHERS PRESENT: Have them call immediately while you help',
                    'Time is critical - act fast'
                ],
                'warning': 'If alone, do NOT delay action to make phone call first. Do thrusts, then call on speaker.'
            },
            {
                'title': 'Position for Abdominal Thrusts',
                'instruction': 'Stand behind the person. Wrap your arms around their waist. Make a fist with one hand and place it just above the navel.',
                'details': [
                    'Position your fist below the ribcage',
                    'Grasp your fist with your other hand',
                    'Person should be standing or sitting upright'
                ],
                'warning': 'Do not position fist over ribs or at the very bottom of breastbone'
            },
            {
                'title': 'Perform Abdominal Thrusts (Heimlich)',
                'instruction': 'Give quick, upward thrusts into the abdomen. Perform 5 thrusts, then check if object is dislodged.',
                'details': [
                    'Each thrust should be forceful',
                    'Thrust inward and upward',
                    'Repeat until object comes out or person becomes unconscious'
                ],
                'warning': 'Use forceful thrusts - this is a life-threatening situation'
            },
            {
                'title': 'If Person Becomes Unconscious',
                'instruction': 'Lower person to ground. Begin CPR starting with chest compressions. Check mouth for object before giving breaths.',
                'details': [
                    'Perform 30 chest compressions',
                    'Look in mouth for object',
                    'Remove only if clearly visible',
                    'Continue CPR until help arrives'
                ],
                'warning': 'Do not perform finger sweeps blindly - can push object deeper'
            }
        ]
    
    @staticmethod
    def burn_first_aid_steps():
        """Burn first aid steps"""
        return [
            {
                'title': 'Stop the Burning Process',
                'instruction': 'Remove person from heat source. Remove any clothing or jewelry near burned area (unless stuck to skin).',
                'details': [
                    'Stop, drop, and roll if clothing is on fire',
                    'Turn off heat source if safe',
                    'Remove jewelry before swelling starts'
                ],
                'warning': 'Do NOT remove anything stuck to the burn'
            },
            {
                'title': 'Cool the Burn',
                'instruction': 'Run cool (not cold) water over burn for 10-20 minutes. Do not use ice.',
                'details': [
                    'Use cool running water if possible',
                    'Can also use cool, wet compresses',
                    'For chemical burns, continue flushing for 20 minutes minimum'
                ],
                'warning': 'Never use ice, butter, or ointments on fresh burns'
            },
            {
                'title': 'Cover the Burn',
                'instruction': 'Cover burn loosely with sterile, non-stick bandage or clean cloth.',
                'details': [
                    'Do not apply tight bandages',
                    'Use non-stick gauze if available',
                    'Do not break any blisters'
                ],
                'warning': 'Do not use fluffy cotton or materials that can stick to burn'
            },
            {
                'title': 'Manage Pain',
                'instruction': 'Elevate burned area above heart level if possible. Keep person warm with blanket on unburned areas.',
                'details': [
                    'Elevation helps reduce swelling',
                    'Watch for signs of shock',
                    'Reassure the person'
                ],
                'warning': 'Seek immediate medical help for severe burns, burns on face/hands/feet/genitals, or burns larger than 3 inches'
            },
            {
                'title': 'Monitor and Wait for Help',
                'instruction': 'Do not give anything to eat or drink. Watch for shock symptoms. Keep burn covered and clean.',
                'details': [
                    'Signs of shock: pale, cold, clammy skin; rapid breathing',
                    'Keep person calm',
                    'Do not apply ointments or creams'
                ],
                'warning': 'All serious burns require professional medical evaluation'
            }
        ]
    
    @staticmethod
    def breathing_assistance_steps():
        """Breathing difficulty assistance"""
        return [
            {
                'title': 'Call Emergency Services Immediately',
                'instruction': 'Call 911 or your local emergency number. Breathing difficulty is serious.',
                'details': [
                    'State clearly: "Medical emergency - difficulty breathing"',
                    'Provide your location',
                    'Stay on the line'
                ],
                'warning': 'Difficulty breathing can become life-threatening quickly'
            },
            {
                'title': 'Help Person Into Comfortable Position',
                'instruction': 'Help person sit upright or in a position that makes breathing easier. Do not lay them flat.',
                'details': [
                    'Sitting upright usually helps most',
                    'Leaning slightly forward can help',
                    'Loosen any tight clothing'
                ],
                'warning': 'Do not force person to lie down'
            },
            {
                'title': 'Check for Medications',
                'instruction': 'If person has asthma inhaler or prescribed breathing medication, help them use it.',
                'details': [
                    'Follow instructions on medication',
                    'Shake inhaler before use',
                    'Help them take slow, deep breaths'
                ],
                'warning': 'Only use medications prescribed to that person'
            },
            {
                'title': 'Keep Person Calm',
                'instruction': 'Speak calmly and reassuringly. Encourage slow, controlled breathing.',
                'details': [
                    'Anxiety can worsen breathing difficulty',
                    'Breathe with them to show rhythm',
                    'Open windows for fresh air'
                ],
                'warning': 'If breathing stops, begin CPR immediately'
            },
            {
                'title': 'Monitor Until Help Arrives',
                'instruction': 'Watch for changes in condition. Be ready to start CPR if person stops breathing.',
                'details': [
                    'Watch skin color - blue tint is emergency',
                    'Note if person becomes confused or drowsy',
                    'Time how long between breaths'
                ],
                'warning': 'If person becomes unconscious, begin CPR'
            }
        ]
    
    @staticmethod
    def fracture_care_steps():
        """Fracture/broken bone care"""
        return [
            {
                'title': 'Do Not Move the Person',
                'instruction': 'Unless in immediate danger, do not move the person. Call emergency services.',
                'details': [
                    'Movement can worsen injury',
                    'Spinal injuries require special care',
                    'Wait for professional help'
                ],
                'warning': 'Do not try to realign the bone or push bone back in'
            },
            {
                'title': 'Immobilize the Injured Area',
                'instruction': 'Support the injured area in the position found. Use padding and splints if available.',
                'details': [
                    'Can use rolled newspapers, boards, or pillows as splints',
                    'Pad the splint with soft material',
                    'Secure above and below the fracture'
                ],
                'warning': 'Do not tie too tight - check circulation regularly'
            },
            {
                'title': 'Control Any Bleeding',
                'instruction': 'If there is bleeding, apply gentle pressure with clean cloth around (not on) the fracture site.',
                'details': [
                    'Do not press directly on protruding bone',
                    'Apply pressure around the wound',
                    'Cover open wounds with sterile dressing'
                ],
                'warning': 'Do not wash wound or try to push bone back'
            },
            {
                'title': 'Treat for Shock',
                'instruction': 'Keep person lying down and warm. Elevate legs slightly if no spinal injury suspected.',
                'details': [
                    'Cover with blanket',
                    'Do not give food or drink',
                    'Reassure the person'
                ],
                'warning': 'Watch for signs of shock: pale, cold, rapid breathing'
            }
        ]
    
    @staticmethod
    def head_injury_steps():
        """Head injury care"""
        return [
            {
                'title': 'Call Emergency Services',
                'instruction': 'Any significant head injury requires medical evaluation. Call 911.',
                'details': [
                    'Head injuries can be serious even without visible damage',
                    'Provide your exact location',
                    'Describe what happened'
                ],
                'warning': 'Do not move person if neck injury is suspected'
            },
            {
                'title': 'Keep Person Still',
                'instruction': 'Keep the person lying down with head and shoulders slightly elevated. Stabilize the head and neck.',
                'details': [
                    'Do not move unless absolutely necessary',
                    'Support head in position found',
                    'Watch for vomiting'
                ],
                'warning': 'Assume neck injury until proven otherwise'
            },
            {
                'title': 'Control Any Bleeding',
                'instruction': 'Apply gentle pressure with clean cloth. Do not press hard if skull fracture suspected.',
                'details': [
                    'Do not remove objects stuck in wound',
                    'Do not clean deep wounds',
                    'Apply pressure around wound, not directly on it if skull fracture suspected'
                ],
                'warning': 'Do not apply direct pressure if you suspect skull fracture'
            },
            {
                'title': 'Monitor Consciousness',
                'instruction': 'Keep person awake and talking if possible. Watch for changes in consciousness.',
                'details': [
                    'Ask simple questions repeatedly',
                    'Note any confusion or drowsiness',
                    'Watch for seizures'
                ],
                'warning': 'Loss of consciousness, even briefly, is serious'
            }
        ]
    
    @staticmethod
    def allergic_reaction_steps():
        """Allergic reaction assistance"""
        return [
            {
                'title': 'Assess Severity',
                'instruction': 'Look for signs of severe reaction: difficulty breathing, swelling of face/throat, rapid pulse, dizziness. If severe, call 911 immediately.',
                'details': [
                    'Mild: rash, itching, hives',
                    'Severe: breathing difficulty, swelling, confusion',
                    'Anaphylaxis requires immediate emergency care'
                ],
                'warning': 'Severe allergic reactions can be life-threatening'
            },
            {
                'title': 'Use Epinephrine if Available',
                'instruction': 'If person has epinephrine auto-injector (EpiPen) and reaction is severe, help them use it immediately.',
                'details': [
                    'Inject into outer thigh muscle',
                    'Hold for 3 seconds',
                    'Can inject through clothing if needed',
                    'Call 911 immediately after using'
                ],
                'warning': 'Always call emergency services after using epinephrine'
            },
            {
                'title': 'Position the Person',
                'instruction': 'Have person lie flat with legs elevated (unless they\'re vomiting or having trouble breathing).',
                'details': [
                    'If breathing difficulty: sit them upright',
                    'If vomiting: turn on side',
                    'If unconscious: recovery position'
                ],
                'warning': 'Position depends on symptoms'
            },
            {
                'title': 'Monitor and Reassure',
                'instruction': 'Stay with person. Watch for worsening symptoms. Be ready to perform CPR if needed.',
                'details': [
                    'Second reaction can occur',
                    'Keep person calm',
                    'Do not give anything by mouth if trouble breathing'
                ],
                'warning': 'Symptoms can worsen rapidly'
            }
        ]
    
    @staticmethod
    def stroke_steps():
        """Stroke response steps (F.A.S.T.)"""
        return [
            {
                'title': 'Call 911 Immediately',
                'instruction': 'Stroke is a medical emergency. Every second counts. Call emergency services immediately.',
                'details': [
                    'Note the time symptoms started',
                    'This information is critical for treatment',
                    'Do not drive person to hospital yourself'
                ],
                'warning': 'Time is brain - immediate medical care is critical'
            },
            {
                'title': 'F.A.S.T. Assessment',
                'instruction': 'Check for stroke signs: Face drooping, Arm weakness, Speech difficulty, Time to call 911.',
                'details': [
                    'Face: Ask person to smile. Is one side drooping?',
                    'Arms: Ask person to raise both arms. Does one drift down?',
                    'Speech: Ask person to repeat a simple sentence. Is speech slurred?',
                    'Time: Note time symptoms started'
                ],
                'warning': 'Do not wait to see if symptoms go away'
            },
            {
                'title': 'Keep Person Comfortable',
                'instruction': 'Have person lie down with head and shoulders slightly raised. Loosen tight clothing.',
                'details': [
                    'Turn head to side if vomiting',
                    'Do not give anything to eat or drink',
                    'Keep person calm'
                ],
                'warning': 'Do not give aspirin or other medications unless directed by emergency services'
            },
            {
                'title': 'Monitor Condition',
                'instruction': 'Watch for changes. Be prepared to perform CPR if person stops breathing.',
                'details': [
                    'Check breathing regularly',
                    'Note any new symptoms',
                    'Stay with person until help arrives'
                ],
                'warning': 'Condition can deteriorate rapidly'
            }
        ]
    
    @staticmethod
    def general_emergency_steps():
        """General emergency response steps"""
        return [
            {
                'title': 'Assess the Situation',
                'instruction': 'Ensure scene is safe. Check if person is responsive. Call emergency services if needed.',
                'details': [
                    'Do not put yourself in danger',
                    'Shout for help',
                    'Call 911 if situation is serious'
                ],
                'warning': 'Your safety comes first'
            },
            {
                'title': 'Call for Help',
                'instruction': 'Call emergency services and describe the situation clearly.',
                'details': [
                    'State your location',
                    'Describe what happened',
                    'Follow dispatcher instructions',
                    'Stay on the line'
                ],
                'warning': 'Do not hang up until told to do so'
            },
            {
                'title': 'Provide Comfort',
                'instruction': 'Keep person calm and comfortable. Reassure them that help is coming.',
                'details': [
                    'Keep person still unless in danger',
                    'Cover with blanket if cold',
                    'Talk reassuringly'
                ],
                'warning': 'Do not move person unless absolutely necessary'
            },
            {
                'title': 'Monitor Condition',
                'instruction': 'Watch for changes in condition. Be ready to start CPR if needed.',
                'details': [
                    'Check breathing regularly',
                    'Watch for signs of shock',
                    'Note any changes to tell paramedics'
                ],
                'warning': 'If condition worsens, update emergency services immediately'
            }
        ]

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_elapsed_time():
    """Calculate elapsed time since emergency started"""
    if st.session_state.start_time:
        elapsed = datetime.now() - st.session_state.start_time
        minutes = int(elapsed.total_seconds() // 60)
        seconds = int(elapsed.total_seconds() % 60)
        return f"{minutes:02d}:{seconds:02d}"
    return "00:00"

def display_timer():
    """Display emergency timer"""
    elapsed = get_elapsed_time()
    st.markdown(f"""
        <div class="timer-display">
            ⏱️ Time Elapsed: {elapsed}
        </div>
    """, unsafe_allow_html=True)

def display_severity_alert(severity, emergency_type):
    """Display severity level alert"""
    severity_info = {
        'critical': {
            'emoji': '🔴',
            'title': 'CRITICAL EMERGENCY',
            'class': 'critical-alert',
            'message': 'Immediate action required. Life-threatening situation.'
        },
        'urgent': {
            'emoji': '🟠',
            'title': 'URGENT SITUATION',
            'class': 'urgent-alert',
            'message': 'Prompt medical attention needed.'
        },
        'monitor': {
            'emoji': '🟡',
            'title': 'MONITOR SITUATION',
            'class': 'monitor-alert',
            'message': 'Assess and monitor. Seek medical advice if worsens.'
        }
    }
    
    info = severity_info.get(severity, severity_info['urgent'])
    emergency_display = emergency_type.replace('_', ' ').title()
    
    st.markdown(f"""
        <div class="{info['class']}">
            {info['emoji']} {info['title']}<br>
            {emergency_display}<br>
            <div style="font-size: 18px; margin-top: 10px;">{info['message']}</div>
        </div>
    """, unsafe_allow_html=True)

def display_safety_disclaimer():
    """Display safety and ethics disclaimer"""
    st.markdown("""
        <div class="glass-alert-danger">
            <h3 style="margin-top: 0; color: #b71c1c !important;">⚠️ IMPORTANT DISCLAIMER</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="glass-card">
            <div class="large-text">
            <strong>This is DECISION SUPPORT, NOT MEDICAL DIAGNOSIS</strong><br><br>
            
            ✓ This tool provides emergency guidance based on symptoms described<br>
            ✓ It is NOT a substitute for professional medical care<br>
            ✓ ALWAYS call emergency services (911) for serious emergencies<br>
            ✓ Follow instructions from emergency dispatchers and paramedics<br>
            ✓ This tool cannot diagnose conditions or prescribe treatments<br><br>
            
            <strong>When in doubt, always call 911</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)

def generate_emergency_summary():
    """Generate comprehensive emergency summary"""
    elapsed = get_elapsed_time()
    emergency_type = st.session_state.emergency_type or 'Unknown'
    severity = st.session_state.severity_level or 'Unknown'
    
    summary = f"""
╔═══════════════════════════════════════════════════════════╗
                    EMERGENCY INCIDENT SUMMARY
╚═══════════════════════════════════════════════════════════╝

INCIDENT DETAILS:
─────────────────────────────────────────────────────────────
Emergency Type:     {emergency_type.replace('_', ' ').title()}
Severity Level:     {severity.upper()}
Time Elapsed:       {elapsed}
Timestamp:          {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SITUATION DESCRIPTION:
─────────────────────────────────────────────────────────────
{st.session_state.emergency_data.get('description', 'No description provided')}

ACTIONS TAKEN:
─────────────────────────────────────────────────────────────
"""
    
    if st.session_state.user_actions:
        for i, action in enumerate(st.session_state.user_actions, 1):
            summary += f"{i}. {action}\n"
    else:
        summary += "No actions recorded yet\n"
    
    summary += f"""
COMPLETED STEPS:
─────────────────────────────────────────────────────────────
"""
    
    if st.session_state.steps_completed:
        for step in st.session_state.steps_completed:
            summary += f"✓ {step}\n"
    else:
        summary += "No steps completed yet\n"
    
    summary += """
─────────────────────────────────────────────────────────────
NEXT STEPS:
• Continue following guidance steps
• Provide this summary to paramedics when they arrive
• Do not leave person unattended
• Continue monitoring condition

⚠️ This summary is for emergency responders only
⚠️ This is not a medical diagnosis
╚═══════════════════════════════════════════════════════════╝
    """
    
    return summary

def text_to_speech_placeholder(text):
    """Placeholder for text-to-speech functionality"""
    st.info(f"🔊 Text-to-Speech: Would read aloud: '{text[:100]}...'")

# ============================================================================
# MAIN APPLICATION INTERFACE
# ============================================================================

def main():
    """Main application interface"""
    
    # Header - removed because hero section replaces it
    
    # Navigation
    if not st.session_state.emergency_active:
        show_home_screen()
    else:
        show_emergency_interface()

def show_home_screen():
    """Show home screen with emergency intake options"""
    
    # Hero Section with Glassmorphism
    st.markdown("""
        <div class="hero-section">
            <div class="hero-logo">🚨</div>
            <div class="hero-title">LifeLine AI</div>
            <div class="hero-subtitle">Pre-Hospital Emergency Decision Support System</div>
            <div style="margin-top: 1.5rem;">
                <span class="tech-badge">🤖 AI-Assisted Triage</span>
                <span class="tech-badge">🔍 Explainable Decisions</span>
                <span class="tech-badge">🛡️ Safety-First</span>
                <span class="tech-badge">♿ Accessibility-First</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Safety disclaimer
    display_safety_disclaimer()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Emergency intake section
    st.markdown("### 📝 Describe the Emergency")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Multimodal input options
        input_method = st.radio(
            "Choose input method:",
            ["💬 Text Input", "🎙️ Voice Input (Simulated)", "📸 Image Upload"],
            horizontal=True
        )
        
        emergency_description = ""
        uploaded_image = None
        
        if input_method == "💬 Text Input":
            emergency_description = st.text_area(
                "Describe what happened:",
                height=150,
                placeholder="Example: 'Person collapsed and is not breathing' or 'Severe bleeding from arm injury'"
            )
        
        elif input_method == "🎙️ Voice Input (Simulated)":
            st.info("🎙️ In production: Click to record voice input. Speech-to-text will transcribe automatically.")
            
            # Demo voice input options
            voice_demo = st.selectbox(
                "Select simulated voice input:",
                [
                    "Select a demo scenario...",
                    "Person collapsed and is not breathing",
                    "Severe bleeding from leg wound",
                    "Child is choking on food",
                    "Elderly person with chest pain",
                    "Someone had a bad fall and hit their head"
                ]
            )
            
            if voice_demo != "Select a demo scenario...":
                emergency_description = voice_demo
                st.success(f"🎙️ Voice captured: '{voice_demo}'")
        
        elif input_method == "📸 Image Upload":
            st.info("📸 Upload image of visible injury (optional - enhances assessment)")
            uploaded_image = st.file_uploader(
                "Upload image:",
                type=['png', 'jpg', 'jpeg'],
                help="Images help assess visible injuries like burns, bleeding, or wounds"
            )
            
            emergency_description = st.text_area(
                "Also describe the situation:",
                height=100,
                placeholder="Describe what you see..."
            )
            
            if uploaded_image:
                st.image(uploaded_image, caption="Uploaded Image", width=300)
    
    with col2:
        st.markdown("### 🚀 Quick Scenarios")
        st.markdown("Click to test:")
        
        if st.button("🔴 Cardiac Arrest", use_container_width=True):
            start_emergency("Person collapsed, not breathing, unresponsive")
        
        if st.button("🩸 Severe Bleeding", use_container_width=True):
            start_emergency("Heavy bleeding from deep cut on arm")
        
        if st.button("🫁 Choking", use_container_width=True):
            start_emergency("Person is choking and cannot breathe")
        
        if st.button("🔥 Burns", use_container_width=True):
            start_emergency("Person burned by hot liquid, severe pain")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Start emergency button
    if emergency_description:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚨 START EMERGENCY ASSESSMENT", use_container_width=True, type="primary"):
                start_emergency(emergency_description, uploaded_image)
    
    # Additional information section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    
    with st.expander("ℹ️ About LifeLine AI"):
        st.markdown("""
            <div class="glass-card">
            <div class="large-text">
            <strong>LifeLine AI</strong> is an AI-assisted emergency decision support tool designed to help bystanders 
            and first responders take appropriate action before professional medical help arrives.
            
            <br><br><strong>Features:</strong><br>
            ✓ Multimodal input (text, voice, images)<br>
            ✓ AI-assisted triage classification<br>
            ✓ Step-by-step emergency guidance<br>
            ✓ Emergency summary generation<br>
            ✓ Designed for non-medical users<br>
            
            <br><strong>Important:</strong><br>
            • This is NOT a medical diagnosis tool<br>
            • Always call emergency services for serious situations<br>
            • Follow professional medical advice when available<br>
            </div>
            </div>
        """, unsafe_allow_html=True)
    
    with st.expander("📞 When to Call 911"):
        st.markdown("""
            <div class="glass-card">
            <div class="large-text">
            <strong>Call 911 immediately if:</strong><br><br>
            
            🔴 Person is unconscious or unresponsive<br>
            🔴 Not breathing or difficulty breathing<br>
            🔴 Severe bleeding that won't stop<br>
            🔴 Chest pain or pressure<br>
            🔴 Signs of stroke (face drooping, arm weakness, speech difficulty)<br>
            🔴 Severe allergic reaction<br>
            🔴 Seizures<br>
            🔴 Severe burns<br>
            🔴 Suspected poisoning<br>
            🔴 Serious head injury<br>
            🔴 Severe pain<br>
            
            <br><strong>When in doubt, always call 911</strong>
            </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Beautiful Footer
    st.markdown("""
        <div class="footer">
            <div class="hero-logo" style="font-size: 2.5rem;">🚨</div>
            <h3 style="color: #b71c1c !important; margin: 1rem 0;">LifeLine AI</h3>
            <p style="font-size: 1.2rem; color: #666; margin-bottom: 1.5rem;">
                AI-Assisted Emergency Decision Support — Saving Lives Before Help Arrives
            </p>
            <div style="margin: 1.5rem 0;">
                <span class="tech-badge">🤖 AI-Assisted</span>
                <span class="tech-badge">🔍 Explainable</span>
                <span class="tech-badge">🛡️ Safety-First</span>
                <span class="tech-badge">♿ Accessible</span>
            </div>
            <p style="opacity: 0.7; font-size: 0.95rem; margin-top: 2rem;">
                Comprehensive AI-for-Good Prototype | Emergency Response Innovation<br>
                Built with Python + Streamlit | Responsible AI Framework
            </p>
            <p style="opacity: 0.6; font-size: 0.85rem; margin-top: 1rem;">
                ⚠️ Educational & Demonstration Purposes Only — Not Clinically Validated
            </p>
        </div>
    """, unsafe_allow_html=True)


def start_emergency(description, image=None):
    """Initialize emergency session"""
    st.session_state.emergency_active = True
    st.session_state.start_time = datetime.now()
    st.session_state.current_step = 0
    st.session_state.steps_completed = []
    st.session_state.emergency_data = {
        'description': description,
        'has_image': image is not None
    }
    st.session_state.user_actions = []
    st.session_state.show_summary = False
    
    # Classify emergency
    severity, emergency_type, reasoning = EmergencyClassifier.classify_emergency(
        description,
        EmergencyClassifier.analyze_image_for_injuries(image) if image else None
    )
    
    st.session_state.severity_level = severity
    st.session_state.emergency_type = emergency_type
    st.session_state.classification_reasoning = reasoning
    
    st.rerun()

def show_emergency_interface():
    """Show active emergency guidance interface"""
    
    # Header with timer
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("🏠 New Emergency", use_container_width=True):
            reset_emergency()
            st.rerun()
    
    with col2:
        display_timer()
    
    with col3:
        if st.button("📋 View Summary", use_container_width=True):
            st.session_state.show_summary = not st.session_state.show_summary
    
    # Show summary if requested
    if st.session_state.show_summary:
        show_emergency_summary_interface()
        return
    
    # Display severity alert
    display_severity_alert(
        st.session_state.severity_level,
        st.session_state.emergency_type
    )
    
    # EXPLAINABILITY BOX - Shows reasoning transparently
    if st.session_state.classification_reasoning:
        st.markdown("""
            <div class="info-card">
                <strong>🔍 Why LifeLine AI Chose This Severity Level:</strong><br><br>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"""
                <div class="large-text">
                <strong>Classification Reasoning:</strong><br>
                {st.session_state.classification_reasoning}
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Show what was detected
            emergency_display = st.session_state.emergency_type.replace('_', ' ').title()
            severity_display = st.session_state.severity_level.upper()
            
            st.markdown(f"""
                <div class="large-text">
                <strong>Detection Details:</strong><br>
                • Emergency Type: {emergency_display}<br>
                • Severity: {severity_display}<br>
                • Method: Keyword matching + safety rules<br>
                • Approach: Conservative (when unclear, escalate)
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Emergency call reminder
    if st.session_state.severity_level == 'critical':
        st.markdown("""
            <div class="warning-banner" style="background: #ff0000; font-size: 24px;">
                📞 CALL 911 IMMEDIATELY - Put phone on speaker and follow these steps while help is on the way
            </div>
        """, unsafe_allow_html=True)
    
    # Get guidance steps
    guidance_steps = EmergencyGuidance.get_guidance_steps(st.session_state.emergency_type)
    
    # Progress indicator
    total_steps = len(guidance_steps)
    current_step = st.session_state.current_step
    
    st.markdown(f"""
        <div class="info-card">
            <strong>Progress:</strong> Step {min(current_step + 1, total_steps)} of {total_steps}
            <br>Completed: {len(st.session_state.steps_completed)} / {total_steps} steps
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display current step
    if current_step < total_steps:
        display_guidance_step(guidance_steps[current_step], current_step + 1)
    else:
        # All steps completed
        st.markdown("""
            <div class="monitor-alert">
                ✅ All guidance steps completed!<br>
                Continue monitoring until help arrives.
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 What to do next:")
        st.markdown("""
            <div class="info-card large-text">
            • Stay with the person<br>
            • Continue monitoring their condition<br>
            • Be ready to restart CPR if needed<br>
            • Provide the emergency summary to paramedics<br>
            • Note any changes in condition<br>
            </div>
        """, unsafe_allow_html=True)
    
    # Navigation buttons
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if current_step > 0:
            if st.button("⬅️ Previous Step", use_container_width=True):
                st.session_state.current_step -= 1
                st.rerun()
    
    with col2:
        if current_step < total_steps:
            if st.button("✅ Mark Complete & Next", use_container_width=True, type="primary"):
                step_title = guidance_steps[current_step]['title']
                if step_title not in st.session_state.steps_completed:
                    st.session_state.steps_completed.append(step_title)
                st.session_state.current_step += 1
                st.rerun()
    
    with col3:
        if st.button("🔄 Repeat Instructions", use_container_width=True):
            st.rerun()

def display_guidance_step(step, step_number):
    """Display a single guidance step with details"""
    
    # Step card
    st.markdown(f"""
        <div class="step-card">
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                <span class="step-number">{step_number}</span>
                <h2 style="color: #1a1a2e; margin: 0;">{step['title']}</h2>
            </div>
            
            <div style="font-size: 20px; color: #1a1a2e; margin-bottom: 20px; line-height: 1.6;">
                <strong>What to do:</strong><br>
                {step['instruction']}
            </div>
    """, unsafe_allow_html=True)
    
    # Warning if present
    if step.get('warning'):
        st.markdown(f"""
            <div style="background: #ff6b6b; color: white; padding: 15px; border-radius: 10px; margin: 15px 0;">
                ⚠️ <strong>WARNING:</strong> {step['warning']}
            </div>
        """, unsafe_allow_html=True)
    
    # Details
    if step.get('details'):
        st.markdown("""
            <div style="background: rgba(0,255,136,0.1); padding: 15px; border-radius: 10px; margin: 15px 0;">
                <strong style="color: #1a1a2e;">Important Details:</strong>
                <ul style="color: #1a1a2e; font-size: 18px; margin-top: 10px;">
        """, unsafe_allow_html=True)
        
        for detail in step['details']:
            st.markdown(f"<li>{detail}</li>", unsafe_allow_html=True)
        
        st.markdown("</ul></div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Text-to-speech button
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button(f"🔊 Read Step {step_number} Aloud", use_container_width=True):
            text_to_speech_placeholder(step['instruction'])
    
    with col2:
        # Log action button
        action_text = st.text_input(
            "Log what you did:",
            key=f"action_{step_number}",
            placeholder=f"E.g., 'Started chest compressions'"
        )
        if action_text and st.button("💾 Log Action", use_container_width=True):
            st.session_state.user_actions.append(f"Step {step_number}: {action_text}")
            st.success("Action logged!")

def show_emergency_summary_interface():
    """Show emergency summary and reporting interface"""
    
    st.markdown("## 📋 Emergency Incident Summary")
    
    summary = generate_emergency_summary()
    
    # Display summary
    st.markdown(f"""
        <div class="summary-box">
            <pre style="white-space: pre-wrap; margin: 0; font-size: 14px;">{summary}</pre>
        </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔊 Read Summary Aloud", use_container_width=True):
            text_to_speech_placeholder(summary)
    
    with col2:
        # Download summary button
        st.download_button(
            label="📥 Download Summary",
            data=summary,
            file_name=f"emergency_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col3:
        if st.button("✉️ Share with Responders (Simulated)", use_container_width=True):
            st.success("✅ Summary prepared for emergency responders!")
            st.info("In production: This would securely transmit to emergency services")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Additional notes
    st.markdown("### 📝 Add Additional Notes")
    additional_notes = st.text_area(
        "Any additional information for responders:",
        height=100,
        placeholder="E.g., 'Person has diabetes', 'Allergic to penicillin', etc."
    )
    
    if additional_notes:
        st.session_state.emergency_data['additional_notes'] = additional_notes
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Back button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("⬅️ Back to Guidance", use_container_width=True, type="primary"):
            st.session_state.show_summary = False
            st.rerun()

def reset_emergency():
    """Reset emergency session"""
    st.session_state.emergency_active = False
    st.session_state.start_time = None
    st.session_state.current_step = 0
    st.session_state.steps_completed = []
    st.session_state.emergency_data = {}
    st.session_state.severity_level = None
    st.session_state.emergency_type = None
    st.session_state.user_actions = []
    st.session_state.show_summary = False

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
