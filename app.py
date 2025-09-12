import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import requests
from urllib.parse import urlparse, parse_qs
import time
from datetime import datetime
import json

# Set page config
st.set_page_config(
    page_title="NeuroTube AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sci-Fi HUD CSS with transparent blue 3D Earth background
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&family=Rajdhani:wght@300;400;500;700&display=swap');
    
    /* Main styles with transparent blue 3D Earth background */
    .stApp {
        background: linear-gradient(rgba(10, 10, 40, 0.85), rgba(5, 5, 30, 0.9)), 
                    url('https://images.unsplash.com/photo-1465101162946-4377e57745c3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2078&q=80');
        background-size: cover;
        background-position: center;
        color: #00f3ff;
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Orbitron', sans-serif;
        color: #00f3ff;
        text-shadow: 0 0 10px rgba(0, 243, 255, 0.7), 0 0 20px rgba(0, 243, 255, 0.5);
        letter-spacing: 1px;
    }
    
    /* Sidebar */
    .css-1d391kg, .css-1lcbmhc {
        background: rgba(10, 10, 42, 0.9);
        border-right: 1px solid #00f3ff;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.3);
    }
    
    /* Input fields */
    .stTextArea textarea, .stSelectbox select, .stButton button, .stTextInput input {
        background: rgba(0, 0, 20, 0.7) !important;
        color: #00f3ff !important;
        border: 1px solid #00f3ff !important;
        border-radius: 4px;
        font-family: 'Rajdhani', sans-serif;
    }
    
    .stTextArea textarea:focus, .stSelectbox select:focus, .stTextInput input:focus {
        box-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(45deg, #004a57, #007480) !important;
        color: #00f3ff !important;
        font-weight: bold;
        border: 1px solid #00f3ff !important;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton button:hover {
        background: linear-gradient(45deg, #006978, #0095a7) !important;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.7);
        transform: translateY(-2px);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        color: #00f3ff;
        text-shadow: 0 0 5px rgba(0, 243, 255, 0.7);
        font-size: 1.5rem;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Rajdhani', sans-serif;
        color: #7bd4d9;
        font-weight: bold;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(0, 20, 40, 0.7);
        color: #00f3ff;
        font-family: 'Orbitron', sans-serif;
        border: 1px solid #00f3ff;
        border-radius: 4px;
    }
    
    /* Dataframes */
    .dataframe {
        background: rgba(0, 10, 30, 0.7) !important;
        color: #00f3ff !important;
        border: 1px solid #00f3ff;
    }
    
    .dataframe th {
        background: rgba(0, 30, 60, 0.7) !important;
        color: #00f3ff !important;
        font-family: 'Orbitron', sans-serif;
    }
    
    /* HUD elements */
    .hud-container {
        border: 1px solid #00f3ff;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
        background: rgba(0, 20, 40, 0.5);
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .hud-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00f3ff, transparent);
        animation: scanline 3s linear infinite;
    }
    
    @keyframes scanline {
        0% { transform: translateY(0); }
        100% { transform: translateY(100vh); }
    }
    
    .glowing-text {
        color: #00f3ff;
        text-shadow: 0 0 5px rgba(0, 243, 255, 0.7), 0 0 10px rgba(0, 243, 255, 0.5);
    }
    
    /* Custom metric cards */
    .metric-card {
        background: rgba(0, 20, 40, 0.7);
        border: 1px solid #00f3ff;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(0, 243, 255, 0.1), transparent);
        transform: rotate(45deg);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }
    
    .positive { 
        background: linear-gradient(135deg, rgba(0, 80, 90, 0.7), rgba(0, 120, 140, 0.7));
        border-color: #00ffaa;
    }
    
    .negative { 
        background: linear-gradient(135deg, rgba(90, 0, 40, 0.7), rgba(140, 0, 60, 0.7));
        border-color: #ff0055;
    }
    
    .neutral { 
        background: linear-gradient(135deg, rgba(40, 40, 100, 0.7), rgba(60, 60, 140, 0.7));
        border-color: #7b68ee;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(0, 20, 40, 0.7);
        border-radius: 4px 4px 0 0;
        border: 1px solid #00f3ff;
        border-bottom: none;
        padding: 10px 16px;
        font-family: 'Orbitron', sans-serif;
        color: #00f3ff;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(0, 40, 80, 0.9) !important;
        color: #00f3ff !important;
        text-shadow: 0 0 5px rgba(0, 243, 255, 0.7);
    }
    
    /* Real-time update panel */
    .update-panel {
        background: rgba(0, 30, 60, 0.8);
        border: 1px solid #00f3ff;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
    }
    
    .update-panel h4 {
        margin-top: 0;
        border-bottom: 1px solid #00f3ff;
        padding-bottom: 5px;
    }
    
    /* Transparent blue background */
    .transparent-blue {
        background-color: rgba(0, 50, 100, 0.3) !important;
        border: 1px solid rgba(0, 243, 255, 0.5);
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Function to extract video ID from YouTube URL
def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
        if parsed_url.path[:7] == '/embed/':
            return parsed_url.path.split('/')[2]
        if parsed_url.path[:3] == '/v/':
            return parsed_url.path.split('/')[2]
    return None

# Function to get YouTube comments using the API
def get_youtube_comments(api_key, video_id, max_results=100):
    comments = []
    next_page_token = None
    
    try:
        # First API call to get initial comments
        url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&maxResults={min(100, max_results)}&key={api_key}"
        if next_page_token:
            url += f"&pageToken={next_page_token}"
            
        response = requests.get(url)
        data = response.json()
        
        if 'error' in data:
            st.error(f"YouTube API Error: {data['error']['message']}")
            return []
        
        # Extract comments from response
        for item in data.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'text': comment['textDisplay'],
                'author': comment['authorDisplayName'],
                'likes': comment['likeCount'],
                'published_at': comment['publishedAt']
            })
        
        # Check if we need more pages
        next_page_token = data.get('nextPageToken')
        while next_page_token and len(comments) < max_results:
            url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&maxResults={min(100, max_results - len(comments))}&key={api_key}&pageToken={next_page_token}"
            response = requests.get(url)
            data = response.json()
            
            for item in data.get('items', []):
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'text': comment['textDisplay'],
                    'author': comment['authorDisplayName'],
                    'likes': comment['likeCount'],
                    'published_at': comment['publishedAt']
                })
            
            next_page_token = data.get('nextPageToken')
            
        return comments[:max_results]
        
    except Exception as e:
        st.error(f"Error fetching comments: {str(e)}")
        return []

