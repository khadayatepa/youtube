import streamlit as st
from pytube import YouTube
import tempfile
import os

st.set_page_config(page_title="YouTube Downloader", layout="centered")

st.title("📥 YouTube Video Downloader")

url = st.text_input("🎥 Enter YouTube video URL")

if url:
    try:
        yt = YouTube(url)
        st.video(url)

        st.markdown(f"**Title**: {yt.title}")
        st.markdown(f"**Length**: {yt.length // 60} min {yt.length % 60} sec")
        st.markdown(f"**Views**: {yt.views}")
        st.markdown(f"**Channel**: {yt.author}")

        # Filter out small progressive streams only
        streams = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").asc()

        # Check and exclude missing filesize values
        valid_streams = [s for s in streams if s.filesize is not None and s.filesize < 50 * 1024 * 1024]  # 50MB max
        if not valid_streams:
            st.warning("⚠️ No valid video streams under 50MB found. Try a shorter/lower-resolution video.")
        else:
            options = [f"{s.resolution} - {round(s.filesize / (1024 * 1024), 2)} MB" for s in valid_streams]
            choice = st.selectbox("Select resolution to download:", options)

            if st.button("Prepare Download"):
                idx = options.index(choice)
                selected_stream = valid_streams[idx]

                # Download to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                    file_path = selected_stream.download(
                        output_path=os.path.dirname(tmp_file.name),
                        filename=os.path.basename(tmp_file.name)
                    )

                # Show download button after file is ready
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Video",
                        data=f,
                        file_name=yt.title.replace(" ", "_") + ".mp4",
                        mime="video/mp4"
                    )
                os.remove(file_path)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
