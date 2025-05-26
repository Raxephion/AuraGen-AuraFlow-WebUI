# AuraFlow Local ✨ - Image Gen on a Diet (VRAM-wise!)

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Tired of image generators that demand a king's ransom in VRAM? Want to run the rather brilliant AuraFlow locally without your GPU staging a protest? Well, you've stumbled into the right digital alleyway!

This little app is your friendly neighborhood AuraFlow interface, designed to be (relatively) kind to your graphics card, especially if you're rocking around **6GB of VRAM**. It's built for folks who prefer clicking buttons to wrestling with code, and for those who just want to make pretty (or hilariously bizarre) pictures without a PhD in Machine Learning.

## What's This All About, Then?

This project provides a simple Gradio web UI to generate images using the powerful **AuraFlow text-to-image model** (`fal/AuraFlow-v0.3` by default). The key goals are:

*   **Low(ish) VRAM Usage:** Optimized to run on GPUs with around 6GB VRAM by enabling CPU offloading. Your mileage may vary, but we're trying!
*   **Easy Installation:** Get up and running with minimal fuss. If you can follow a recipe, you can (probably) do this.
*   **Local Generation:** Keep your prompts and creations on your own machine.
*   **User-Friendly Interface:** No need to stare at a command line all day. Sliders and buttons, oh my!
*   **Fast(ish) Generation:** AuraFlow is pretty zippy for its size, and this app tries not to slow it down.

## Features (Or, What Cool Things Can It Do?)

*   Generate images from text prompts using AuraFlow.
*   Adjust image width and height (up to AuraFlow's limits, which are quite generous!).
*   Control inference steps and guidance scale (CFG).
*   Set a specific seed for reproducible images or go wild with a random one.
*   Saves your masterpieces to an `output` folder.
*   A rather fetching (if we do say so ourselves) modern UI theme.
*   Attempts to be VRAM-friendly by offloading model parts to CPU when not in use (thanks, `diffusers`!).

## Requirements (The Not-So-Secret Ingredients)

### Hardware:
*   A **dedicated NVIDIA GPU** is highly recommended, ideally with **at least 6GB of VRAM**.
    *   *Can it run on CPU?* Yes, the script will fall back to CPU if no CUDA device is found. Expect it to be significantly slower (think continental drift, but for pixels).
    *   *AMD GPUs?* While `diffusers` and PyTorch are improving ROCm support, this guide primarily focuses on NVIDIA CUDA.

### Software:
*   **Python** (version 3.9 or higher recommended). You can get it from [python.org](https://www.python.org/downloads/). Make sure to check "Add Python to PATH" during installation if you're on Windows.
*   **Pip** (usually comes with Python).
*   **Git** (optional, but useful for cloning this repository). Get it from [git-scm.com](https://git-scm.com/downloads).

### Python Libraries:
The necessary Python libraries are listed in `requirements.txt`. The main cast includes:
*   `diffusers`
*   `torch` (and its companions `torchvision`, `torchaudio`)
*   `transformers`
*   `accelerate`
*   `gradio`
*   `Pillow`
*   `pathvalidate`
*   `protobuf`
*   `safetensors`

## Installation & Setup (The Not-So-Scary Part)

Alright, let's get this show on the road.

1.  **Get the Code:**
    *   **Option A (with Git):** Open your terminal/command prompt and run:
        ```bash
        git clone https://github.com/Raxephion/AuraFlooow.git AuraFlowLocal
        cd AuraFlowLocal
        ```
    *   **Option B (Download ZIP):** Download the ZIP file from `https://github.com/Raxephion/AuraFlooow/archive/refs/heads/main.zip` (or your default branch name), extract it somewhere memorable, and navigate into that folder (`AuraFlooow-main` or similar) using your terminal.

2.  **Create a Virtual Environment (Highly Recommended!):**
    This keeps things tidy and avoids conflicts with other Python projects. It's like giving your app its own little apartment.
    Open your terminal in the project directory (`AuraFlowLocal` or `AuraFlooow-main`) and run:
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    *   **Windows:**
        ```bash
        venv\Scripts\activate
        ```
        (Your prompt should now start with `(venv)`)
    *   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
        (Your prompt should now start with `(venv)`)

4.  **Install the Magic Spells (Dependencies):**
    With your virtual environment active, run:
    ```bash
    pip install -r requirements.txt
    ```
    This might take a few minutes, as it's downloading some hefty libraries like PyTorch. Grab a cup of tea.

## Running the App (Let the Magic Happen!)

Once everything is installed:

1.  Make sure your virtual environment is still active. If not, reactivate it (see step 3 in Installation).
2.  In your terminal, from the project directory, run:
    ```bash
    python app.py
    ```
    (Or, if you're using the `run.bat` file on Windows, simply double-click it.)

3.  **Patience, Young Padawan:** The very first time you run this, `diffusers` will download the AuraFlow model files (which are quite large, around 10-15GB for the `fal/AuraFlow-v0.3` fp16 version). This will take a while depending on your internet speed. Subsequent runs will be much faster as the model will be cached locally in the `models` folder.
    You'll see progress bars in the terminal for the download.

4.  Once the model is loaded and the UI is ready, you'll see a message like:
    `Running on local URL: http://127.0.0.1:7860` (the port number might vary).

5.  Open that URL in your web browser, and you should be greeted by the AuraFlow Local interface!

## A Note on AuraFlow (The Brains of the Operation)

This application uses **AuraFlow v0.3** by default, a fully open-sourced, flow-based text-to-image generation model from `fal.ai`.
As they say on their Hugging Face page:
> "Compared to AuraFlow-v0.2, the model is fine-tuned on more aesthetic datasets and now supports various aspect ratio, (now width and height up to 1536 pixels). This model achieves state-of-the-art results on GenEval."

It's a fantastic piece of engineering!
**Huge credits to:** @cloneofsimo, @isidentical, and the researchers whose prior work laid the foundation. You can read more on the [AuraFlow v0.3 Hugging Face page](https://huggingface.co/fal/AuraFlow-v0.3) and their [blog post](https://fal.ai/blog/auraflow).

## Troubleshooting & Notes

*   **"CUDA out of memory" errors:**
    *   Try reducing the image width/height.
    *   Ensure no other GPU-heavy applications are running.
    *   This app is designed for ~6GB VRAM. If you have less, it might struggle with larger images.
    *   The `enable_model_cpu_offload()` feature helps a lot, but it's not magic!
*   **Slow on first run:** This is likely the model download. Check your terminal.
*   **Model not loading / `protobuf` error:** Ensure you've installed all requirements in your *active* virtual environment (especially `pip install protobuf`).
*   **Gradio `tooltip` error:** This script has removed the `tooltip` argument for broader compatibility. If you want tooltips and have a newer Gradio version, you can try adding them back.

## Modifying the Model

The script is set to use `fal/AuraFlow-v0.3`. If you want to experiment with a different AuraFlow-compatible model (like `cozy-creator/aura-flow-fp16-version` if you have it downloaded and prefer it), you can change the `MODEL_NAME` variable at the top of `app.py`. Make sure the model is compatible with `AuraFlowPipeline`.

## Disclaimer

*   This is a community project provided as-is.
*   AuraFlow itself is a powerful model. Please use it responsibly and ethically.
*   Results can vary, and image generation is a bit of an art form. Experiment and have fun!

---
