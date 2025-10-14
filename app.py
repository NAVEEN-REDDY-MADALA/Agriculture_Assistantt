import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import requests
import json
from datetime import datetime, timedelta
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import qrcode
import io
import base64


# Page config
st.set_page_config(page_title="🌾 Advanced Smart Agriculture Assistant", page_icon="🌾", layout="wide")


# Your working class names (keestrea,lit ping the same order)
class_names = [
    'Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 'PlantVillage',
    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
    'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight',
    'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus',
    'Tomato_healthy'
]

# Enhanced class mapping
CLASS_MAPPING = {
    'PlantVillage': 'Unknown_Plant_Sample',
    'Pepper__bell___Bacterial_spot': 'Pepper_Bacterial_Spot',
    'Pepper__bell___healthy': 'Pepper_Healthy',
    'Potato___Early_blight': 'Potato_Early_Blight',
    'Potato___Late_blight': 'Potato_Late_Blight',
    'Potato___healthy': 'Potato_Healthy',
    'Tomato_Bacterial_spot': 'Tomato_Bacterial_Spot',
    'Tomato_Early_blight': 'Tomato_Early_Blight',
    'Tomato_Late_blight': 'Tomato_Late_Blight',
    'Tomato_Leaf_Mold': 'Tomato_Leaf_Mold',
    'Tomato_Septoria_leaf_spot': 'Tomato_Septoria_Leaf_Spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite': 'Tomato_Spider_Mites',
    'Tomato__Target_Spot': 'Tomato_Target_Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus': 'Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato__Tomato_mosaic_virus': 'Tomato_Mosaic_Virus',
    'Tomato_healthy': 'Tomato_Healthy'
}

# COMPREHENSIVE TRANSLATIONS - EVERYTHING IN BOTH LANGUAGES
TRANSLATIONS = {
    'en': {
        'title': '🌾 Advanced Smart Agriculture Assistant',
        'subtitle': 'AI-Powered Complete Farming Solution',
        'disease_detection': '🔍 Disease Detection',
        'crop_advisor': '🌱 Crop Advisor',
        'market_insights': '📊 Market Insights',
        'insurance_helper': '🛡️ Insurance Helper',
        'weather_station': '🌤️ Weather Station',
        'dashboard': '📈 Farmer Dashboard',
        'upload_image': '📷 Upload Plant Image',
        'analyze_plant': '🔍 Analyze Plant',
        'analysis_results': '🎯 Analysis Results',
        'ai_confidence': 'AI Confidence',
        'healthy': 'Healthy Plant',
        'disease_detected': 'Disease Detected',
        'description': 'Description',
        'cause': 'Cause of Disease',
        'organic_treatment': '🌿 Organic Treatment',
        'chemical_treatment': '🧪 Chemical Treatment',
        'estimated_cost': 'Estimated Cost',
        'whatsapp_share': 'Share via WhatsApp',
        'farm_details': 'Farm Details',
        'farm_area': 'Farm area (hectares)',
        'crop_value': 'Crop value per hectare (₹)',
        'treatment_info': 'Treatment Info',
        'economic_impact': 'Economic Impact',
        'spread_risk': 'Spread Risk',
        'treatment_plan': 'Treatment Plan',
        'share_results': 'Share Results via WhatsApp',
        'click_to_share': 'Click to Share on WhatsApp',
        'copy_message': 'Copy Message',
        'scan_qr': 'Scan QR code to share',
        'model_support': 'AI Model Support',
        'ai_analysis_details': 'AI Analysis Details',
        'top_predictions': 'Top 3 Predictions',
        'disease_information': 'Disease Information',
        'economic_impact_analysis': 'Economic Impact Analysis',
        'disease_spread_risk': 'Disease Spread Risk Assessment',
        'treatment_schedule': 'Treatment Schedule',
        'early_detection': 'Early Detection',
        'medium_delay': 'Medium Delay',
        'severe_impact': 'Severe Impact',
        'best_outcome': 'Best outcome',
        'loss_50': '50% loss',
        'critical_loss': 'Critical loss',
        'total_crop_value': 'Total Crop Value',
        'urgent_action': 'URGENT ACTION REQUIRED',
        'monitor_closely': 'MONITOR CLOSELY',
        'low_risk': 'LOW RISK',
        'navigation': 'Navigation',
        'location': 'Location',
        'soil_type': 'Soil Type',
        'season': 'Season',
        'get_recommendations': 'Get Recommendations',
        'recommended_crops': 'Recommended Crops',
        'success_rate': 'Success Rate',
        'profit_potential': 'Profit Potential',
        'water_requirement': 'Water Requirement',
        'current_market_prices': 'Current market prices and trends for agricultural products',
        'price_trends': 'Price Trends',
        'crop_insurance_assistance': 'Assistance with crop insurance claims and eligibility',
        'damage_percentage': 'Damage Percentage',
        'area_affected': 'Area Affected (hectares)',
        'crop_type': 'Crop Type',
        'eligible_claim': 'ELIGIBLE for insurance claim!',
        'not_eligible': 'NOT ELIGIBLE - Damage below minimum threshold (33%)',
        'estimated_compensation': 'Estimated Compensation',
        'required_documents': 'Required Documents',
        'weather_conditions': 'Current weather conditions and agricultural alerts',
        'get_weather': 'Get Weather Data',
        'temperature': 'Temperature',
        'humidity': 'Humidity',
        'wind_speed': 'Wind Speed',
        'rain_24h': 'Rain (24h)',
        'disease_risk_level': 'Disease Risk Level',
        'agricultural_alerts': 'Agricultural Alerts',
        'total_analyses': 'Total Analyses',
        'diseases_detected': 'Diseases Detected',
        'avg_confidence': 'Avg Confidence',
        'this_week': 'This Week',
        'disease_distribution': 'Disease Distribution',
        'analysis_timeline': 'Analysis Timeline',
        'recent_history': 'Recent Analysis History',
        'no_history': 'No analysis history yet. Start by analyzing some plants!'
    },
    'te': {
        'title': '🌾 అధునాతన స్మార్ట్ వ్యవసాయ సహాయకుడు',
        'subtitle': 'AI-శక్తితో పూర్తి వ్యవసాయ పరిష్కారం',
        'disease_detection': '🔍 వ్యాధి గుర్తింపు',
        'crop_advisor': '🌱 పంట సలహాదారు',
        'market_insights': '📊 మార్కెట్ సమాచారం',
        'insurance_helper': '🛡️ బీమా సహాయకుడు',
        'weather_station': '🌤️ వాతావరణ కేంద్రం',
        'dashboard': '📈 రైతు డ్యాష్‌బోర్డ్',
        'upload_image': '📷 మొక్క చిత్రం అప్‌లోడ్ చేయండి',
        'analyze_plant': '🔍 మొక్కను విశ్లేషించండి',
        'analysis_results': '🎯 విశ్లేషణ ఫలితాలు',
        'ai_confidence': 'AI విశ్వసనీయత',
        'healthy': 'ఆరోగ్యకరమైన మొక్క',
        'disease_detected': 'వ్యాధి కనుగొనబడింది',
        'description': 'వర్ణన',
        'cause': 'వ్యాధికి కారణం',
        'organic_treatment': '🌿 సేంద్రీయ చికిత్స',
        'chemical_treatment': '🧪 రసాయన చికిత్స',
        'estimated_cost': 'అంచనా ఖర్చు',
        'whatsapp_share': 'వాట్సాప్ ద్వారా పంచుకోండి',
        'farm_details': 'వ్యవసాయ వివరాలు',
        'farm_area': 'వ్యవసాయ భూమి (హెక్టార్లు)',
        'crop_value': 'హెక్టార్‌కు పంట విలువ (₹)',
        'treatment_info': 'చికిత్స సమాచారం',
        'economic_impact': 'ఆర్థిక ప్రభావం',
        'spread_risk': 'వ్యాప్తి ప్రమాదం',
        'treatment_plan': 'చికిత్స ప్రణాళిక',
        'share_results': 'వాట్సాప్ ద్వారా ఫలితాలు పంచుకోండి',
        'click_to_share': 'వాట్సాప్‌లో పంచుకోవడానికి క్లిక్ చేయండి',
        'copy_message': 'సందేశం కాపీ చేయండి',
        'scan_qr': 'పంచుకోవడానికి QR కోడ్ స్కాన్ చేయండి',
        'model_support': 'AI మోడల్ మద్దతు',
        'ai_analysis_details': 'AI విశ్లేషణ వివరాలు',
        'top_predictions': 'టాప్ 3 అంచనాలు',
        'disease_information': 'వ్యాధి సమాచారం',
        'economic_impact_analysis': 'ఆర్థిక ప్రభావ విశ్లేషణ',
        'disease_spread_risk': 'వ్యాధి వ్యాప్తి ప్రమాద అంచనా',
        'treatment_schedule': 'చికిత్స కార్యక్రమం',
        'early_detection': 'ముందస్తు గుర్తింపు',
        'medium_delay': 'మధ్యస్థ ఆలస్యం',
        'severe_impact': 'తీవ్ర ప్రభావం',
        'best_outcome': 'మంచి ఫలితం',
        'loss_50': '50% నష్టం',
        'critical_loss': 'క్లిష్ట నష్టం',
        'total_crop_value': 'మొత్తం పంట విలువ',
        'urgent_action': 'తక్షణ చర్య అవసరం',
        'monitor_closely': 'దగ్గరగా పర్యవేక్షించండి',
        'low_risk': 'తక్కువ ప్రమాదం',
        'navigation': 'నేవిగేషన్',
        'location': 'ప్రాంతం',
        'soil_type': 'మట్టి రకం',
        'season': 'కాలం',
        'get_recommendations': 'సిఫార్సులు పొందండి',
        'recommended_crops': 'సిఫార్సు చేసిన పంటలు',
        'success_rate': 'విజయ రేటు',
        'profit_potential': 'లాభ అవకాశం',
        'water_requirement': 'నీటి అవసరం',
        'current_market_prices': 'వ్యవసాయ ఉత్పత్తుల ప్రస్తుత మార్కెట్ ధరలు మరియు ట్రెండ్‌లు',
        'price_trends': 'ధర ట్రెండ్‌లు',
        'crop_insurance_assistance': 'పంట బీమా క్లెయిమ్‌లు మరియు అర్హతలో సహాయం',
        'damage_percentage': 'నష్ట శాతం',
        'area_affected': 'ప్రభావిత ప్రాంతం (హెక్టార్లు)',
        'crop_type': 'పంట రకం',
        'eligible_claim': 'బీమా క్లెయిమ్‌కు అర్హులు!',
        'not_eligible': 'అర్హులు కాదు - కనిష్ట హద్దు కంటే తక్కువ నష్టం (33%)',
        'estimated_compensation': 'అంచనా పరిహారం',
        'required_documents': 'అవసరమైన పత్రాలు',
        'weather_conditions': 'ప్రస్తుత వాతావరణ పరిస్థితులు మరియు వ్యవసాయ హెచ్చరికలు',
        'get_weather': 'వాతావరణ డేటా పొందండి',
        'temperature': 'ఉష్ణోగ్రత',
        'humidity': 'తేమ',
        'wind_speed': 'గాలి వేగం',
        'rain_24h': 'వర్షం (24 గంటలు)',
        'disease_risk_level': 'వ్యాధి ప్రమాద స్థాయి',
        'agricultural_alerts': 'వ్యవసాయ హెచ్చరికలు',
        'total_analyses': 'మొత్తం విశ్లేషణలు',
        'diseases_detected': 'గుర్తించిన వ్యాధులు',
        'avg_confidence': 'సగటు విశ్వసనీయత',
        'this_week': 'ఈ వారం',
        'disease_distribution': 'వ్యాధి పంపిణీ',
        'analysis_timeline': 'విశ్లేషణ టైంలైన్',
        'recent_history': 'ఇటీవలి విశ్లేషణ చరిత్ర',
        'no_history': 'ఇంకా విశ్లేషణ చరిత్ర లేదు. కొన్ని మొక్కలను విశ్లేషించడం ప్రారంభించండి!'
    }
}

