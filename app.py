import os
import uuid
import gradio as gr
from diffusers import AuraFlowPipeline
import torch
from PIL import Image
from pathvalidate import sanitize_filename
import gc # Garbage Collector

# --- Configuration ---
# Ensure output and model directories exist
os.makedirs("output", exist_ok=True)
os.makedirs("models", exist_ok=True)

MODEL_FOLDER = "models"
OUTPUT_FOLDER = "output"
MODEL_NAME = "fal/AuraFlow-v0.3" # Official AuraFlow diffusers model

# Determine device and dtype
if torch.cuda.is_available():
    # Attempt to use cuda:0 first, then cuda:1, etc.
    # For a specific device like cuda:1, you can hardcode it.
    # However, let's try to be more flexible.
    try:
        torch.cuda.set_device(0) # Try primary GPU
        DEVICE = "cuda:0"
    except RuntimeError:
        print("CUDA device 0 not available or already in use. Trying cuda:1 if available.")
        try:
            torch.cuda.set_device(1)
            DEVICE = "cuda:1" # As per your original specific request
        except RuntimeError:
            print("CUDA device 1 not available. Falling back to CPU.")
            DEVICE = "cpu"
else:
    DEVICE = "cpu"

TORCH_DTYPE = torch.float16 if DEVICE.startswith("cuda") else torch.float32
VARIANT = "fp16" if DEVICE.startswith("cuda") else None # No fp16 variant for CPU usually

# --- Global Variables ---
pipeline = None
last_seed = -1 # Initialize with -1 for random

# --- Model Loading ---
def load_auraflow_pipeline():
    global pipeline
    if pipeline is None:
        print(f"Loading AuraFlow model: {MODEL_NAME} to {DEVICE} with {TORCH_DTYPE}...")
        try:
            pipeline_args = {"cache_dir": MODEL_FOLDER, "torch_dtype": TORCH_DTYPE}
            if VARIANT:
                pipeline_args["variant"] = VARIANT

            pipeline = AuraFlowPipeline.from_pretrained(MODEL_NAME, **pipeline_args)

            if DEVICE.startswith("cuda"):
                print("Enabling model CPU offload for lower VRAM usage...")
                pipeline.enable_model_cpu_offload() # Key for low VRAM
            else:
                pipeline.to(DEVICE) # Move to CPU if not using CUDA offload

            print("AuraFlow model loaded successfully.")
        except Exception as e:
            print(f"Error loading AuraFlow model: {e}")
            pipeline = None # Ensure pipeline is None if loading failed
            raise # Re-raise the exception to notify the user via Gradio
    return pipeline

# --- Core Generation Logic ---
def generate_image(prompt: str, width: int, height: int, num_inference_steps: int, seed: int, guidance_scale: float, progress=gr.Progress(track_tqdm=True)):
    global last_seed, pipeline

    if pipeline is None:
        # This could happen if the initial load failed.
        gr.Error("Model is not loaded. Please check console logs and restart the app.")
        return None, "Error: Model not loaded.", -1, "Error"


    current_seed = int(seed)
    if current_seed == -1:
        current_seed = torch.randint(0, 2**32 - 1, (1,)).item()
    last_seed = current_seed # Store the actual seed used

    generator = torch.Generator(device="cpu").manual_seed(current_seed) # Generator on CPU for reproducibility

    status_message = "Generating..."
    try:
        print(f"Generating image with seed: {current_seed}")
        pil_image = pipeline(
            prompt=prompt,
            width=width,
            height=height,
            num_inference_steps=num_inference_steps,
            generator=generator,
            guidance_scale=guidance_scale,
        ).images[0]

        # Sanitize prompt for filename (limit length)
        safe_prompt_segment = sanitize_filename(prompt[:50] if prompt else "auraflow_img")
        if not safe_prompt_segment.strip(): # Handle empty or space-only prompts
            safe_prompt_segment = "auraflow_img"
        
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{safe_prompt_segment}_{current_seed}_{unique_id}.png"
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        
        pil_image.save(filepath, 'PNG')
        status_message = f"Image saved as: {filepath}"
        print(status_message)

        # Clear VRAM cache if on CUDA
        if DEVICE.startswith("cuda"):
            torch.cuda.empty_cache()
        gc.collect()

        return pil_image, current_seed, status_message

    except Exception as e:
        print(f"Error during image generation: {e}")
        import traceback
        traceback.print_exc()
        status_message = f"Error: {str(e)}"
        return None, current_seed, status_message


# --- UI Helper Functions ---
def reset_seed_value():
    return -1

def reuse_last_seed_value():
    global last_seed
    return last_seed if last_seed is not None else -1

# --- Gradio Interface ---
# Attempt to load the model at startup
# This way, any loading errors are caught early, and the first generation isn't slow.
try:
    load_auraflow_pipeline()
except Exception as e:
    print(f"Failed to load model on startup: {e}. The app might not function correctly.")
    # Gradio will still launch, but generation will fail until model is loaded.

