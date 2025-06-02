import streamlit as st
from pytube import YouTube
import os

st.set_page_config(page_title="YouTube Downloader", layout="centered")

st.title("📥 YouTube Video Downloader")

# Input URL
url = st.text_input("Enter YouTube video URL:")

if url:
    try:
        yt = YouTube(url)
        st.video(url)

        st.write(f"**Title:** {yt.title}")
        st.write(f"**Channel:** {yt.author}")
        st.write(f"**Length:** {yt.length} seconds")

        # Get available streams
        streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        stream_options = [f"{stream.resolution} - {round(stream.filesize / (1024 * 1024), 2)} MB" for stream in streams]

        # Select stream
        choice = st.selectbox("Choose resolution:", stream_options)

        if st.button("Download"):
            index = stream_options.index(choice)
            stream = streams[index]
            file_path = stream.download()
            with open(file_path, "rb") as f:
                st.download_button(label="Download Video", data=f, file_name=os.path.basename(file_path))
            os.remove(file_path)

    except Exception as e:
        st.error(f"Error: {e}")
