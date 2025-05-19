import streamlit as st
import os
from Senti import extract_video_id, analyze_sentiment, bar_chart, plot_sentiment
from YoutubeCommentScrapper import save_video_comments_to_csv, get_channel_info, youtube, get_channel_id, get_video_stats

def delete_non_matching_csv_files(directory_path, video_id):
    for file_name in os.listdir(directory_path):
        if not file_name.endswith('.csv') or file_name == f'{video_id}.csv':
            continue
        os.remove(os.path.join(directory_path, file_name))

# Page Configuration
st.set_page_config(page_title='YouTube Comment Analysis', page_icon='🎥', layout='wide')

# Custom Styling
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #ff5733;
            margin-bottom: 20px;
        }
        .metric-container {
            background-color: green;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
        .video-container {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
        .sidebar-input {
            font-size: 16px;
            border-radius: 10px;
        }
        .info-box {
            padding: 15px;
            border-radius: 10px;
            background: #e8f5e9;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 15px;
        }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.image("LOGO.png", use_column_width=True)
st.sidebar.title("📊 Sentiment Analysis")
st.sidebar.header("🔗 Enter YouTube Link")
youtube_link = st.sidebar.text_input("Paste Link Here", placeholder="Enter a valid YouTube URL")

# Hide Streamlit Footer & Menu
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

if youtube_link:
    video_id = extract_video_id(youtube_link)
    channel_id = get_channel_id(video_id)
    
    if video_id:
        st.sidebar.success(f"✅ Video ID: {video_id}")
        csv_file = save_video_comments_to_csv(video_id)
        delete_non_matching_csv_files(os.getcwd(), video_id)
        
        st.sidebar.download_button(
            label="📥 Download Comments",
            data=open(csv_file, 'rb').read(),
            file_name=os.path.basename(csv_file),
            mime="text/csv"
        )
        
        channel_info = get_channel_info(youtube, channel_id)
        stats = get_video_stats(video_id)
        
        # Channel Section
        with st.container():
            st.markdown("<h1 class='main-title'>🎬 Channel Overview</h1>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 3])
            col1.image(channel_info['channel_logo_url'], width=150)
            with col2:
                st.markdown(f"<div class='info-box'><b>📌 Channel Name:</b> {channel_info['channel_title']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-box'><b>📅 Created On:</b> {channel_info['channel_created_date'][:10]}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-box'><b>📺 Total Videos:</b> {channel_info['video_count']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-box'><b>👥 Subscribers:</b> {channel_info['subscriber_count']}</div>", unsafe_allow_html=True)
        
        # Video Stats Section
        with st.container():
            st.markdown("<h1 class='main-title'>🎥 Video Statistics</h1>", unsafe_allow_html=True)
            col3, col4, col5 = st.columns(3)
            col3.markdown("<div class='metric-container'><h3>👁 Total Views</h3><h2>" + stats["viewCount"] + "</h2></div>", unsafe_allow_html=True)
            col4.markdown("<div class='metric-container'><h3>👍 Likes</h3><h2>" + stats["likeCount"] + "</h2></div>", unsafe_allow_html=True)
            col5.markdown("<div class='metric-container'><h3>💬 Comments</h3><h2>" + stats["commentCount"] + "</h2></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='video-container'>", unsafe_allow_html=True)
        st.video(youtube_link)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Sentiment Analysis
        results = analyze_sentiment(csv_file)
        with st.container():
            st.markdown("<h1 class='main-title'>📊 Sentiment Analysis</h1>", unsafe_allow_html=True)
            col6, col7, col8 = st.columns(3)
            col6.markdown("<div class='metric-container'><h3>😊 Positive Comments</h3><h2>" + str(results['num_positive']) + "</h2></div>", unsafe_allow_html=True)
            col7.markdown("<div class='metric-container'><h3>😡 Negative Comments</h3><h2>" + str(results['num_negative']) + "</h2></div>", unsafe_allow_html=True)
            col8.markdown("<div class='metric-container'><h3>😐 Neutral Comments</h3><h2>" + str(results['num_neutral']) + "</h2></div>", unsafe_allow_html=True)
        
        bar_chart(csv_file)
        plot_sentiment(csv_file)
    
    else:
        st.error("❌ Invalid YouTube link. Please enter a valid URL.")