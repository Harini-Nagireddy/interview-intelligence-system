from moviepy import VideoFileClip, AudioFileClip

def merge_audio_video(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    final_video = video.with_audio(audio)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)

    video.close()
    audio.close()

    return output_path