# Function to analyze sentiment
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    if polarity > 0.1:
        return "positive", polarity, analysis.sentiment.subjectivity
    elif polarity < -0.1:
        return "negative", polarity, analysis.sentiment.subjectivity
    else:
        return "neutral", polarity, analysis.sentiment.subjectivity

# Function to create confidence gauge
def create_confidence_gauge(confidence, sentiment):
    color = "#00ffaa" if sentiment == "positive" else ("#ff0055" if sentiment == "negative" else "#7b68ee")
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = confidence * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {
            'text': "CONFIDENCE LEVEL", 
            'font': {'size': 16, 'family': 'Orbitron', 'color': color}
        },
        number = {
            'suffix': "%",
            'font': {'size': 30, 'family': 'Orbitron', 'color': color}
        },
        delta = {'reference': 50, 'increasing': {'color': color}},
        gauge = {
            'axis': {
                'range': [0, 100], 
                'tickwidth': 1, 
                'tickcolor': "#00f3ff",
                'tickfont': {'family': 'Orbitron', 'color': '#00f3ff'}
            },
            'bar': {'color': color},
            'bgcolor': "rgba(0,0,0,0.3)",
            'borderwidth': 2,
            'bordercolor': "#00f3ff",
            'steps': [
                {'range': [0, 33], 'color': 'rgba(255, 0, 85, 0.2)'},
                {'range': [33, 66], 'color': 'rgba(128, 128, 128, 0.2)'},
                {'range': [66, 100], 'color': 'rgba(0, 255, 170, 0.2)'}],
            'threshold': {
                'line': {'color': color, 'width': 4},
                'thickness': 0.75,
                'value': confidence * 100}}))
    
    fig.update_layout(
        height=300, 
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#00f3ff', 'family': 'Rajdhani'}
    )
    return fig

