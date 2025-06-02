import streamlit as st
from pytube import YouTube
import os
import tempfile

st.set_page_config(page_title="YouTube Downloader", layout="centered")

st.title("📥 YouTube Video Downloader")

url = st.text_input("🎥 Enter YouTube video URL:")

if url:
    try:
        yt = YouTube(url)
        st.video(url)

        st.write(f"**Title:** {yt.title}")
        st.write(f"**Channel:** {yt.author}")
        st.write(f"**Length:** {yt.length // 60} min {yt.length % 60} sec")

        # Get available progressive streams (video + audio)
        streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        stream_options = [f"{i.resolution} - {round(i.filesize / 1024 / 1024, 2)} MB" for i in streams]

        selected = st.selectbox("Select resolution to download:", stream_options)

        if st.button("Download"):
            index = stream_options.index(selected)
            stream = streams[index]

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                stream.download(output_path=os.path.dirname(tmp_file.name), filename=os.path.basename(tmp_file.name))
                with open(tmp_file.name, "rb") as video_file:
                    btn = st.download_button(
                        label="📥 Click here to save the video",
                        data=video_file,
                        file_name=yt.title.replace(" ", "_") + ".mp4",
                        mime="video/mp4"
                    )
                os.remove(tmp_file.name)

    except Exception as e:
        st.error(f"❌ Error: {e}")
