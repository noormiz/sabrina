import os # Akbar
import random
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from mission_core import MissionState, launch_step, cruise_step, landing_step, collect_data, return_home, EXOPLANETS, SPECTROSCOPY_ELEMENTS, get_spectroscopy_data, assess_atmosphere # <-- Import necessary logic

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'sabrina-space-mission-simulator-secret-key-2024')  # For session management

# Get Gemini API key from environment variable (more secure than hardcoding)
# Fallback to hardcoded key if env var not set (for development only)
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyDZPEoBU-gGTjiPrxzdfrCd6fWmson0dw8')

# Initialize the mission state globally so it persists across user actions
mission = MissionState()

def generate_space_name(name):
    """Generate a fun space-related name for the user."""
    titles = ['Commander', 'Captain', 'Astronaut', 'Pilot', 'Explorer', 'Navigator', 'Mission Specialist']
    suffixes = ['of the Stars', 'Stellar', 'Cosmic', 'Galactic', 'Nebula', 'Apollo', 'Voyager']
    
    # Use first name only
    first_name = name.split()[0] if name else 'Explorer'
    
    # Randomly choose a title and sometimes add a suffix
    title = random.choice(titles)
    if random.random() > 0.5:  # 50% chance to add suffix
        suffix = random.choice(suffixes)
        return f"{title} {first_name} {suffix}"
    else:
        return f"{title} {first_name}"

@app.route('/', methods=['GET'])
def home():
    """Displays the current mission status and controls."""
    # Check if user has entered their name - redirect to welcome if not
    if not session.get('user_name') or not session.get('space_name'):
        return redirect(url_for('welcome'))
    
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
    return render_template('index.html', state=state, exoplanets=EXOPLANETS, gemini_api_key=GEMINI_API_KEY, 
                         user_name=session.get('user_name'), space_name=session.get('space_name'))

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    """Welcome page where users enter their name."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            space_name = generate_space_name(name)
            session['user_name'] = name
            session['space_name'] = space_name
            return redirect(url_for('welcome_intro'))
        else:
            # If no name provided, show error
            return render_template('welcome.html', error="Please enter your name to begin your space adventure!")
    
    # GET request - show welcome form
    return render_template('welcome.html')

@app.route('/welcome_intro', methods=['GET'])
def welcome_intro():
    """Introduction page after name entry."""
    if 'user_name' not in session or 'space_name' not in session:
        return redirect(url_for('welcome'))
    
    return render_template('welcome_intro.html', 
                         user_name=session.get('user_name'),
                         space_name=session.get('space_name'),
                         exoplanets=EXOPLANETS)

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


@app.route('/spectroscopy', methods=['GET'])
def spectroscopy():
    """Shows the spectroscopy activity page."""
    if mission.status != 'SURFACE_DATA':
        return redirect(url_for('home'))
    
    state = mission.get_current_state()
    planet_key = mission.target_planet_key
    spectroscopy_data = get_spectroscopy_data(planet_key) if planet_key else None
    
    return render_template('spectroscopy.html', 
                         state=state, 
                         spectroscopy_data=spectroscopy_data,
                         elements_data=SPECTROSCOPY_ELEMENTS,
                         user_name=session.get('user_name'),
                         space_name=session.get('space_name'))

@app.route('/spectroscopy_complete', methods=['POST'])
def spectroscopy_complete():
    """Handles completion of spectroscopy activity."""
    if mission.status != 'SURFACE_DATA':
        return redirect(url_for('home'))
    
    # Mark spectroscopy as completed
    mission.spectroscopy_completed = True
    # Add bonus data units for completing spectroscopy
    mission.collected_data_units += 25
    
    return redirect(url_for('home'))

@app.route('/transit_photometry', methods=['GET'])
def transit_photometry():
    """Shows the transit photometry activity page."""
    if mission.status != 'SURFACE_DATA':
        return redirect(url_for('home'))
    
    state = mission.get_current_state()
    planet_key = mission.target_planet_key
    planet_data = EXOPLANETS.get(planet_key) if planet_key else None
    
    return render_template('transit_photometry.html', 
                         state=state, 
                         planet_data=planet_data,
                         user_name=session.get('user_name'),
                         space_name=session.get('space_name'))

@app.route('/transit_photometry_complete', methods=['POST'])
def transit_photometry_complete():
    """Handles completion of transit photometry activity."""
    if mission.status != 'SURFACE_DATA':
        return redirect(url_for('home'))
    
    # Mark transit photometry as completed
    mission.transit_photometry_completed = True
    # Add bonus data units for completing transit photometry
    mission.collected_data_units += 25
    
    return redirect(url_for('home'))

@app.route('/collect', methods=['POST'])
def collect():
    """Handles the action to collect data on the surface."""
    collect_data(mission)
    return redirect(url_for('home'))

@app.route('/give_up_activities', methods=['POST'])
def give_up_activities():
    """Allows user to skip activities and proceed to return phase."""
    if mission.status != 'SURFACE_DATA':
        return redirect(url_for('home'))
    
    # Mark both activities as "skipped" (not completed, but allow proceeding)
    # Don't add any data units since they're giving up
    mission.spectroscopy_completed = False
    mission.transit_photometry_completed = False
    # Proceed to return prep without completing activities
    mission.status = "RETURN_PREP"
    
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
    # Preserve user session data
    if 'user_name' in session:
        session['user_name'] = session['user_name']
    if 'space_name' in session:
        session['space_name'] = session['space_name']
    return redirect(url_for('home'))

@app.route('/restart', methods=['GET', 'POST'])
def restart():
    """Clears session and returns to welcome page."""
    session.clear()
    mission.__init__()  # Reset mission state
    return redirect(url_for('welcome'))

@app.route('/retry_mission', methods=['POST'])
def retry_mission():
    """Retries the mission from the phase where it failed."""
    if mission.status != 'FAILURE':
        return redirect(url_for('home'))
    
    # Retry from the phase before failure
    if mission.retry_from_failure():
        return redirect(url_for('home'))
    else:
        # If retry fails, just reset to selection
        return redirect(url_for('reset_mission'))


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
    
    # Production deployment: Use gunicorn (see Procfile)
    # For local development, run: python app.py
    # For production, gunicorn will be used and this won't execute
    # Get port from environment variable (for production) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Use 0.0.0.0 to accept connections from any IP (needed for production)
    # Use 127.0.0.1 for local development only
    host = os.environ.get('HOST', '127.0.0.1')
    # Debug mode only for local development
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("\nStarting Flask server...")
    print(f"Server will be available at: http://{host}:{port}")
    print("Gemini API key loaded successfully!")
    print("=" * 50)
    app.run(debug=debug, host=host, port=port)

    # Akbar Code
