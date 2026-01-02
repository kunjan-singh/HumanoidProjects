# RoboBrain Demo App

A Flask web application for running RoboBrain 2.0 inference with a user-friendly interface.
<img width="1520" height="1820" alt="image" src="https://github.com/user-attachments/assets/4d6e255c-0f5d-452e-9847-b8f4f615f18b" />

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

This will show output like:

<img width="740" height="399" alt="image" src="https://github.com/user-attachments/assets/5affdca2-ca86-406b-88f6-8935f0912c39" />

The app will start on `http://localhost:5000`

### First Run
- The model will load on startup (may take 1-2 minutes)
- Once loaded, you'll see the status indicator turn green
- You can then start running inferences

<img width="1518" height="1385" alt="image" src="https://github.com/user-attachments/assets/ab9f2896-b4ca-46e8-ae9b-4973b193362e" />


## Usage

1. **Upload an Image**: Click "Upload Image" and select an image file (JPG, PNG, BMP, or GIF)
2. **Enter a Prompt**: Type your question or request about the image
3. **Select Task Type** (optional): Choose the type of task (defaults to "General Question")
4. **Adjust Temperature** (optional): Control response creativity (0 = deterministic, 1 = creative)
5. **Run Inference**: Click the "Run Inference" button
6. **View Results**: The model's response will appear below the form

<img width="1585" height="2585" alt="image" src="https://github.com/user-attachments/assets/2abf0270-954d-4853-99aa-fbad1d1c6b78" />


## Visualization Tools

Use the outputs from the model inference and visualize on your images to betetr understand the output.

### Bounding Box 

The input should be in the format: [574, 236, 622, 306]

<img width="1537" height="1758" alt="image" src="https://github.com/user-attachments/assets/8265db36-a744-4057-b747-abf2fecacdd0" />


### Points Visualization

The input should be a list of points in the format: [(400, 309), (357, 268), (311, 236), ...etc]

<img width="781" height="835" alt="image" src="https://github.com/user-attachments/assets/0e86420f-6c42-44bf-8be5-19f92131fb12" />




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
