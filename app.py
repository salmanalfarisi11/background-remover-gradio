import os
import tempfile
import gradio as gr
from rembg import remove
from PIL import Image

# Force ONNXRuntime to CPU only
os.environ["ORT_PROVIDERS"] = "CPUExecutionProvider"

def remove_background(input_image: Image.Image) -> Image.Image:
    """Your existing remover."""
    return remove(input_image)

def remove_and_save(img: Image.Image):
    """
    1) remove background,
    2) save to a temp PNG,
    3) return (PIL.Image for preview, file path for DownloadButton).
    """
    result = remove_background(img)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    result.save(tmp.name, format="PNG")
    tmp.close()
    return result, tmp.name

with gr.Blocks() as demo:
    gr.Markdown("## 🖼️ Background Remover")
    gr.Markdown(
        "Upload an image and click **Remove Background** to get a transparent PNG.  \n"
        "**Note:** CPU-only ONNX Runtime (no GPU needed)."
    )

    with gr.Row():
        original = gr.Image(type="pil", label="Original")
        result   = gr.Image(type="pil", label="Result")

    # Stack Remove + Download vertically
    with gr.Column(elem_id="controls"):
        remove_btn   = gr.Button("✂️ Remove Background", variant="primary")
        download_btn = gr.DownloadButton("⬇️ Download PNG")

    remove_btn.click(
        fn=remove_and_save,
        inputs=original,
        outputs=[result, download_btn],
    )

    # Centered footer
    demo.css = """
      #controls { align-items: start; gap: 0.5rem; }
      .footer { text-align: center; margin-top: 2rem; color: #666; font-size:0.9rem; }
      .social-icons a { margin: 0 0.5rem; text-decoration: none; color: inherit; }
    """

    gr.HTML("""
      <div class="footer">
        Made by Salman Alfarisi • 2025<br>
        <span class="social-icons">
          <a href="https://github.com/salmanalfarisi11" target="_blank">GitHub</a> |
          <a href="https://www.instagram.com/faris.salman111/" target="_blank">Instagram</a> |
          <a href="https://id.linkedin.com/in/salmanalfarisi11" target="_blank">LinkedIn</a>
        </span><br>
        Source code on <a href="https://github.com/salmanalfarisi11" target="_blank">GitHub</a>
      </div>
    """)

if __name__ == "__main__":
    demo.launch()