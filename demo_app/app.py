import os
import sys
import gc
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import tempfile
import traceback
import torch

# Try to import psutil, fallback if not available
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("Warning: psutil not installed. Memory usage will not be available.")

# Add RoboBrain2.0 to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'RoboBrain2.0'))
from inference import UnifiedInference

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# Initialize model globally
model_instance = None
current_model_id = "BAAI/RoboBrain2.0-7B"

def get_memory_usage():
    """Get current memory usage in MB."""
    if not PSUTIL_AVAILABLE:
        return "N/A (psutil not installed)"
    try:
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        return f"{memory_info.rss / 1024 / 1024:.2f}"  # Convert to MB
    except Exception as e:
        print(f"Error getting memory: {e}")
        return "N/A"

def get_device():
    """Get the device being used by the model."""
    try:
        if torch.cuda.is_available():
            return "CUDA (GPU)"
        elif torch.backends.mps.is_available():
            return "MPS (Apple Silicon)"
        else:
            return "CPU"
    except Exception as e:
        print(f"Error getting device: {e}")
        return "Unknown"

def load_model(model_id="BAAI/RoboBrain2.0-7B"):
    """Load the RoboBrain model."""
    global model_instance, current_model_id
    try:
        print(f"Loading RoboBrain model: {model_id}")
        # Unload previous model if exists
        if model_instance is not None:
            print("Unloading previous model...")
            del model_instance
            gc.collect()
        
        model_instance = UnifiedInference(
            model_id=model_id,
            device_map="auto"
        )
        current_model_id = model_id
        print(f"Model loaded successfully: {model_id}")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        traceback.print_exc()
        model_instance = None
        return False

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/inference', methods=['POST'])
def api_inference():
    """Handle inference requests."""
    try:
        # Check if model is loaded
        if model_instance is None:
            return jsonify({'error': 'Model not loaded. Please load a model first.'}), 500
        
        # Get form data
        prompt = request.form.get('prompt', '').strip()
        task = request.form.get('task', 'general')
        temperature = float(request.form.get('temperature', 0.7))
        
        if not prompt:
            return jsonify({'error': 'Please enter a prompt.'}), 400
        
        # Check if image is uploaded
        if 'image' not in request.files:
            return jsonify({'error': 'Please upload an image.'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'Please select a file.'}), 400
        
        if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            return jsonify({'error': 'Please upload a valid image file (JPG, PNG, BMP, GIF).'}), 400
        
        # Save temporary image
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_path)
        
        try:
            # Run inference
            result = model_instance.inference(
                text=prompt,
                image=temp_path,
                task=task,
                do_sample=True,
                temperature=temperature
            )
            
            return jsonify({
                'success': True,
                'result': result,
                'task': task
            })
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    except Exception as e:
        error_msg = f"Error during inference: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return jsonify({'error': error_msg}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Check if model is loaded."""
    return jsonify({
        'status': 'ready' if model_instance is not None else 'loading',
        'model_loaded': model_instance is not None,
        'model_id': current_model_id
    })

@app.route('/api/stats', methods=['GET'])
def stats():
    """Get model statistics."""
    try:
        memory_usage = get_memory_usage()
        if isinstance(memory_usage, str) and "N/A" in memory_usage:
            memory_str = memory_usage
        else:
            memory_str = f'{float(memory_usage):.2f} MB'
        
        device = get_device()
        model_loaded = model_instance is not None
        model_id = current_model_id if model_instance is not None else 'None'
        
        return jsonify({
            'model_loaded': model_loaded,
            'model_id': model_id,
            'memory_usage': memory_str,
            'device': device,
            'success': True
        })
    except Exception as e:
        print(f"Error in stats endpoint: {e}")
        traceback.print_exc()
        return jsonify({
            'model_loaded': model_instance is not None,
            'model_id': current_model_id if model_instance is not None else 'None',
            'memory_usage': 'N/A',
            'device': 'Unknown',
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/load-model', methods=['POST'])
def load_model_endpoint():
    """Load a specific model."""
    try:
        data = request.get_json()
        model_id = data.get('model_id')
        
        if not model_id:
            return jsonify({'error': 'Model ID is required'}), 400
        
        success = load_model(model_id)
        
        if success:
            memory_usage = get_memory_usage()
            if isinstance(memory_usage, str) and "N/A" in memory_usage:
                memory_str = memory_usage
            else:
                memory_str = f'{float(memory_usage):.2f} MB'
            
            return jsonify({
                'success': True,
                'message': f'Model {model_id} loaded successfully',
                'model_id': model_id,
                'device': get_device(),
                'memory_usage': memory_str
            })
        else:
            return jsonify({'error': 'Failed to load model'}), 500
    
    except Exception as e:
        error_msg = f"Error loading model: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        return jsonify({'error': error_msg}), 500

@app.route('/api/unload-model', methods=['POST'])
def unload_model_endpoint():
    """Unload the current model."""
    global model_instance
    try:
        if model_instance is None:
            return jsonify({'error': 'No model is currently loaded'}), 400
        
        del model_instance
        model_instance = None
        gc.collect()
        
        memory_usage = get_memory_usage()
        if isinstance(memory_usage, str) and "N/A" in memory_usage:
            memory_str = memory_usage
        else:
            memory_str = f'{float(memory_usage):.2f} MB'
        
        return jsonify({
            'success': True,
            'message': 'Model unloaded successfully',
            'memory_usage': memory_str
        })
    
    except Exception as e:
        error_msg = f"Error unloading model: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    print("Starting RoboBrain Demo App...")
    print(f"Loading model on startup: {current_model_id}")
    
    success = load_model(current_model_id)
    if success:
        print(f"✓ Model loaded successfully: {current_model_id}")
    else:
        print(f"✗ Failed to load model: {current_model_id}")
        print("The app will start but you'll need to load a model manually.")
    
    print("Starting Flask server on http://localhost:5000")
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
