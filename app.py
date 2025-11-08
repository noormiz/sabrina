import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from mission_core import MissionState, launch_step, cruise_step, landing_step, collect_data, return_home, EXOPLANETS # <-- Import necessary logic

# Initialize the Flask application
app = Flask(__name__)

# Get Gemini API key from environment variable (more secure than hardcoding)
# Fallback to hardcoded key if env var not set (for development only)
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyAx_kgy_uYyresWInzbHRHB_pQvmu6bEv0')

# Initialize the mission state globally so it persists across user actions
mission = MissionState()

@app.route('/', methods=['GET'])
def home():
    """Displays the current mission status and controls."""
    # Ensure mission is in SELECTION state if no planet is selected or if in terminal state
    if mission.target_planet_data is None:
        # If no planet selected, always show selection screen
        if mission.status != 'SELECTION':
            mission.__init__()  # Reset to SELECTION state
    elif mission.status in ['SUCCESS', 'FAILURE']:
        # Keep terminal states as-is (user can see results)
        pass
    
    state = mission.get_current_state()
    # Pass necessary planet data and API key to the template for the selection screen
    return render_template('index.html', state=state, exoplanets=EXOPLANETS, gemini_api_key=GEMINI_API_KEY)

@app.route('/select_planet', methods=['POST'])
def select_planet_route():
    """Handles the user selecting a planet, setting the mission target."""
    planet_key = request.form.get('planet_key')
    if planet_key and planet_key in EXOPLANETS:
        mission.__init__() # Reset mission state completely
        mission.set_target(planet_key)
    return redirect(url_for('home'))

@app.route('/launch', methods=['POST'])
def launch():
    """Handles the user's input for the launch step (TWR)."""
    
    # 1. Get user input from the HTML form (TWR value, which is float)
    try:
        twr = float(request.form['thrust_twr'])
    except (ValueError, TypeError):
        twr = 0.0 # Will cause an immediate failure

    # 2. Execute the mission logic (from mission_core.py)
    result_message = launch_step(mission, twr)
    
    # The template will display the result message, status, and error code automatically
    return redirect(url_for('home'))

@app.route('/cruise', methods=['POST'])
def cruise():
    """Handles the step-based action for the cruise phase, including mid-course burn."""
    
    # 1. Get user input for the burn duration
    try:
        burn_duration = int(request.form.get('burn_duration', 0))
    except (ValueError, TypeError):
        burn_duration = 0
        
    # 2. Execute the mission logic (from mission_core.py)
    cruise_step(mission, burn_duration)
    
    return redirect(url_for('home'))

@app.route('/land', methods=['POST'])
def land():
    """Handles the user's input for the landing retro-burn duration."""
    
    try:
        duration = int(request.form.get('burn_duration', 0))
    except (ValueError, TypeError):
        duration = 0
        
    landing_step(mission, duration)
    return redirect(url_for('home'))


@app.route('/collect', methods=['POST'])
def collect():
    """Handles the action to collect data on the surface."""
    collect_data(mission)
    return redirect(url_for('home'))


@app.route('/return_home', methods=['POST'])
def return_ship():
    """Handles the final return home sequence."""
    return_home(mission)
    return redirect(url_for('home'))

@app.route('/reset', methods=['GET', 'POST'])
def reset_mission():
    """Resets the mission to selection state."""
    mission.__init__()  # Reset to initial SELECTION state
    return redirect(url_for('home'))


# --- API Endpoint for the Client-Side AI Tutor ---
# This is where the HTML/JS front-end will ask for AI feedback
@app.route('/api/ai_prompt', methods=['POST'])
def ai_prompt():
    """Mocks a backend for the AI tutor to provide context to the frontend logic."""
    data = request.json
    
    # In a real app, you would send data['query'] to the Gemini API here.
    # We only need to provide the necessary context back to the frontend JS.
    
    context = {
        "status": mission.status,
        "error_code": mission.error_code,
        "planet": mission.target_planet_data["name"] if mission.target_planet_data else "Unknown"
    }

    return jsonify(context), 200


if __name__ == '__main__':
    # Check if API key is set
    if not GEMINI_API_KEY:
        print("WARNING: GEMINI_API_KEY environment variable is not set!")
        print("   The AI tutor will not work. Set it with:")
        print("   $env:GEMINI_API_KEY='your_api_key_here'")
        print("   Or use: python start_server.ps1")
    else:
        print("Gemini API key loaded successfully!")
    
    # Setting debug=True restarts the server automatically when you save changes
    print("\nStarting Flask server...")
    print("Server will be available at: http://localhost:5000")
    print("Gemini API key loaded successfully!")
    print("=" * 50)
    app.run(debug=True, host='127.0.0.1', port=5000)

    # Akbar Code