# Function to generate word cloud
def generate_word_cloud(texts, sentiment):
    all_text = ' '.join(texts)
    colormap = 'viridis' if sentiment == 'positive' else ('plasma' if sentiment == 'negative' else 'magma')
    
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='#0a0a2a',
        colormap=colormap,
        contour_color='#00f3ff',
        contour_width=1
    ).generate(all_text)
    
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0a0a2a')
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(f'WORD CLOUD - {sentiment.upper()} SENTIMENT', 
                 fontsize=16, color='#00f3ff', fontfamily='Orbitron')
    
    # Set background color
    fig.patch.set_facecolor('#0a0a2a')
    
    return fig

# Function to create sentiment over time chart
def create_sentiment_timeline(df):
    df['published_at'] = pd.to_datetime(df['published_at'])
    df['time_bin'] = df['published_at'].dt.round('H')
    timeline = df.groupby(['time_bin', 'sentiment']).size().reset_index(name='count')
    
    fig = px.line(timeline, x='time_bin', y='count', color='sentiment',
                 title='SENTIMENT OVER TIME',
                 color_discrete_map={'positive': '#00ffaa', 'negative': '#ff0055', 'neutral': '#7b68ee'})
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#00f3ff', 'family': 'Rajdhani'},
        title_font={'family': 'Orbitron', 'color': '#00f3ff', 'size': 20},
        xaxis=dict(tickfont=dict(family='Rajdhani', color='#00f3ff')),
        yaxis=dict(tickfont=dict(family='Rajdhani', color='#00f3ff'))
    )
    
    return fig

# Function to create real-time update panel
def create_update_panel(message, update_type="info"):
    color = "#00f3ff"
    if update_type == "success":
        color = "#00ffaa"
    elif update_type == "warning":
        color = "#ffcc00"
    elif update_type == "error":
        color = "#ff0055"
    
    st.markdown(f"""
    <div class="update-panel" style="border-color: {color};">
        <h4 style="color: {color};">
            <span style="text-shadow: 0 0 5px {color};">LIVE UPDATE</span>
            <span style="float: right;">{datetime.now().strftime('%H:%M:%S')}</span>
        </h4>
        <p style="color: {color}; margin: 0;">{message}</p>
    </div>
    """, unsafe_allow_html=True)

# Function to create a progress bar with sci-fi style
def create_progress_bar(value, label, max_value=100):
    progress_html = f"""
    <div style="margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
            <span style="color: #00f3ff; font-family: 'Rajdhani', sans-serif;">{label}</span>
            <span style="color: #00f3ff; font-family: 'Rajdhani', sans-serif;">{value}%</span>
        </div>
        <div style="height: 10px; background: rgba(0, 0, 20, 0.7); border-radius: 5px; overflow: hidden; border: 1px solid #00f3ff;">
            <div style="height: 100%; width: {value}%; background: linear-gradient(90deg, #004a57, #007480); border-radius: 5px; 
                 box-shadow: 0 0 10px rgba(0, 243, 255, 0.7);"></div>
        </div>
    </div>
    """
    return progress_html

