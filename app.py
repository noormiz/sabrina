from flask import Flask, render_template, request, redirect, url_for, jsonify
from mission_core import MissionState, launch_step, cruise_step, landing_step, collect_data, return_home, EXOPLANETS # <-- Import necessary logic

# Initialize the Flask application
app = Flask(__name__)

# Initialize the mission state globally so it persists across user actions
mission = MissionState()

@app.route('/', methods=['GET'])
def home():
    """Displays the current mission status and controls."""
    state = mission.get_current_state()
    # Pass necessary planet data to the template for the selection screen
    return render_template('index.html', state=state, exoplanets=EXOPLANETS)

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
    # Setting debug=True restarts the server automatically when you save changes
    app.run(debug=True)