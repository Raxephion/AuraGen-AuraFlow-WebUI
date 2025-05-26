# NB: Project still being tested and files modified. 

# AuraFLooow ✨  
_Image Generation Without the VRAM Meltdown_

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

So you've got a mid-range GPU, an artistic itch, and a mild aversion to ComfyUI’s 400-node spaghetti graphs? Welcome. You’re in the right place — **AuraFLooow** is your one-click, low-fuss web UI for running the AuraFlow image model without setting your rig on fire.

This isn't a feature dump of ComfyUI, and it doesn’t want to be. Think of it as “image generation on a diet” — built for people who just want to type stuff like _“cyberpunk goose in a trench coat”_ and see it rendered, without reading a TensorRT whitepaper first.

---

## 🧐 What *Is* This?

AuraFLooow is a lightweight Gradio web app wrapping the [`fal/AuraFlow-v0.3`](https://huggingface.co/fal/AuraFlow-v0.3) image generation model. It’s for people who:

- Own a GPU that didn’t cost more than their car.
- Prefer sliders over shell scripts.
- Want to run locally (yes, even offline — no cloud nonsense).
- Think AI art should be simple enough your mum could use it. And maybe does.

---

## 🎯 Features

- Generates images from text prompts with AuraFlow.
- Output resolution control (up to AuraFlow’s 1536px ceiling).
- Steps, CFG scale, seed — tweak away.
- Auto-saves outputs to an `output/` folder.
- Simple, modern UI with no required brain damage.
- VRAM-friendly thanks to CPU offloading via `diffusers`.

---

## 🧠 System Requirements

### 🧱 Hardware
- **NVIDIA GPU** with **6GB+ VRAM**
- **AMD/Intel?** Possible, but not officially supported. You're on your own, brave soul.

### 💿 Software
- **Windows**
- **Python 3.9+**
- No other installations needed — we’ve got `.bat` scripts to automate the mess.

---

## ⚡ Quickstart (for Lazy but Genius People)

1. **Download the repo** (ZIP or Git).
2. **Double-click `install.bat`**  
   This will:
   - Create a virtual environment
   - Install all dependencies
3. **Double-click `launch.bat`**  
   This:
   - Activates the venv
   - Launches the web UI in your browser

Done. You’re generating. You're welcome.

---

## 🧩 About the Model – AuraFlow v0.3

AuraFlow v0.3 is a stylish little diffusion model that:
- Supports large images (up to 1536x1536)
- Uses flow-matching to keep things snappy
- Scores great on GenEval benchmarks

Built by the clever humans at [fal.ai](https://fal.ai/blog/auraflow). Props to `@cloneofsimo`, `@isidentical`, and their crew.

---

## 🧯 Troubleshooting

### CUDA Out of Memory?
- Lower the resolution.
- Close apps hogging the GPU (yes, even Chrome).
- CPU offload helps, but magic it ain't.

### First Launch is Slow?
That’s the model downloading. Give it time. It’s ~10–15GB. Coffee break.

### Python Errors?
Try running `install.bat` again to reset the venv and dependencies.

---

## 🔁 Want to Use a Different Model?

1. Open `app.py`
2. Change this line:
```python
MODEL_NAME = "fal/AuraFlow-v0.3"
```
…to whatever Hugging Face model you want (as long as it's compatible with `diffusers`).

---

## 🙃 Final Words

AuraFLooow is for creators, tinkerers, and burnt-out ComfyUI users who just want to make some dang art. It's not built for production. It’s not trying to be everything. It’s just meant to work — simply, and well.

Use responsibly. Prompt ethically. And don’t call us if your VRAM explodes.

---

Happy prompting! 🎨  
— *Team Definitely Slept at Some Point*
