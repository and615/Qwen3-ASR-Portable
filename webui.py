import gradio as gr
import tempfile
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

print("=" * 50)
print("  Qwen3-ASR Speech Recognition")
print("=" * 50)
print(f"Script dir: {SCRIPT_DIR}")

AVAILABLE_MODELS = ["Qwen3-ASR-1.7B", "Qwen3-ASR-0.6B"]
LANGUAGES = ["Auto", "Chinese", "English", "Japanese", "Korean", "Cantonese"]

def process_audio(audio_file, model_name, language, enable_timestamps):
    if not audio_file:
        return "Please upload an audio file", None, None

    try:
        print(f"Processing: {audio_file}")
        print(f"Model: {model_name}, Language: {language}, Timestamps: {enable_timestamps}")

        # 在函数内部导入和创建engine，避免Gradio序列化torch对象
        from engine import Qwen3ASREngine
        from srt_generator import timestamps_to_srt

        engine = Qwen3ASREngine(model_dir=os.path.join(SCRIPT_DIR, "models"))

        result = engine.transcribe(
            audio=audio_file,
            model=model_name,
            lang=language if language != "Auto" else None,
            timestamps=enable_timestamps
        )

        if "error" in result:
            print(f"Error: {result['error']}")
            return result["error"], None, None

        print(f"Done: {result['text'][:100]}...")

        text_output = f"[Language] {result['language']}\n\n{result['text']}"

        output_dir = os.path.join(SCRIPT_DIR, "outputs")
        os.makedirs(output_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(audio_file))[0]

        txt_path = os.path.join(output_dir, f"{base}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(result["text"])

        srt_path = None
        if enable_timestamps and result["timestamps"]:
            srt_path = os.path.join(output_dir, f"{base}.srt")
            timestamps_to_srt(result["timestamps"], result["text"], srt_path)

        return text_output, txt_path, srt_path

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}", None, None

with gr.Blocks(title="Qwen3-ASR") as demo:
    gr.Markdown("# Qwen3-ASR Speech Recognition")
    gr.Markdown("Supports 52 languages and dialects, with SRT subtitle generation")

    with gr.Row():
        with gr.Column(scale=1):
            audio_input = gr.Audio(
                label="Upload Audio",
                type="filepath",
                sources=["upload", "microphone"]
            )
            model_select = gr.Dropdown(
                choices=AVAILABLE_MODELS, value="Qwen3-ASR-1.7B",
                label="Model"
            )
            language_input = gr.Dropdown(
                choices=LANGUAGES, value="Auto", label="Language"
            )
            enable_ts = gr.Checkbox(label="Enable timestamps (generate SRT)", value=False)
            submit_btn = gr.Button("Transcribe", variant="primary")

        with gr.Column(scale=2):
            text_output = gr.Textbox(label="Result", lines=10)
            txt_file = gr.File(label="Download TXT")
            srt_file = gr.File(label="Download SRT")

    submit_btn.click(
        fn=process_audio,
        inputs=[audio_input, model_select, language_input, enable_ts],
        outputs=[text_output, txt_file, srt_file]
    )

if __name__ == "__main__":
    import threading
    import webbrowser

    def open_browser():
        webbrowser.open("http://localhost:7860")

    print("Starting Web Interface...")
    timer = threading.Timer(2.0, open_browser)
    timer.start()
    demo.launch(server_name="0.0.0.0", server_port=7860)
