from flask import Flask, render_template, request, redirect, url_for
from mission_core import MissionState, launch_step, cruise_step, landing_step, collect_data, return_home # <-- Note the full import list

# Initialize the Flask application
app = Flask(__name__)

# Initialize the mission state globally so it persists across user actions
mission = MissionState()

@app.route('/', methods=['GET', 'POST'])
def home():
    """Displays the current mission status and controls."""
    # This route handles the main view
    return render_template('index.html', state=mission.get_current_state())

@app.route('/launch', methods=['POST'])
def launch():
    """Handles the user's input for the launch step."""
    
    # 1. Get user input from the HTML form
    try:
        # We assume the form field is named 'thrust_power'
        thrust = int(request.form['thrust_power'])
    except ValueError:
        # Simple error handling for bad input
        thrust = -1 

    # 2. Execute the mission logic (from mission_core.py)
    launch_step(mission, thrust)
    
    # 3. Redirect back to the home page to display the new state
    return redirect(url_for('home'))

@app.route('/cruise', methods=['POST'])
def cruise():
    """Handles the step-based action for the cruise phase."""
    
    # 1. Execute the mission logic (from mission_core.py)
    cruise_step(mission)
    
    # 2. Redirect back to the home page to display the new state
    return redirect(url_for('home'))

@app.route('/land', methods=['POST'])
def land():
    """Handles the user's input for the landing retro-burn."""
    
    # 1. Get user input from the HTML form (retro_burn_duration_s)
    try:
        duration = int(request.form['burn_duration'])
    except ValueError:
        duration = -1 
        
    # 2. Execute the mission logic (from mission_core.py)
    landing_step(mission, duration)
    
    # 3. Redirect back to the home page
    return redirect(url_for('home'))


@app.route('/collect', methods=['POST'])
def collect():
    """Handles the action to collect data on the surface."""
    
    # Execute the mission logic (from mission_core.py)
    collect_data(mission)
    
    # Redirect back to the home page
    return redirect(url_for('home'))


@app.route('/return', methods=['POST'])
def return_ship():
    """Handles the final return home sequence."""
    
    # Execute the mission logic (from mission_core.py)
    return_home(mission)
    
    # Redirect back to the home page
    return redirect(url_for('home'))


# --- The Server Start Block (MUST be at the very end) ---
if __name__ == '__main__':
    # Setting debug=True restarts the server automatically when you save changes
    app.run(debug=True)