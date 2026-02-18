# RoboBrain Demo App

A Flask web application for running RoboBrain 2.0 inference with a user-friendly interface.

## Features

- **Image Upload**: Upload images for analysis
- **Prompt Input**: Enter custom prompts or questions
- **Multiple Task Types**: 
  - General Question
  - Pointing
  - Affordance
  - Trajectory
  - Grounding
- **Adjustable Temperature**: Control the creativity of responses
- **Real-time Model Status**: See when the model is ready
- **Beautiful UI**: Modern, responsive web interface

## Setup

### 0. Environment Setup
# Robobrain 2.0 steps on Mac

Setup virtual environment: 
```bash
pyenv install 3.10
pyenv virtualenv 3.10 robobrain2

pyenv activate robobrain2
```

Install all requirements:
```bash
pip install -r requirements.txt
pip install transformers
pip install torchvision
pip install accelerate
```

Make sure to login to huggingface account using:
```bash
hf auth login
```

Then make sure you go to the hugging face repositories such as robobrain2.0 or robobrain and enable access to the repo for this account.


### 1. Install Dependencies

```bash
cd demo_app
pip install -r requirements.txt
```

### 2. Run the App

```bash
python app.py
```

The app will start on `http://localhost:5000`

### First Run
- The model will load on startup (may take 1-2 minutes)
- Once loaded, you'll see the status indicator turn green
- You can then start running inferences

## Usage

1. **Upload an Image**: Click "Upload Image" and select an image file (JPG, PNG, BMP, or GIF)
2. **Enter a Prompt**: Type your question or request about the image
3. **Select Task Type** (optional): Choose the type of task (defaults to "General Question")
4. **Adjust Temperature** (optional): Control response creativity (0 = deterministic, 1 = creative)
5. **Run Inference**: Click the "Run Inference" button
6. **View Results**: The model's response will appear below the form

## Task Types

- **General Question**: Ask any question about the image
- **Pointing**: Identify locations/points in the image
- **Affordance**: Predict affordance areas for robot manipulation
- **Trajectory**: Predict trajectory points for robot movement
- **Grounding**: Find regions matching a text description

## System Requirements

- Python 3.8+
- 16GB+ RAM (recommended)
- For optimal performance on Mac, use Apple Silicon (M1/M2/M3)

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- GIF (.gif)
- Maximum file size: 50MB

## Architecture

- **Backend**: Flask REST API
- **Frontend**: HTML5 + CSS3 + Vanilla JavaScript
- **Model**: RoboBrain 2.0 (BAAI/RoboBrain2.0-7B)
- **Device**: Auto-detects CUDA, MPS (Mac), or CPU

## Troubleshooting

### Model takes a long time to load
- The first load downloads the model from Hugging Face (~15GB)
- Subsequent runs will be faster as the model is cached

### Out of memory error
- Reduce the number of open applications
- The app uses `device_map="auto"` for optimal memory management
- On Mac, it automatically uses Apple Silicon's GPU if available

### Port 5000 already in use
- Change the port in `app.py`: `app.run(..., port=5001)`

## Notes

- The app runs in debug mode by default (auto-reloads on code changes)
- For production use, disable debug mode and use a production WSGI server
- Temporary image files are automatically cleaned up after processing