# COMPREHENSIVE TREATMENT DATABASE WITH BOTH LANGUAGES
TREATMENT_DATABASE = {
    'Pepper_Bacterial_Spot': {
        'en': {
            'disease_name': 'Bell Pepper Bacterial Spot',
            'description': 'Dark brown spots with yellow halos on pepper leaves. Caused by Xanthomonas bacteria.',
            'cause': 'Xanthomonas campestris bacteria. Spreads through water splash, contaminated tools.',
            'organic_treatment': [
                'Apply copper-based organic spray (2-3 times weekly)',
                'Remove and destroy infected leaves immediately',
                'Use neem oil spray in evening hours',
                'Improve air circulation around plants',
                'Avoid overhead watering - water at soil level'
            ],
            'chemical_treatment': [
                'Copper sulfate spray (0.3%)',
                'Streptomycin sulfate (200 ppm)',
                'Copper hydroxide fungicide',
                'Alternating copper and streptomycin treatments'
            ],
            'cost_estimate': '₹150-300 per acre'
        },
        'te': {
            'disease_name': '[translate:మిరపకాయ బ్యాక్టీరియల్ స్పాట్]',
            'description': '[translate:మిరపకాయ ఆకులపై పసుపు వలయాలతో ముదురు గోధుమ రంగు చుక్కలు.]',
            'cause': '[translate:జాంథోమోనాస్ కాంపెస్ట్రిస్ బ్యాక్టీరియా.]',
            'organic_treatment': [
                '[translate:రాగి ఆధారిత సేంద్రీయ స్ప్రే వాడండి (వారానికి 2-3 సార్లు)]',
                '[translate:వ్యాధిగ్రస్తమైన ఆకులను వెంటనే తొలగించండి]',
                '[translate:సాయంకాలం వేప నూనె స్ప్రే చేయండి]',
                '[translate:మొక్కల మధ్య గాలి ప్రసారం మెరుగుపరచండి]'
            ],
            'chemical_treatment': [
                '[translate:కాపర్ సల్ఫేట్ స్ప్రే (0.3%)]',
                '[translate:స్ట్రెప్టోమైసిన్ సల్ఫేట్ (200 పీపీఎం)]',
                '[translate:కాపర్ హైడ్రాక్సైడ్ శిలీంద్రనాశిని]'
            ],
            'cost_estimate': '₹150-300 [translate:ఎకరానికి]'
        }
    },
    'Tomato_Yellow_Leaf_Curl_Virus': {
        'en': {
            'disease_name': 'Tomato Yellow Leaf Curl Virus (TYLCV)',
            'description': 'Viral disease causing yellowing, curling, and stunting of tomato plants. Transmitted by whiteflies.',
            'cause': 'TYLCV virus transmitted by Bemisia tabaci whiteflies.',
            'organic_treatment': [
                'Remove infected plants immediately',
                'Control whiteflies using sticky traps',
                'Use reflective mulch to repel whiteflies',
                'Plant virus-resistant varieties',
                'Spray neem oil to control vectors'
            ],
            'chemical_treatment': [
                'Imidacloprid for whitefly control (0.5ml/liter)',
                'Thiamethoxam spray (0.4g/liter)',
                'Acetamiprid 20% SP (0.4g/liter)',
                'Use systemic insecticides for whiteflies',
                'No direct cure - focus on vector control'
            ],
            'cost_estimate': '₹400-700 per acre'
        },
        'te': {
            'disease_name': '[translate:టమాటో పసుపు ఆకు కర్లింగ్ వైరస్ (TYLCV)]',
            'description': '[translate:టమాటో మొక్కలను పసుపు చేసి, కర్లింగ్ చేసి, మరుగుజ్జు చేసే వైరల్ వ్యాధి.]',
            'cause': '[translate:తెల్ల ఈగల ద్వారా వ్యాపించే TYLCV వైరస్.]',
            'organic_treatment': [
                '[translate:వ్యాధిగ్రస్తమైన మొక్కలను వెంటనే తొలగించండి]',
                '[translate:జిగురు ట్రాప్‌లు వాడి తెల్ల ఈగలను నియంత్రించండి]',
                '[translate:తెల్ల ఈగలను తరిమికొట్టడానికి రిఫ్లెక్టివ్ మల్చ్ వాడండి]',
                '[translate:వైరస్ నిరోధక రకాలను నాటండి]'
            ],
            'chemical_treatment': [
                '[translate:తెల్ల ఈగ నియంత్రణకు ఇమిడాక్లోప్రిడ్ (0.5ml/లీటర్)]',
                '[translate:థియామెథోక్సామ్ స్ప్రే (0.4g/లీటర్)]',
                '[translate:అసెటామిప్రిడ్ 20% SP (0.4g/లీటర్)]',
                '[translate:తెల్ల ఈగలకు వ్యవస్థాగత కీటకనాశినులు వాడండి]',
                '[translate:ప్రత్యక్ష చికిత్స లేదు - వెక్టర్ నియంత్రణపై దృష్టి పెట్టండి]'
            ],
            'cost_estimate': '₹400-700 [translate:ఎకరానికి]'
        }
    },
    'Tomato_Late_Blight': {
        'en': {
            'disease_name': 'Tomato Late Blight',
            'description': 'Water-soaked lesions with white mold growth. Highly destructive fungal disease.',
            'cause': 'Phytophthora infestans fungus. Favored by cool, moist conditions.',
            'organic_treatment': [
                'Remove infected plants immediately',
                'Apply Bordeaux mixture (1%)',
                'Use resistant varieties when replanting',
                'Improve air circulation',
                'Avoid overhead irrigation'
            ],
            'chemical_treatment': [
                'Metalaxyl + Mancozeb spray (2.5g/liter)',
                'Dimethomorph 50% WP (1g/liter)',
                'Propamocarb hydrochloride (2ml/liter)',
                'Copper oxychloride (3g/liter)',
                'Alternating different fungicides'
            ],
            'cost_estimate': '₹300-600 per acre'
        },
        'te': {
            'disease_name': '[translate:టమాటో ఆలస్య వ్యాధి]',
            'description': '[translate:తెల్లని కుట్టిన పెరుగుదలతో నీటిలో నిండిన గాయాలు. అత్యంత విధ్వంసక శిలీంద్ర వ్యాధి.]',
            'cause': '[translate:ఫైటోఫ్తోరా ఇన్ఫెస్టాన్స్ శిలీంద్రం.]',
            'organic_treatment': [
                '[translate:వ్యాధిగ్రస్తమైన మొక్కలను వెంటనే తొలగించండి]',
                '[translate:బోర్డియక్స్ మిశ్రమం వేయండి (1%)]',
                '[translate:మళ్లీ నాటేటప్పుడు నిరోధక రకాలను వాడండి]',
                '[translate:గాలి ప్రసారణ మెరుగుపరచండి]'
            ],
            'chemical_treatment': [
                '[translate:మెటలాక్సిల్ + మాంకోజెబ్ స్ప్రే (2.5g/లీటర్)]',
                '[translate:డైమెథోమార్ఫ్ 50% WP (1g/లీటర్)]',
                '[translate:ప్రోపామోకార్బ్ హైడ్రోక్లోరైడ్ (2ml/లీటర్)]',
                '[translate:కాపర్ ఆక్సిక్లోరైడ్ (3g/లీటర్)]',
                '[translate:వేర్వేరు శిలీంద్రనాశినులను ప్రత్యామ్నాయంగా వాడండి]'
            ],
            'cost_estimate': '₹300-600 [translate:ఎకరానికి]'
        }
    },
    'Unknown_Plant_Sample': {
        'en': {
            'disease_name': 'Plant Image Analysis - Unclear Result',
            'description': 'The image is not clear enough for specific disease identification.',
            'cause': 'Poor image quality or plant/disease not in training database.',
            'organic_treatment': [
                'Take a clearer photo with better lighting',
                'Capture diseased parts up close',
                'Ensure leaf is fully visible in frame',
                'Remove any background distractions'
            ],
            'chemical_treatment': [
                'Cannot recommend without clear identification',
                'Consult local agriculture expert',
                'Contact nearest Krishi Vigyan Kendra'
            ],
            'cost_estimate': 'Depends on actual disease identified'
        },
        'te': {
            'disease_name': '[translate:మొక్క చిత్ర విశ్లేషణ - అస్పష్ట ఫలితం]',
            'description': '[translate:నిర్దిష్ట వ్యాధి గుర్తింపుకు చిత్రం తగినంత స్పష్టంగా లేదు.]',
            'cause': '[translate:చిత్ర నాణ్యత లేదా మొక్క/వ్యాధి శిక్షణ డేటాబేస్‌లో లేదు.]',
            'organic_treatment': [
                '[translate:మెరుగైన వెలుతురుతో స్పష్టమైన ఫోటో తీయండి]',
                '[translate:వ్యాధిగ్రస్తమైన భాగాలను దగ్గరగా తీయండి]',
                '[translate:ఆకు పూర్తిగా ఫ్రేంలో కనిపించేలా చూడండి]'
            ],
            'chemical_treatment': [
                '[translate:స్పష్టమైన గుర్తింపు లేకుండా సిఫార్సు చేయలేము]',
                '[translate:స్థానిక వ్యవసాయ నిపుణుడిని సంప్రదించండి]',
                '[translate:సమీప కృషి విజ్ఞాన కేంద్రాన్ని సంప్రదించండి]'
            ],
            'cost_estimate': '[translate:వాస్తవ వ్యాధి గుర్తింపుపై ఆధారపడుతుంది]'
        }
    }
}


