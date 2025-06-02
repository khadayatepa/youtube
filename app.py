import streamlit as st
from pytube import YouTube
import tempfile
import os

st.set_page_config(page_title="YouTube Downloader", layout="centered")

st.title("📥 YouTube Video Downloader")

url = st.text_input("Enter YouTube video URL:")

if url:
    try:
        yt = YouTube(url)

        st.video(url)
        st.success(f"Video Title: {yt.title}")
        st.info(f"Channel: {yt.author} | Duration: {yt.length // 60} min {yt.length % 60} sec")

        # Filter available progressive (audio+video) streams
        streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by("resolution").desc()
        options = [f"{s.resolution} ({round(s.filesize / 1024 / 1024, 2)} MB)" for s in streams]
        choice = st.selectbox("Select quality to download:", options)

        if st.button("Fetch & Prepare Download"):
            stream = streams[options.index(choice)]

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                file_path = stream.download(output_path=os.path.dirname(tmp.name), filename=os.path.basename(tmp.name))
                st.success("✅ Download ready!")

                with open(file_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Click to Download Video",
                        data=f,
                        file_name=yt.title.replace(" ", "_") + ".mp4",
                        mime="video/mp4"
                    )

                os.remove(file_path)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
