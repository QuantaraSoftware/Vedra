import os
from flask import Flask
from pywebio import input, output
from pywebio.platform.flask import webio_view
from moviepy.editor import VideoFileClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips, ImageClip

import config

app = Flask(__name__)

os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)

def movies_editor():
    output.put_markdown("# Movies.Editor Web Video Editor (Render Compatible)")

    # 1️⃣ Upload videos
    video_files = input.file_upload(
        "Upload video clips (max 10 minutes each, multiple allowed)",
        accept="video/*",
        multiple=True
    )
    video_paths = []
    for idx, v in enumerate(video_files):
        path = os.path.join(config.UPLOAD_FOLDER, f"clip_{idx}.mp4")
        with open(path, "wb") as f:
            f.write(v['content'])
        video_paths.append(path)

    # 2️⃣ Optional: Upload background audio
    audio_file = input.file_upload("Upload background music (optional)", accept="audio/*")
    audio_path = None
    if audio_file:
        audio_path = os.path.join(config.UPLOAD_FOLDER, "bg_audio.mp3")
        with open(audio_path, "wb") as f:
            f.write(audio_file['content'])

    # 3️⃣ Select filter
    selected_filter = input.select("Select a video filter", options=list(config.FILTERS.keys()))

    # 4️⃣ Apply filter to clips
    clips = []
    for path in video_paths:
        clip = VideoFileClip(path).subclip(0, min(config.MAX_VIDEO_LENGTH, VideoFileClip(path).duration))
        clip = config.FILTERS[selected_filter](clip)
        clips.append(clip)

    # 5️⃣ Arrange clip order
    output.put_text("Arrange clip order (0 = first, etc.)")
    clip_order = []
    for i in range(len(clips)):
        order = input.input(f"Order for clip {i}", type=input.NUMBER, value=i)
        clip_order.append((order, clips[i]))
    clip_order.sort(key=lambda x: x[0])
    clips = [c[1] for c in clip_order]

    # 6️⃣ Concatenate clips
    final_clip = concatenate_videoclips(clips)

    # 7️⃣ Add watermark image
    if os.path.exists(config.WATERMARK_IMAGE):
        watermark = (ImageClip(config.WATERMARK_IMAGE)
                     .set_duration(final_clip.duration)
                     .resize(height=50)  # adjust size
                     .set_pos(("right", "bottom"))
                     .margin(right=10, bottom=10))
        composite = CompositeVideoClip([final_clip, watermark])
    else:
        composite = final_clip

    # 8️⃣ Merge background audio if exists
    if audio_path:
        bg_audio = AudioFileClip(audio_path).subclip(0, composite.duration)
        composite = composite.set_audio(bg_audio)

    # 9️⃣ Export
    output_path = os.path.join(config.OUTPUT_FOLDER, "output_movies_editor.mp4")
    composite.write_videofile(output_path, codec='libx264', audio_codec='aac')

    # 🔟 AI Feature placeholders
    output.put_markdown("### AI Features (Demo placeholders)")
    for feature in config.AI_FEATURES:
        output.put_text(f"- {feature}")

    # 1️⃣1️⃣ Download
    output.put_file("Download Edited Video", output_path)

# Flask routing
app.add_url_rule('/editor', 'webio_view', webio_view(movies_editor), methods=['GET', 'POST', 'OPTIONS'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
