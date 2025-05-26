# AuraFLooow ✨  
_Image Generation Without the VRAM Meltdown_

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

So you've got a mid-range GPU, an artistic itch, and a mild aversion to ComfyUI’s 400-node spaghetti graphs? Welcome. You’re in the right place — **AuraFLooow** is your one-click, low-fuss web UI for running the AuraFlow image model without setting your rig on fire.

This isn't a feature dump of ComfyUI, and it doesn’t want to be. Think of it as “image generation on a diet” — built for people who just want to type stuff like _“cyberpunk goose in a trench coat”_ and see it rendered, without reading a TensorRT whitepaper first.

---

## 🧐 What *Is* This?

AuraFLooow is a lightweight web app using Gradio that wraps around the excellent [`fal/AuraFlow-v0.3`](https://huggingface.co/fal/AuraFlow-v0.3) text-to-image model. It’s for those who:

- Own a GPU that didn’t cost more than their car.
- Prefer sliders over shell scripts.
- Want to run locally (yes, even offline — no "cloud credits" required).
- Think AI art should be simple enough that your mum could use it. And possibly does.

---

## 🎯 Core Features (aka “What It Actually Does”)

- Generates images from text prompts with AuraFlow.
- Resize image output — up to AuraFlow’s very generous limits.
- Tweak steps, CFG scale, and seed (or roll the dice).
- Saves your creations to an `output/` folder automatically.
- Dark-mode-ish modern UI with buttons, not bash.
- Tries very hard not to gobble up all your VRAM, with CPU offloading via `diffusers`.

---

## 🧠 System Requirements

### 🧱 Hardware
- A **dedicated NVIDIA GPU** with **at least 6GB of VRAM**.
  - *Can it run on CPU?* Yes. Should it? Not unless you enjoy existential waiting.
  - *AMD GPUs?* Technically possible. But we don’t officially support those shenanigans — `diffusers` + ROCm is a whole separate odyssey.

### 💿 Software
- **Python 3.9+**  
- **Pip** (comes with Python, usually)
- **Git** (optional, unless you enjoy downloading ZIPs manually)

### 🧙 Required Python Packages

Everything you need is in `requirements.txt`, including:
- `diffusers`, `torch`, `transformers`, `gradio`, `accelerate`
- Plus a few supporting roles: `Pillow`, `protobuf`, `safetensors`, etc.

---

## 🛠️ Installation – Or “How Not to Break It”

### 1. Clone (or Download) the Repository
**Option A – Git enjoyers:**
```bash
git clone https://github.com/Raxephion/AuraFlooow.git AuraFLooow
cd AuraFLooow
```

**Option B – ZIP warriors:**
Download the ZIP from GitHub, extract it, and `cd` into the folder.

### 2. Create a Virtual Environment
Because isolation is healthy (for Python projects, anyway):
```bash
python -m venv venv
```

### 3. Activate It
**Windows:**
```bash
venv\Scripts\activate
```
**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
Yes, PyTorch is big. Go make coffee.

---

## 🚀 Running the App

After installing, fire it up:

```bash
python app.py
```

(Windows users can just double-click `run.bat` if the command line makes them itchy.)

The **first run** will download the model (10–15GB, depending on version). Don’t panic — it’s only slow once. After that, it’s cached.

Once you see something like:
```
Running on local URL: http://127.0.0.1:7860
```
pop that into your browser and enjoy the ride.

---

## 🧩 About the Model – AuraFlow v0.3

AuraFlow v0.3 is a clever little beast — flow-based, open-source, and fine-tuned for aesthetics. Think of it as the model equivalent of a gallery curator with a GPU.

> _“Supports multiple aspect ratios, 1536px limits, and state-of-the-art scores on GenEval.”_  
> – paraphrased from [fal.ai](https://fal.ai/blog/auraflow)

Massive kudos to the team: `@cloneofsimo`, `@isidentical`, and others who actually understand diffusion math.

---

## 🧯 Common Problems (and Solutions That Don’t Involve Screaming)

### 🔥 CUDA Out of Memory?
- Lower your image resolution.
- Close other GPU-intensive apps (yes, even Chrome).
- 6GB VRAM is the sweet spot — below that, expect hiccups.
- CPU offload helps, but it's not witchcraft.

### 🐢 First Run is Slow?
That’s the model downloading. It’s not stuck. Just slow. Blame your ISP.

### ❌ Protobuf Errors or Missing Models?
Double-check that you’re installing packages *inside* the virtual environment.

### 🧪 Gradio `tooltip` errors?
We removed `tooltip` for broader compatibility. If you’re using a newer Gradio version and really want it back — go ahead and hack it in.

---

## 🔁 Changing the Model

Default model is `fal/AuraFlow-v0.3`. To swap it:

1. Open `app.py`
2. Look for `MODEL_NAME = "fal/AuraFlow-v0.3"`
3. Change it to your preferred model (as long as it’s AuraFlow-compatible)

You can also load models locally if they’re in your Hugging Face cache.

---

## 🙃 Final Words (and a Gentle Disclaimer)

This is a side project. It’s not bulletproof. It’s not enterprise-ready. But it works, and it's meant to get you creating without the overhead of ComfyUI or the GPU of a data center.

Please:
- Use ethically.
- Don’t prompt weird illegal stuff.
- Credit the original model creators.
- Don’t send support requests to NVIDIA when this breaks.

---

Happy prompting! 🎨  
— *Team Probably Didn’t Sleep Enough*