# Using a soft theme for a modern look. You can try others like gr.themes.Glass()
theme = gr.themes.Soft(
    primary_hue=gr.themes.colors.purple,
    secondary_hue=gr.themes.colors.orange,
    neutral_hue=gr.themes.colors.gray,
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
).set(
    # Further fine-tuning of the theme if needed
    # button_primary_background_fill="*primary_500",
    # button_primary_background_fill_hover="*primary_400",
)

with gr.Blocks(theme=theme, css="""
    .gradio-container { background-color: #f7f7f7; } /* Light background for the page */
    .small-button { /* For seed buttons */
        min-width: 0 !important;
        width: 3em; /* Slightly wider for better emoji display */
        height: 3em; /* Match textbox height if possible */
        padding: 0.25em !important;
        line-height: 1;
        font-size: 1.2em; /* Make emoji bigger */
        align-self: end; /* Align with bottom of textbox */
        margin-left: 0.5em !important;
    }
    #seed_row .gr-form { /* Target the form containing the number input and buttons */
        display: flex;
        align-items: flex-end; /* Align items to the bottom */
    }
    #seed_row .gr-number { /* Target number input specifically */
        flex-grow: 1; /* Allow number input to take available space */
    }
    .gr-group { /* Style for groups/cards if used */
        border-radius: 12px !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05) !important;
        background-color: white !important; /* Card background */
        padding: 20px !important;
    }
    /* Ensure markdown headers are styled nicely by the theme or add custom styles */
    h1 { font-size: 2.5em !important; color: *primary_600 !important; text-align: center; margin-bottom: 0.5em !important; }
    .gr-markdown p { font-size: 1.1em; color: *neutral_600; text-align: center; margin-bottom: 1.5em; }
""") as demo:

    gr.Markdown("# AuraFlow ✨ Image Generation")
    gr.Markdown("Experience the power of AuraFlow, the largest Apache-licensed open-source image generation model. This UI is designed to be sleek and VRAM-friendly.")

    with gr.Row():
        with gr.Column(scale=2, min_width=400): # Control Panel
            with gr.Group():
                gr.Markdown("### 🎨 Generation Settings")
                prompt_input = gr.Textbox(
                    label="Prompt",
                    placeholder="e.g., A stunning fantasy landscape, castles in the sky, digital art",
                    lines=3
                )
                
                with gr.Row():
                    width_slider = gr.Slider(label="Width", minimum=256, maximum=2048, value=1024, step=64) # Default to common sizes
                    height_slider = gr.Slider(label="Height", minimum=256, maximum=2048, value=1024, step=64)

                steps_slider = gr.Slider(label="Inference Steps", minimum=4, maximum=100, value=28, step=1) # AuraFlow can work with fewer steps
                guidance_slider = gr.Slider(label="Guidance Scale (CFG)", minimum=0.0, maximum=20.0, value=3.0, step=0.1) # Typical CFG for AuraFlow

                with gr.Row(elem_id="seed_row"): # For CSS targeting
                    seed_input = gr.Number(label="Seed (-1 for random)", value=-1, precision=0, interactive=True)
                    # MODIFIED: Removed tooltip argument
                    random_seed_button = gr.Button("🎲", elem_classes="small-button")
                    # MODIFIED: Removed tooltip argument
                    reuse_seed_button = gr.Button("♻️", elem_classes="small-button")

                generate_button = gr.Button("Generate Image", variant="primary", scale=2)

        with gr.Column(scale=3, min_width=500): # Output Panel
            with gr.Group():
                gr.Markdown("### 🖼️ Generated Image")
                output_image = gr.Image(label="Output", type="pil", interactive=False, show_download_button=True, show_share_button=True)
                with gr.Accordion("Generation Details", open=False):
                    generated_seed_output = gr.Textbox(label="Used Seed", interactive=False)
                    status_output = gr.Textbox(label="Status / Filename", interactive=False, lines=2)

    # --- Event Handling ---
    generate_button.click(
        fn=generate_image,
        inputs=[prompt_input, width_slider, height_slider, steps_slider, seed_input, guidance_slider],
        outputs=[output_image, generated_seed_output, status_output],
        api_name="generate_image" # For API access if needed
    )

    random_seed_button.click(fn=reset_seed_value, inputs=[], outputs=seed_input)
    reuse_seed_button.click(fn=reuse_last_seed_value, inputs=[], outputs=seed_input)

    # Example of how to set default values from sliders to prompt (if desired)
    # def update_prompt_with_size(width, height):
    #     return f"A photo of X, {width}x{height}" # Example
    # width_slider.release(update_prompt_with_size, [width_slider, height_slider], prompt_input)
    # height_slider.release(update_prompt_with_size, [width_slider, height_slider], prompt_input)

# --- Launch ---
if __name__ == "__main__":
    # The queue helps manage multiple requests if the app is busy
    # max_size=1 might be better for low VRAM to avoid OOM if multiple heavy jobs queue up
    demo.queue(max_size=1, default_concurrency_limit=1) 
    demo.launch(debug=True, share=False) # Set share=True to get a public link (careful with resources)