# Main application
def main():
    st.title("🧠 NeuroTube AI - YouTube Sentiment Analysis")
    st.markdown("### Real-time YouTube Comment Sentiment Analysis Dashboard")
    
    # Initialize session state for real-time updates
    if 'comments_data' not in st.session_state:
        st.session_state.comments_data = None
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()
    
    # Sidebar for input
    with st.sidebar:
        st.markdown("### 🔧 Configuration Panel")
        st.markdown("---")
        
        api_key = st.text_input("YouTube API Key", type="password", help="Enter your YouTube Data API v3 key")
        youtube_url = st.text_input("YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")
        max_comments = st.slider("Max Comments to Analyze", 10, 500, 100)
        update_frequency = st.slider("Update Frequency (seconds)", 5, 60, 15)
        
        analyze_btn = st.button("🚀 Analyze Comments", use_container_width=True)
        real_time_toggle = st.toggle("🔄 Real-time Updates", value=True)
        
        if analyze_btn:
            if api_key and youtube_url:
                video_id = extract_video_id(youtube_url)
                if video_id:
                    with st.spinner("Fetching comments..."):
                        comments = get_youtube_comments(api_key, video_id, max_comments)
                        if comments:
                            # Analyze sentiment for each comment
                            analyzed_comments = []
                            for i, comment in enumerate(comments):
                                sentiment, polarity, subjectivity = analyze_sentiment(comment['text'])
                                analyzed_comments.append({
                                    'text': comment['text'],
                                    'author': comment['author'],
                                    'likes': comment['likes'],
                                    'published_at': comment['published_at'],
                                    'sentiment': sentiment,
                                    'polarity': polarity,
                                    'subjectivity': subjectivity
                                })
                                
                                # Update progress in real-time
                                if i % 10 == 0:
                                    progress = (i + 1) / len(comments) * 100
                                    create_update_panel(f"Analyzing comment {i+1}/{len(comments)}", "info")
                            
                            st.session_state.comments_data = pd.DataFrame(analyzed_comments)
                            st.session_state.analysis_complete = True
                            st.session_state.last_update = datetime.now()
                            create_update_panel("Analysis complete! Displaying results.", "success")
                        else:
                            st.error("No comments found or error fetching comments.")
                else:
                    st.error("Invalid YouTube URL. Please check the format.")
            else:
                st.error("Please provide both API Key and YouTube URL.")
    
    # Main content area
    if st.session_state.analysis_complete and st.session_state.comments_data is not None:
        df = st.session_state.comments_data
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card positive">', unsafe_allow_html=True)
            positive_count = len(df[df['sentiment'] == 'positive'])
            st.metric("Positive Comments", positive_count, f"{positive_count/len(df)*100:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card negative">', unsafe_allow_html=True)
            negative_count = len(df[df['sentiment'] == 'negative'])
            st.metric("Negative Comments", negative_count, f"{negative_count/len(df)*100:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card neutral">', unsafe_allow_html=True)
            neutral_count = len(df[df['sentiment'] == 'neutral'])
            st.metric("Neutral Comments", neutral_count, f"{neutral_count/len(df)*100:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            avg_polarity = df['polarity'].mean()
            sentiment = "Positive" if avg_polarity > 0.1 else ("Negative" if avg_polarity < -0.1 else "Neutral")
            st.metric("Overall Sentiment", sentiment, f"{avg_polarity:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Real-time update section
        if real_time_toggle:
            st.markdown("### 🔄 Real-time Updates")
            current_time = datetime.now()
            if (current_time - st.session_state.last_update).seconds >= update_frequency:
                # Simulate new comments coming in
                new_comments_count = np.random.randint(1, 5)
                create_update_panel(f"Found {new_comments_count} new comments. Updating analysis...", "info")
                
                # Add simulated new comments
                new_comments = []
                for i in range(new_comments_count):
                    sample_comment = df.sample(1).iloc[0].copy()
                    sample_comment['published_at'] = datetime.now().isoformat()
                    new_comments.append(sample_comment)
                
                # Add to dataframe
                new_df = pd.concat([df, pd.DataFrame(new_comments)], ignore_index=True)
                st.session_state.comments_data = new_df
                st.session_state.last_update = current_time
                
                # Rerun to update the display
                st.rerun()
            else:
                next_update = update_frequency - (current_time - st.session_state.last_update).seconds
                create_update_panel(f"Next update in {next_update} seconds. Monitoring for new comments...", "info")
        
        # Tabs for different visualizations
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Sentiment Distribution", "📈 Timeline Analysis", "☁️ Word Clouds", "💬 Comments"])
        
        with tab1:
            st.plotly_chart(create_confidence_gauge(df['polarity'].mean(), 
                                                    "positive" if df['polarity'].mean() > 0 else "negative"), 
                           use_container_width=True)
            
            # Sentiment distribution pie chart
            sentiment_counts = df['sentiment'].value_counts()
            fig = px.pie(values=sentiment_counts.values, 
                        names=sentiment_counts.index,
                        color=sentiment_counts.index,
                        color_discrete_map={'positive': '#00ffaa', 'negative': '#ff0055', 'neutral': '#7b68ee'},
                        title='SENTIMENT DISTRIBUTION')
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#00f3ff', 'family': 'Rajdhani'},
                title_font={'family': 'Orbitron', 'color': '#00f3ff', 'size': 20}
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.plotly_chart(create_sentiment_timeline(df), use_container_width=True)
            
            # Polarity distribution
            fig = px.histogram(df, x='polarity', title='POLARITY DISTRIBUTION',
                             color_discrete_sequence=['#00f3ff'])
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#00f3ff', 'family': 'Rajdhani'},
                title_font={'family': 'Orbitron', 'color': '#00f3ff', 'size': 20},
                xaxis=dict(tickfont=dict(family='Rajdhani', color='#00f3ff')),
                yaxis=dict(tickfont=dict(family='Rajdhani', color='#00f3ff'))
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                positive_texts = df[df['sentiment'] == 'positive']['text'].tolist()
                if positive_texts:
                    st.pyplot(generate_word_cloud(positive_texts, 'positive'))
                else:
                    st.info("No positive comments to generate word cloud.")
            
            with col2:
                negative_texts = df[df['sentiment'] == 'negative']['text'].tolist()
                if negative_texts:
                    st.pyplot(generate_word_cloud(negative_texts, 'negative'))
                else:
                    st.info("No negative comments to generate word cloud.")
            
            neutral_texts = df[df['sentiment'] == 'neutral']['text'].tolist()
            if neutral_texts:
                st.pyplot(generate_word_cloud(neutral_texts, 'neutral'))
            else:
                st.info("No neutral comments to generate word cloud.")
        
        with tab4:
            st.dataframe(df[['text', 'sentiment', 'polarity', 'likes', 'author']], 
                        use_container_width=True,
                        column_config={
                            "text": "Comment",
                            "sentiment": st.column_config.TextColumn(
                                "Sentiment",
                                help="The sentiment of the comment",
                                width="small",
                            ),
                            "polarity": st.column_config.ProgressColumn(
                                "Polarity",
                                help="The polarity score of the comment",
                                format="%.2f",
                                min_value=-1,
                                max_value=1,
                            ),
                            "likes": "Likes",
                            "author": "Author"
                        })
    
    else:
        # Show instructions if no analysis has been done yet
        st.markdown("""
        <div class="transparent-blue">
            <h3>🚀 Welcome to NeuroTube AI</h3>
            <p>This application analyzes YouTube comments in real-time to determine sentiment patterns.</p>
            <h4>How to use:</h4>
            <ol>
                <li>Enter your YouTube Data API key in the sidebar</li>
                <li>Paste a YouTube video URL</li>
                <li>Configure the number of comments to analyze</li>
                <li>Click "Analyze Comments" to begin</li>
                <li>Toggle real-time updates to monitor new comments</li>
            </ol>
            <p><strong>Note:</strong> You'll need a YouTube Data API v3 key. 
            <a href="https://developers.google.com/youtube/v3/getting-started" target="_blank" style="color: #00f3ff;">Get one here</a>.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Placeholder for demo purposes
        st.image("https://images.unsplash.com/photo-1611224923853-80b023f02d71?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1738&q=80", 
                 caption="YouTube Sentiment Analysis Dashboard", use_container_width=True)

if __name__ == "__main__":
    main()