# Database setup (keeping your working functions)
def init_database():
    conn = sqlite3.connect('agriculture_assistant.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS farmer_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  disease TEXT,
                  confidence REAL,
                  treatment_given TEXT,
                  location TEXT)''')
    conn.commit()
    conn.close()


def save_analysis(disease, confidence, treatment, location="Unknown"):
    try:
        conn = sqlite3.connect('agriculture_assistant.db')
        c = conn.cursor()
        c.execute(
            "INSERT INTO farmer_history (timestamp, disease, confidence, treatment_given, location) VALUES (?, ?, ?, ?, ?)",
            (datetime.now().isoformat(), disease, float(confidence), treatment, location))
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Database error: {e}")


def get_farmer_history():
    try:
        conn = sqlite3.connect('agriculture_assistant.db')
        df = pd.read_sql_query("SELECT * FROM farmer_history ORDER BY timestamp DESC", conn)
        conn.close()
        if 'confidence' in df.columns and len(df) > 0:
            df['confidence'] = pd.to_numeric(df['confidence'], errors='coerce')
        return df
    except Exception as e:
        return pd.DataFrame()


# ENHANCED WHATSAPP MESSAGE WITH BOTH ORGANIC AND CHEMICAL TREATMENTS
def generate_whatsapp_message(disease, confidence, treatment_info, lang_code='en'):
    if lang_code == 'te':
        message = f"""🌾 వ్యవసాయ AI విశ్లేషణ నివేదిక

🔍 వ్యాధి: {disease.replace('_', ' ')}
📊 AI విశ్వసనీయత: {confidence:.1%}

🌿 సేంద్రీయ చికిత్స:"""
        organic_treatments = treatment_info.get('organic_treatment', [])
        for i, treatment in enumerate(organic_treatments[:3], 1):
            clean_treatment = treatment.replace('[translate:', '').replace(']', '')
            message += f"\n{i}. {clean_treatment}"

        message += f"""\n\n🧪 రసాయన చికిత్స:"""
        chemical_treatments = treatment_info.get('chemical_treatment', [])
        for i, treatment in enumerate(chemical_treatments[:3], 1):
            clean_treatment = treatment.replace('[translate:', '').replace(']', '')
            message += f"\n{i}. {clean_treatment}"

        message += f"""\n\n💰 అంచనా ఖర్చు: {treatment_info.get('cost_estimate', 'N/A')}

🌾 స్మార్ట్ వ్యవసాయ AI అసిస్టెంట్ ద్వారా"""
    else:
        message = f"""🌾 Smart Agriculture AI Analysis Report

🔍 Disease Detected: {disease.replace('_', ' ')}
📊 AI Confidence: {confidence:.1%}

🌿 Organic Treatment:"""
        organic_treatments = treatment_info.get('organic_treatment', [])
        for i, treatment in enumerate(organic_treatments[:3], 1):
            message += f"\n{i}. {treatment}"

        message += f"""\n\n🧪 Chemical Treatment:"""
        chemical_treatments = treatment_info.get('chemical_treatment', [])
        for i, treatment in enumerate(chemical_treatments[:3], 1):
            message += f"\n{i}. {treatment}"

        message += f"""\n\n💰 Estimated Cost: {treatment_info.get('cost_estimate', 'N/A')}

🌾 Powered by Smart Agriculture AI Assistant"""

    return message


def create_whatsapp_qr_code(message):
    try:
        encoded_message = requests.utils.quote(message)
        whatsapp_url = f"https://wa.me/?text={encoded_message}"

        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(whatsapp_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        return base64.b64encode(buffer.getvalue()).decode(), whatsapp_url
    except Exception as e:
        st.error(f"QR Code error: {e}")
        return None, None


# ENHANCED WEATHER API (keeping your working version)
def get_weather_alerts(location="Hyderabad"):
    try:
        api_key = "705266c0789cd984eb29503280b12c1e"
        current_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        current_response = requests.get(current_url, timeout=10)
        current_data = current_response.json()

        if current_response.status_code != 200:
            raise Exception(f"API Error: {current_data.get('message', 'Unknown error')}")

        temp = current_data['main']['temp']
        humidity = current_data['main']['humidity']
        description = current_data['weather'][0]['description']
        wind_speed = current_data['wind']['speed']
        pressure = current_data['main']['pressure']
        feels_like = current_data['main']['feels_like']

        alerts = []
        disease_risk = "Low"

        if humidity > 75:
            alerts.append("⚠️ High humidity detected! Increased risk of fungal diseases.")
            alerts.append("🛡️ Recommendation: Apply preventive fungicide spray within 24 hours.")
            disease_risk = "High"

        if temp > 35:
            alerts.append("🌡️ High temperature alert! Plants may experience heat stress.")
            alerts.append("💧 Recommendation: Increase watering frequency and provide shade.")
        elif temp < 10:
            alerts.append("❄️ Cold temperature alert! Risk of frost damage.")
            alerts.append("🛡️ Recommendation: Cover sensitive plants overnight.")

        return {
            'temperature': temp,
            'humidity': humidity,
            'description': description.title(),
            'wind_speed': wind_speed,
            'pressure': pressure,
            'feels_like': feels_like,
            'alerts': alerts,
            'disease_risk': disease_risk,
            'rain_forecast': 0,
            'location': current_data['name'],
            'country': current_data['sys']['country']
        }

    except Exception as e:
        return {
            'temperature': 28, 'humidity': 70, 'description': 'Partly cloudy',
            'wind_speed': 5, 'alerts': ["Weather service temporarily unavailable"],
            'disease_risk': "Medium", 'rain_forecast': 0, 'location': location
        }


# ECONOMIC IMPACT CALCULATOR (keeping your working version)
def calculate_economic_impact(disease, area_hectares, crop_value_per_hectare):
    loss_percentages = {
        'Tomato_Late_Blight': {'early': 20, 'medium': 50, 'severe': 90},
        'Potato_Late_Blight': {'early': 30, 'medium': 60, 'severe': 95},
        'Tomato_Yellow_Leaf_Curl_Virus': {'early': 25, 'medium': 60, 'severe': 95},
        'Tomato_Early_Blight': {'early': 10, 'medium': 25, 'severe': 40},
        'Pepper_Bacterial_Spot': {'early': 15, 'medium': 35, 'severe': 60}
    }

    if disease not in loss_percentages:
        loss_percentages[disease] = {'early': 10, 'medium': 30, 'severe': 60}

    losses = loss_percentages[disease]
    total_value = area_hectares * crop_value_per_hectare

    return {
        'early': (total_value * losses['early']) / 100,
        'medium': (total_value * losses['medium']) / 100,
        'severe': (total_value * losses['severe']) / 100,
        'total_crop_value': total_value
    }


# CROP RECOMMENDATIONS (keeping your working version)
def get_crop_recommendations(location, season, soil_type):
    recommendations = {
        'clay': {
            'summer': [
                {'crop': 'Rice', 'success_rate': 85, 'profit_potential': 'High', 'water_req': 'High'},
                {'crop': 'Cotton', 'success_rate': 80, 'profit_potential': 'Medium', 'water_req': 'Medium'}
            ],
            'winter': [
                {'crop': 'Wheat', 'success_rate': 90, 'profit_potential': 'Medium', 'water_req': 'Low'},
                {'crop': 'Mustard', 'success_rate': 85, 'profit_potential': 'Medium', 'water_req': 'Low'}
            ]
        },
        'sandy': {
            'summer': [
                {'crop': 'Millet', 'success_rate': 85, 'profit_potential': 'Medium', 'water_req': 'Low'},
                {'crop': 'Groundnut', 'success_rate': 80, 'profit_potential': 'High', 'water_req': 'Low'}
            ],
            'winter': [
                {'crop': 'Gram', 'success_rate': 85, 'profit_potential': 'High', 'water_req': 'Low'},
                {'crop': 'Mustard', 'success_rate': 80, 'profit_potential': 'Medium', 'water_req': 'Low'}
            ]
        },
        'loamy': {
            'summer': [
                {'crop': 'Tomato', 'success_rate': 90, 'profit_potential': 'High', 'water_req': 'Medium'},
                {'crop': 'Potato', 'success_rate': 85, 'profit_potential': 'Medium', 'water_req': 'Medium'}
            ],
            'winter': [
                {'crop': 'Potato', 'success_rate': 95, 'profit_potential': 'Medium', 'water_req': 'Medium'},
                {'crop': 'Tomato', 'success_rate': 90, 'profit_potential': 'High', 'water_req': 'Medium'}
            ]
        }
    }

    return recommendations.get(soil_type, {}).get(season, [
        {'crop': 'Consult local expert', 'success_rate': 50, 'profit_potential': 'Unknown', 'water_req': 'Medium'}
    ])


# MODEL LOADING AND PREDICTION (keeping your working functions)
@st.cache_resource
def load_model():
    try:
        model = tf.keras.models.load_model('best_model_phase1.h5')
        st.success(f"✅ Model loaded successfully! Input shape: {model.input_shape}")
        return model
    except Exception as e:
        st.error(f"❌ Model loading failed: {e}")
        return None


def preprocess_image(image):
    try:
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image = image.resize((224, 224))
        image_array = np.array(image, dtype=np.float32)
        image_array = image_array / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        return image_array
    except Exception as e:
        st.error(f"Image preprocessing error: {e}")
        return None


def predict_disease(model, image):
    try:
        processed_image = preprocess_image(image)
        if processed_image is None:
            return "Unknown_Plant_Sample", 0.3

        predictions = model.predict(processed_image, verbose=0)
        prediction_scores = predictions[0]

        # Get top 3 predictions for debugging
        top_3_indices = np.argsort(prediction_scores)[-3:][::-1]

        # Store debug info
        st.session_state.debug_predictions = []
        for i, idx in enumerate(top_3_indices):
            class_name = class_names[idx]
            mapped_name = CLASS_MAPPING.get(class_name, class_name)
            confidence = prediction_scores[idx]
            st.session_state.debug_predictions.append({
                'rank': i + 1,
                'class': mapped_name,
                'confidence': confidence
            })

        predicted_class = np.argmax(prediction_scores)
        confidence = float(prediction_scores[predicted_class])
        predicted_disease = class_names[predicted_class]

        # Smart correction for PlantVillage
        if predicted_disease == 'PlantVillage':
            alternative_predictions = []
            for i, score in enumerate(prediction_scores):
                if class_names[i] != 'PlantVillage':
                    alternative_predictions.append((i, score, class_names[i]))

            if alternative_predictions:
                alternative_predictions.sort(key=lambda x: x[1], reverse=True)
                best_alternative = alternative_predictions[0]

                if best_alternative[1] > 0.2:
                    predicted_class = best_alternative[0]
                    confidence = best_alternative[1]
                    predicted_disease = best_alternative[2]

        # Apply class mapping
        if predicted_disease in CLASS_MAPPING:
            predicted_disease = CLASS_MAPPING[predicted_disease]

        return predicted_disease, confidence

    except Exception as e:
        st.error(f"Prediction error: {e}")
        return "Unknown_Plant_Sample", 0.3


def get_treatment_info(disease_key, lang_code='en'):
    if disease_key in TREATMENT_DATABASE:
        return TREATMENT_DATABASE[disease_key][lang_code]

    # Fallback treatment info
    if lang_code == 'te':
        return {
            'disease_name': f'వ్యాధి: {disease_key.replace("_", " ")}',
            'description': 'నిర్దిష్ట వివరాలు అందుబాటులో లేవు. మంచి నాణ్యత గల ఫోటో తీసి మళ్లీ ప్రయత్నించండి.',
            'cause': 'కారణం గుర్తించలేకపోతున్నాము.',
            'organic_treatment': [
                'ప్రభావిత ఆకులను వెంటనే తొలగించండి',
                'వేప నూనె స్ప్రే వారానికి 2 సార్లు చేయండి',
                'మొక్కల మధ్య గాలి ప్రసారణ మెరుగుపరచండి'
            ],
            'chemical_treatment': [
                'కాపర్ ఆధారిత ఫంగిసైడ్',
                'నిపుణుడి సలహా మేరకు రసాయనాలు వాడండి',
                'స్థానిక కృషి విజ్ఞాన కేంద్రాన్ని సంప్రదించండి'
            ],
            'cost_estimate': '₹200-500 ఎకరానికి'
        }
    else:
        return {
            'disease_name': f'Disease: {disease_key.replace("_", " ")}',
            'description': 'Specific details not available. Please take a higher quality photo and try again.',
            'cause': 'Cause cannot be determined.',
            'organic_treatment': [
                'Remove affected leaves immediately',
                'Apply neem oil spray twice weekly',
                'Improve air circulation between plants'
            ],
            'chemical_treatment': [
                'Copper-based fungicide',
                'Chemical treatment as per expert advice',
                'Contact nearest Krishi Vigyan Kendra'
            ],
            'cost_estimate': '₹200-500 per acre'
        }


# ENHANCED DISEASE DETECTION PAGE WITH FULL LANGUAGE SUPPORT
def disease_detection_page(t, lang_code):
    st.markdown(f"""
    <div style='text-align: center; background: linear-gradient(135deg, #4CAF50, #45a049); padding: 25px; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
        <h1 style='color: white; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{t['title']}</h1>
        <p style='color: white; margin: 15px 0 0 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>{t['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Model scope information in selected language
    if lang_code == 'te':
        model_info = """
        🌱 **AI మోడల్ మద్దతు:** ఈ AI అసిస్టెంట్ ఈ వ్యాధులను గుర్తిస్తుంది:
        🍅 **టమాటో వ్యాధులు** (9 రకాలు): బ్యాక్టీరియల్ స్పాట్, ముందస్తు వ్యాధి, ఆలస్య వ్యాధి, ఆకు కుట్టిన, సెప్టోరియా, స్పైడర్ మైట్స్, టార్గెట్ స్పాట్, పసుపు ఆకు కర్లింగ్ వైరస్, మొజాయిక్ వైరస్, ఆరోగ్యకరమైన
        🥔 **బంగాళాదుంప వ్యాధులు** (3 రకాలు): ముందస్తు వ్యాధి, ఆలస్య వ్యాధి, ఆరోగ్యకరమైన
        🌶️ **మిరపకాయ వ్యాధులు** (2 రకాలు): బ్యాక్టీరియల్ స్పాట్, ఆరోగ్యకరమైన
        📸 **మంచి ఫలితాలకు:** సహజ వెలుతురులో దగ్గరగా, స్పష్టమైన ఫోటోలు తీయండి
        """
    else:
        model_info = """
        🌱 **AI Model Support:** This AI Assistant can identify diseases in:
        🍅 **Tomato Diseases** (9 types): Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus, Healthy
        🥔 **Potato Diseases** (3 types): Early Blight, Late Blight, Healthy  
        🌶️ **Pepper Diseases** (2 types): Bacterial Spot, Healthy
        📸 **For best results:** Take close, clear photos with natural lighting
        """

    st.info(model_info)

    model = load_model()
    if model is None:
        error_msg = "⚠️ మోడల్ లోడ్ కాలేదు. దయచేసి 'plant_disease_model_improved.h5' ఉందా లేదా చూడండి." if lang_code == 'te' else "⚠️ Model not loaded. Please check if 'plant_disease_model_improved.h5' exists."
        st.error(error_msg)
        return

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(t['upload_image'])
        file_label = "మొక్క చిత్రం ఎంచుకోండి" if lang_code == 'te' else "Choose plant image"
        uploaded_file = st.file_uploader(file_label, type=['jpg', 'jpeg', 'png'], key="plant_uploader")

        # Farm details for economic analysis
        st.subheader(f"🚜 {t['farm_details']}")
        area_hectares = st.number_input(t['farm_area'], 1.0, 1000.0, 5.0)
        crop_value = st.number_input(t['crop_value'], 10000, 500000, 80000)

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            caption = "📷 అప్‌లోడ్ చేసిన చిత్రం" if lang_code == 'te' else "📷 Uploaded Image"
            st.image(image, caption=caption, use_container_width=True)

            spinner_text = "🧠 AI మీ మొక్కను విశ్లేషిస్తోంది..." if lang_code == 'te' else "🧠 AI analyzing your plant..."
            if st.button(t['analyze_plant'], type="primary", use_container_width=True):
                with st.spinner(spinner_text):
                    disease, confidence = predict_disease(model, image)
                    treatment_info = get_treatment_info(disease, lang_code)

                    st.session_state.disease = disease
                    st.session_state.confidence = confidence
                    st.session_state.treatment_info = treatment_info
                    st.session_state.area_hectares = area_hectares
                    st.session_state.crop_value = crop_value
                    st.session_state.image = image
                    st.session_state.lang_code = lang_code

                    save_analysis(disease, confidence, "Analysis completed", "Unknown")

    with col2:
        if 'disease' in st.session_state:
            st.subheader(t['analysis_results'])

            disease = st.session_state.disease
            confidence = st.session_state.confidence
            treatment_info = st.session_state.treatment_info

            # Debug predictions
            if 'debug_predictions' in st.session_state:
                debug_title = "🔍 AI విశ్లేషణ వివరాలు" if lang_code == 'te' else "🔍 AI Analysis Details"
                with st.expander(debug_title, expanded=False):
                    pred_title = "**టాప్ 3 అంచనాలు:**" if lang_code == 'te' else "**Top 3 Predictions:**"
                    st.write(pred_title)
                    for pred in st.session_state.debug_predictions:
                        icon = "🥇" if pred['rank'] == 1 else "🥈" if pred['rank'] == 2 else "🥉"
                        st.write(f"{icon} {pred['class']}: {pred['confidence']:.1%}")

            # Confidence display
            confidence_color = "🟢" if confidence >= 0.7 else "🟡" if confidence >= 0.4 else "🔴"
            confidence_text = "అధిక" if lang_code == 'te' else "High"
            if confidence < 0.7:
                confidence_text = "మధ్యస్థ" if lang_code == 'te' else "Medium"
            if confidence < 0.4:
                confidence_text = "తక్కువ" if lang_code == 'te' else "Low"

            st.markdown(f"""
            <div style='background: linear-gradient(45deg, #e8f5e8, #f0f8f0); padding: 20px; border-radius: 10px; margin: 10px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                <h3 style='margin: 0; color: #2d5a2d;'>{confidence_color} {t['ai_confidence']}: {confidence:.1%} ({confidence_text})</h3>
            </div>
            """, unsafe_allow_html=True)

            # Results display
            if "healthy" in disease.lower():
                st.success(f"✅ {t['healthy']}: {disease.replace('_', ' ')}")
                st.balloons()
            else:
                st.warning(f"⚠️ {t['disease_detected']}: {disease.replace('_', ' ')}")

                # Enhanced tabbed interface with translated labels
                tab_labels = [
                    f"📋 {t['treatment_info']}",
                    f"💰 {t['economic_impact']}",
                    f"📊 {t['spread_risk']}",
                    f"📅 {t['treatment_plan']}",
                    f"📱 {t['whatsapp_share']}"
                ]
                tab1, tab2, tab3, tab4, tab5 = st.tabs(tab_labels)

                with tab1:
                    st.subheader(f"📋 {t['disease_information']}")

                    st.markdown(f"**📝 {t['description']}:**")
                    desc_text = treatment_info.get('description', 'N/A')
                    # Clean Telugu text
                    if '[translate:' in desc_text:
                        desc_text = desc_text.replace('[translate:', '').replace(']', '')
                    st.info(desc_text)

                    st.markdown(f"**🦠 {t['cause']}:**")
                    cause_text = treatment_info.get('cause', 'Unknown cause')
                    if '[translate:' in cause_text:
                        cause_text = cause_text.replace('[translate:', '').replace(']', '')
                    st.warning(cause_text)

                    treat_col1, treat_col2 = st.columns(2)

                    with treat_col1:
                        st.markdown(f"**{t['organic_treatment']}:**")
                        organic_treatments = treatment_info.get('organic_treatment', [])
                        for i, item in enumerate(organic_treatments, 1):
                            clean_item = item.replace('[translate:', '').replace(']', '')
                            st.write(f"{i}. {clean_item}")

                    with treat_col2:
                        st.markdown(f"**{t['chemical_treatment']}:**")
                        chemical_treatments = treatment_info.get('chemical_treatment', [])
                        for i, item in enumerate(chemical_treatments, 1):
                            clean_item = item.replace('[translate:', '').replace(']', '')
                            st.write(f"{i}. {clean_item}")

                    cost_text = treatment_info.get('cost_estimate', 'N/A')
                    if '[translate:' in cost_text:
                        cost_text = cost_text.replace('[translate:', '').replace(']', '')
                    st.markdown(f"**💰 {t['estimated_cost']}:** {cost_text}")

                with tab2:
                    st.subheader(f"💰 {t['economic_impact_analysis']}")
                    economic_data = calculate_economic_impact(
                        disease,
                        st.session_state.area_hectares,
                        st.session_state.crop_value
                    )

                    impact_col1, impact_col2, impact_col3 = st.columns(3)
                    with impact_col1:
                        delta_text = f"✅ {t['best_outcome']}"
                        st.metric(t['early_detection'], f"₹{economic_data['early']:,.0f}", delta_text)
                    with impact_col2:
                        delta_text = f"⚠️ {t['loss_50']}"
                        st.metric(t['medium_delay'], f"₹{economic_data['medium']:,.0f}", delta_text)
                    with impact_col3:
                        delta_text = f"❌ {t['critical_loss']}"
                        st.metric(t['severe_impact'], f"₹{economic_data['severe']:,.0f}", delta_text)

                    st.markdown(f"**{t['total_crop_value']}:** ₹{economic_data['total_crop_value']:,.0f}")

                with tab3:
                    st.subheader(f"📊 {t['disease_spread_risk']}")
                    # Mock weather data for spread prediction
                    weather_data = {'humidity': 70, 'rain_forecast': 5}

                    risk_level = "Medium"
                    risk_level_te = "మధ్యస్థ"
                    if "Late_Blight" in disease:
                        risk_level = "High"
                        risk_level_te = "అధిక"
                    elif "healthy" in disease.lower():
                        risk_level = "Low"
                        risk_level_te = "తక్కువ"

                    risk_colors = {'Low': '#28a745', 'Medium': '#ffc107', 'High': '#dc3545'}
                    display_risk = risk_level_te if lang_code == 'te' else risk_level

                    st.markdown(f"""
                    <div style='background-color: {risk_colors[risk_level]}; color: white; padding: 20px; border-radius: 10px; text-align: center;'>
                        <h3>🦠 వ్యాధి వ్యాప్తి ప్రమాదం: {display_risk}</h3>
                    </div>
                    """, unsafe_allow_html=True)

                    if risk_level == "High":
                        if lang_code == 'te':
                            st.error("🚨 **తక్షణ చర్య అవసరం**")
                            st.write("• వ్యాధి వేగంగా వ్యాపిస్తుంది")
                            st.write("• పక్కనున్న మొక్కలను ప్రతిరోజూ పర్యవేక్షించండి")
                            st.write("• వెంటనే చికిత్సలు వేయండి")
                        else:
                            st.error("🚨 **URGENT ACTION REQUIRED**")
                            st.write("• Disease can spread rapidly")
                            st.write("• Monitor neighboring plants daily")
                            st.write("• Apply treatments immediately")
                    elif risk_level == "Medium":
                        if lang_code == 'te':
                            st.warning("⚠️ **దగ్గరగా పర్యవేక్షించండి**")
                            st.write("• నిత్య తనిఖీ సిఫార్సు")
                            st.write("• నివారణ చర్యలు సిఫార్సు")
                        else:
                            st.warning("⚠️ **MONITOR CLOSELY**")
                            st.write("• Regular inspection recommended")
                            st.write("• Preventive measures advisable")
                    else:
                        if lang_code == 'te':
                            st.success("✅ **తక్కువ ప్రమాదం**")
                            st.write("• సాధారణ పర్యవేక్షణ కొనసాగించండి")
                        else:
                            st.success("✅ **LOW RISK**")
                            st.write("• Continue normal monitoring")

                with tab4:
                    st.subheader(f"📅 {t['treatment_schedule']}")

                    if lang_code == 'te':
                        treatment_schedule = [
                            {'day': 1, 'action': 'వ్యాధిగ్రస్తమైన భాగాలను వెంటనే తొలగించండి', 'priority': 'Critical'},
                            {'day': 2, 'action': 'మొదటి చికిత్స స్ప్రే వేయండి', 'priority': 'High'},
                            {'day': 7, 'action': 'రెండవ చికిత్స ప్రయోగం', 'priority': 'Medium'},
                            {'day': 14, 'action': 'పురోగతిని పర్యవేక్షించి మళ్ళీ అంచనా వేయండి', 'priority': 'Medium'},
                            {'day': 21, 'action': 'అవసరమైతే చికిత్స కొనసాగించండి', 'priority': 'Low'}
                        ]
                    else:
                        treatment_schedule = [
                            {'day': 1, 'action': 'Remove infected parts immediately', 'priority': 'Critical'},
                            {'day': 2, 'action': 'Apply first treatment spray', 'priority': 'High'},
                            {'day': 7, 'action': 'Second treatment application', 'priority': 'Medium'},
                            {'day': 14, 'action': 'Monitor progress and reassess', 'priority': 'Medium'},
                            {'day': 21, 'action': 'Continue treatment if needed', 'priority': 'Low'}
                        ]

                    for item in treatment_schedule:
                        priority_colors = {'Critical': '🔴', 'High': '🟡', 'Medium': '🟠', 'Low': '🟢'}
                        day_text = "రోజు" if lang_code == 'te' else "Day"
                        st.write(f"**{day_text} {item['day']}** {priority_colors[item['priority']]} - {item['action']}")

                with tab5:
                    st.subheader(f"📱 {t['share_results']}")

                    whatsapp_message = generate_whatsapp_message(disease, confidence, treatment_info, lang_code)
                    qr_base64, whatsapp_url = create_whatsapp_qr_code(whatsapp_message)

                    if qr_base64 and whatsapp_url:
                        share_col1, share_col2 = st.columns(2)
                        with share_col1:
                            st.markdown(f"[📱 {t['click_to_share']}]({whatsapp_url})")
                            if st.button(f"📋 {t['copy_message']}"):
                                st.code(whatsapp_message)

                        with share_col2:
                            st.markdown(f'<img src="data:image/png;base64,{qr_base64}" width="200">',
                                        unsafe_allow_html=True)
                            st.caption(t['scan_qr'])


# All other pages with full language support
def crop_advisor_page(t):
    st.title(f"🌱 {t['crop_advisor']}")
    desc = "మట్టి మరియు వాతావరణ పరిస్థితుల ఆధారంగా AI-శక్తితో పంట సిఫార్సులు." if 'వ్యవసాయ' in t[
        'crop_advisor'] else "AI-powered crop recommendations based on soil and weather conditions."
    st.info(desc)

    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input(f"📍 {t['location']}", "Hyderabad")
        soil_options = ["clay", "sandy", "loamy"]
        soil_type = st.selectbox(f"🌾 {t['soil_type']}", soil_options)
        season_options = ["summer", "winter", "monsoon"]
        season = st.selectbox(f"🗓️ {t['season']}", season_options)

    with col2:
        if st.button(t['get_recommendations'], type="primary"):
            recommendations = get_crop_recommendations(location, season, soil_type)

            st.subheader(f"🌾 {t['recommended_crops']}")
            for i, crop in enumerate(recommendations, 1):
                st.markdown(f"""
                **{i}. {crop['crop']}**
                - {t['success_rate']}: {crop['success_rate']}%
                - {t['profit_potential']}: {crop['profit_potential']}
                - {t['water_requirement']}: {crop['water_req']}
                """)


def market_insights_page(t):
    st.title(f"📊 {t['market_insights']}")
    st.info(t['current_market_prices'])

    # Sample market data
    market_data = pd.DataFrame({
        'Crop': ['Tomato', 'Potato', 'Onion', 'Rice', 'Wheat'],
        'Price (₹/kg)': [25, 18, 22, 35, 28],
        'Change (%)': [5.2, -2.1, 8.5, 1.2, -0.5],
        'Trend': ['↑', '↓', '↑', '↑', '↓']
    })

    st.dataframe(market_data, use_container_width=True)

    # Price trend chart
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    chart_data = pd.DataFrame({
        'Date': dates,
        'Tomato': np.random.randint(20, 30, 30),
        'Potato': np.random.randint(15, 22, 30),
        'Onion': np.random.randint(18, 28, 30)
    })

    fig = px.line(chart_data, x='Date', y=['Tomato', 'Potato', 'Onion'],
                  title=f"30-Day {t['price_trends']} (₹/kg)")
    st.plotly_chart(fig, use_container_width=True)


def insurance_helper_page(t):
    st.title(f"🛡️ {t['insurance_helper']}")
    st.info(t['crop_insurance_assistance'])

    col1, col2 = st.columns(2)

    with col1:
        damage_percent = st.slider(t['damage_percentage'], 0, 100, 40)
        area_affected = st.number_input(t['area_affected'], 1.0, 100.0, 10.0)
        crop_options = ["Tomato", "Potato", "Rice", "Wheat", "Cotton"]
        crop_type = st.selectbox(t['crop_type'], crop_options)

    with col2:
        if damage_percent >= 33:
            st.success(f"✅ **{t['eligible_claim']}**")
            compensation = area_affected * damage_percent * 700
            st.metric(f"💰 {t['estimated_compensation']}", f"₹{compensation:,.0f}")

            st.subheader(f"📋 {t['required_documents']}")
            if 'insurance_helper' in t and 'అసిస్టెంట్' in t['insurance_helper']:
                st.write("• పంట బీమా పాలసీ కాపీ")
                st.write("• గ్రామ రెవెన్యూ అధికారి రిపోర్ట్")
                st.write("• దెబ్బతిన్న పంటల ఫోటోలు")
                st.write("• బ్యాంక్ ఖాతా వివరాలు")
            else:
                st.write("• Crop insurance policy copy")
                st.write("• Village revenue officer report")
                st.write("• Photographs of damaged crops")
                st.write("• Bank account details")
        else:
            st.error(f"❌ **{t['not_eligible']}**")


def weather_station_page(t):
    st.title(f"🌤️ {t['weather_station']}")
    st.info(t['weather_conditions'])

    location = st.text_input(f"📍 {t['location']}", "Hyderabad")

    if st.button(t['get_weather'], type="primary"):
        weather = get_weather_alerts(location)

        # Current weather metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(f"🌡️ {t['temperature']}", f"{weather['temperature']:.1f}°C",
                      f"Feels like {weather.get('feels_like', 0):.1f}°C")
        with col2:
            st.metric(f"💧 {t['humidity']}", f"{weather['humidity']}%")
        with col3:
            st.metric(f"💨 {t['wind_speed']}", f"{weather['wind_speed']:.1f} m/s")
        with col4:
            st.metric(f"🌧️ {t['rain_24h']}", f"{weather['rain_forecast']:.1f}mm")

        # Disease risk assessment
        risk_colors = {'Low': '#28a745', 'Medium': '#ffc107', 'High': '#dc3545'}
        st.markdown(f"""
        <div style='background-color: {risk_colors[weather["disease_risk"]]}; color: white; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;'>
            <h3>🦠 {t['disease_risk_level']}: {weather["disease_risk"]}</h3>
        </div>
        """, unsafe_allow_html=True)

        # Agricultural alerts
        if weather['alerts']:
            st.subheader(f"⚠️ {t['agricultural_alerts']}")
            for alert in weather['alerts']:
                if alert.startswith('⚠️') or alert.startswith('🌡️') or alert.startswith('❄️'):
                    st.warning(alert)
                elif alert.startswith('🛡️') or alert.startswith('💧'):
                    st.info(alert)
                else:
                    st.write(alert)


def dashboard_page(t):
    st.title(f"📊 {t['dashboard']}")

    init_database()
    df = get_farmer_history()

    if len(df) > 0:
        # Enhanced statistics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(t['total_analyses'], len(df))
        with col2:
            diseases = len(df[~df['disease'].str.contains('healthy', case=False, na=False)])
            st.metric(t['diseases_detected'], diseases)
        with col3:
            if 'confidence' in df.columns:
                avg_conf = df['confidence'].mean()
                st.metric(t['avg_confidence'], f"{avg_conf:.1%}" if not pd.isna(avg_conf) else "N/A")
        with col4:
            recent = len(df[df['timestamp'] >= (datetime.now() - timedelta(days=7)).isoformat()])
            st.metric(t['this_week'], recent)

        # Charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(t['disease_distribution'])
            disease_counts = df['disease'].value_counts().head(10)
            fig_pie = px.pie(values=disease_counts.values, names=disease_counts.index)
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            st.subheader(t['analysis_timeline'])
            df['date'] = pd.to_datetime(df['timestamp']).dt.date
            timeline = df.groupby('date').size().reset_index(name='count')
            fig_line = px.line(timeline, x='date', y='count')
            st.plotly_chart(fig_line, use_container_width=True)

        # Recent history
        st.subheader(f"📋 {t['recent_history']}")
        if not df.empty:
            display_df = df.head(15)[['timestamp', 'disease', 'confidence', 'location']].copy()
            if 'confidence' in display_df.columns:
                display_df['confidence'] = display_df['confidence'].apply(
                    lambda x: f"{x:.1%}" if pd.notnull(x) else "N/A")
            st.dataframe(display_df, use_container_width=True)
    else:
        st.info(f"📊 {t['no_history']}")


def main():
    init_database()

    # Language selection with persistence
    if 'selected_language' not in st.session_state:
        st.session_state.selected_language = "English"

    language_options = ["English", "తెలుగు"]
    language = st.sidebar.selectbox(
        "🌐 Language / భాష",
        language_options,
        index=language_options.index(st.session_state.selected_language)
    )

    if language != st.session_state.selected_language:
        st.session_state.selected_language = language
        st.rerun()

    lang_code = 'en' if language == "English" else 'te'
    t = TRANSLATIONS[lang_code]

    # Enhanced Navigation with full translation
    page = st.sidebar.selectbox(f"📍 {t['navigation']}", [
        f"🔍 {t['disease_detection']}",
        f"🌱 {t['crop_advisor']}",
        f"📊 {t['market_insights']}",
        f"🛡️ {t['insurance_helper']}",
        f"🌤️ {t['weather_station']}",
        f"📈 {t['dashboard']}"
    ])

    # Route to pages
    if "🔍" in page:
        disease_detection_page(t, lang_code)
    elif "🌱" in page:
        crop_advisor_page(t)
    elif "📊" in page:
        market_insights_page(t)
    elif "🛡️" in page:
        insurance_helper_page(t)
    elif "🌤️" in page:
        weather_station_page(t)
    elif "📈" in page:
        dashboard_page(t)


if __name__ == "__main__":
    main()

