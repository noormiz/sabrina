import random
import copy # For deep copying the state history

# --- CONSTANTS AND PLANETARY DATA ---

SIM_CONSTANTS = {
    "G_EARTH": 9.81 * 0.001,        # Simplified gravity constant (km/s^2)
    "FUEL_PER_DAY": 0.5,            # Routine fuel consumed per mission day
    "CRUISE_STEP_DAYS": 10,         # How many days each "cruise step" represents
    "ESCAPE_VELOCITY": 11.2,        # km/s (Simplified threshold)
    "IMPACT_VELOCITY_MAX": 0.05,    # km/s maximum for a safe landing
    "PLANET_GRAVITY_BASE": 0.0005,  # Base gravity constant
    "FUEL_PER_SECOND_BURN": 1.5,
    "DATA_COLLECTION_FUEL_COST": 50,
    "REQUIRED_DATA_UNITS": 50,
    "FUEL_FOR_RETURN_BURN": 100,
}

EXOPLANETS = {
    "Aetheria": {
        "name": "Aetheria", "type": "Frozen Moon", "distance": "15 Light Years",
        "icon": "🚀", "bgColor": "bg-indigo-900", "focus": "Orbital Mechanics & Scale",
        "simDistanceKm": 1500000000, "gravityFactor": 0.8, "atmosphereDrag": 0.1,
    },
    "TerraNova": {
        "name": "Terra Nova", "type": "Rocky Super-Earth", "distance": "40 Light Years",
        "icon": "🌋", "bgColor": "bg-red-900", "focus": "Gravity & Thrust",
        "simDistanceKm": 4000000000, "gravityFactor": 2.5, "atmosphereDrag": 0.5,
    },
    "Kyperus": {
        "name": "Kyperus", "type": "Ocean World", "distance": "22 Light Years",
        "icon": "🌊", "bgColor": "bg-blue-900", "focus": "Atmosphere & Pressure",
        "simDistanceKm": 2200000000, "gravityFactor": 1.2, "atmosphereDrag": 3.0,
    }
}

# --- STATE CLASS ---

class MissionState:
    """Tracks all the critical variables for the space mission."""
    def __init__(self):
        self.status = "SELECTION"       # SELECTION, PRE_LAUNCH, CRUISING, LANDING_PREP, SURFACE_DATA, RETURN_PREP, SUCCESS, FAILURE
        self.error_code = None          # Stores a specific error code
        self.mission_day = 0            # Tracks time/steps taken

        self.initial_fuel = 1000
        self.fuel = self.initial_fuel
        self.dry_mass = 500             
        self.current_mass = self.fuel + self.dry_mass
        
        self.velocity_km_s = 0.0
        self.altitude_km = 0.0
        self.target_distance_km = 0
        self.target_planet_key = None
        self.target_planet_data = None  # Store the dict from EXOPLANETS
        
        self.collected_data_units = 0
        self.required_data_units = SIM_CONSTANTS["REQUIRED_DATA_UNITS"]
        
        self._history = [] # For a potential undo/rewind feature

    def get_current_state(self):
        """Returns a dictionary of current state for easy display/logging."""
        state = self.__dict__.copy()
        state.pop('_history', None) 
        state["fuel_display"] = f"{self.fuel:.1f}"
        state["velocity_display"] = f"{self.velocity_km_s:.2f}"
        return state

    def update_mass(self):
        """Recalculates current mass based on remaining fuel."""
        self.current_mass = self.dry_mass + self.fuel

    def set_target(self, planet_key):
        """Sets the mission target and initial distance."""
        self.target_planet_key = planet_key
        self.target_planet_data = EXOPLANETS[planet_key]
        self.target_distance_km = self.target_planet_data["simDistanceKm"]
        self.status = "PRE_LAUNCH"


# --- MISSION STEP FUNCTIONS ---

def _safe_action_wrapper(func):
    """Decorator to clear error state before an action."""
    def wrapper(state, *args, **kwargs):
        state.error_code = None
        return func(state, *args, **kwargs)
    return wrapper

@_safe_action_wrapper
def launch_step(state, twr):
    """
    Simulates the launch phase based on user-input Thrust-to-Weight Ratio (TWR).
    TWR is the raw value from the slider (e.g., 1.5).
    """
    if state.status != "PRE_LAUNCH":
        return "Not in the launch phase."
    
    twr = float(twr)

    # 1. TWR to Fuel Consumption mapping: 
    # Use twr directly for consumption as a simple penalty mechanism
    fuel_consumed = twr * 15 
    thrust_percent = min(100, (twr - 1.0) * 40)
    actual_thrust = thrust_percent * 50

    # Check for failure BEFORE changing state
    if state.fuel < fuel_consumed:
        state.error_code = "LOW_FUEL_LAUNCH"
        state.status = "FAILURE"
        return "Launch aborted due to insufficient fuel."
        
    if twr < 1.0:
        state.error_code = "GRAVITY_FAIL"
        state.status = "FAILURE"
        return "Thrust too low. Gravity wins."

    # Apply changes
    state.fuel -= fuel_consumed
    state.update_mass()
    
    # 2. Apply Simplified Physics (similar to the JS version)
    net_force_N = actual_thrust - (state.current_mass * SIM_CONSTANTS["G_EARTH"])
    acceleration_km_s2 = net_force_N / state.current_mass
    
    BURN_TIME_S = 10
    state.velocity_km_s += acceleration_km_s2 * BURN_TIME_S
    
    # Prevent crashing for simplicity, just check velocity
    state.mission_day += 1

    # 3. Check for Stage Transition and Mission Constraint Failure
    if state.velocity_km_s >= SIM_CONSTANTS["ESCAPE_VELOCITY"]:
        state.status = "CRUISING"
        # Apply initial distance bump to skip orbital mechanics
        state.altitude_km = min(state.altitude_km, state.target_distance_km * 0.05) 
        
        # Check mission-specific constraints (Non-fatal warning logic)
        if state.target_planet_key == 'TerraNova' and twr < 2.0:
            state.error_code = "INEFFICIENT_TWR_HIGH_GRAV"
            return "Launch successful, but inefficient. Check fuel reserves for high-gravity landing."
        if state.target_planet_key == 'Aetheria' and (twr > 1.8 or twr < 1.2):
            state.error_code = "INEFFICIENT_TWR_LONG_CRUISE"
            return "Launch successful, but inefficient. You wasted fuel needed for the long cruise."

        return "Launch successful! Entering Cruise Phase."
    
    return "Launch in progress. Velocity updated."


@_safe_action_wrapper
def cruise_step(state, burn_duration_s=0):
    """
    Simulates a cruise step towards the target planet. Includes optional mid-course burn.
    """
    if state.status not in ["CRUISING", "FAILURE"]:
        return "Not currently in the cruise phase."

    days = SIM_CONSTANTS["CRUISE_STEP_DAYS"]
    burn_duration_s = int(burn_duration_s)

    # 1. Mid-Course Correction Burn
    if burn_duration_s > 0:
        fuel_consumed_burn = burn_duration_s * SIM_CONSTANTS["FUEL_PER_SECOND_BURN"]
        if state.fuel < fuel_consumed_burn:
            state.error_code = "OUT_OF_FUEL_BURN"
            state.status = "FAILURE" 
            return "CRITICAL FAILURE: Ran out of fuel during mid-course correction."
        
        state.velocity_km_s += burn_duration_s * 0.1 # 1s burn = 0.1 km/s speed increase
        state.fuel -= fuel_consumed_burn
        state.update_mass()
    
    # 2. Routine Fuel Consumption
    fuel_consumed_routine = days * SIM_CONSTANTS["FUEL_PER_DAY"]
    if state.fuel < fuel_consumed_routine:
        state.error_code = "OUT_OF_FUEL_CRUISE"
        state.status = "FAILURE" 
        return "CRITICAL FAILURE: Ran out of fuel mid-course. Vehicle is adrift."
        
    state.fuel -= fuel_consumed_routine
    state.mission_day += days
    state.update_mass()
    
    # 3. Update Position
    distance_traveled = state.velocity_km_s * (days * 3600)
    state.altitude_km += distance_traveled
    
    # 4. Check for Arrival
    if state.altitude_km >= state.target_distance_km:
        state.altitude_km = state.target_distance_km
        state.status = "LANDING_PREP"
        state.velocity_km_s = max(0.5, state.velocity_km_s) # Set initial landing velocity
        return "Arrival at target planet! Preparing for landing sequence."

    distance_remaining = state.target_distance_km - state.altitude_km
    
    # Check mission-specific constraints (Non-fatal warning logic)
    if burn_duration_s > 0:
        is_optimal = False
        planet_key = state.target_planet_key
        if planet_key == 'Aetheria' and 10 <= burn_duration_s <= 20: is_optimal = True
        elif planet_key == 'Kyperus' and 20 <= burn_duration_s <= 30: is_optimal = True
        elif planet_key == 'TerraNova' and 30 <= burn_duration_s <= 45: is_optimal = True

        if not is_optimal:
            state.error_code = "SUBOPTIMAL_BURN"
            return f"Cruising... WARNING: Burn of {burn_duration_s}s was sub-optimal for {state.target_planet_data['name']}."

    return f"Cruising... Mission Day {state.mission_day}. Distance remaining: {distance_remaining:,.0f} km."

@_safe_action_wrapper
def landing_step(state, retro_burn_duration_s):
    """
    Simulates the landing retro-burn based on user-input duration.
    """
    if state.status != "LANDING_PREP":
        return "Not in the landing prep phase."

    retro_burn_duration_s = int(retro_burn_duration_s)
    planet_data = state.target_planet_data

    # 1. Calculate Fuel and Mass Changes
    fuel_consumed = retro_burn_duration_s * SIM_CONSTANTS["FUEL_PER_SECOND_BURN"]

    if state.fuel < fuel_consumed:
        state.error_code = "LOW_FUEL_LANDING_CRASH"
        state.status = "FAILURE"
        return "CRITICAL FAILURE: Ran out of fuel during retro-burn, leading to impact."

    state.fuel -= fuel_consumed
    state.update_mass()
    
    # 2. Apply Physics (Deceleration)
    
    # Pull: Gravity is relative to the planet's factor
    planet_gravity_pull = state.current_mass * SIM_CONSTANTS["PLANET_GRAVITY_BASE"] * planet_data["gravityFactor"]

    # Push: Retro-thrust force is proportional to burn duration
    retro_thrust = retro_burn_duration_s * 6000 
    
    # Drag: Atmospheric Drag is based on velocity and drag factor
    drag_force = state.velocity_km_s * 5000 * planet_data["atmosphereDrag"] 

    # Net Force = (Thrust + Drag) - Gravity. (Deceleration occurs if Net Force > 0 in this simplified model)
    net_force_N = (retro_thrust + drag_force) - planet_gravity_pull
    
    deceleration_km_s2 = net_force_N / state.current_mass
    
    # Apply change to velocity
    state.velocity_km_s -= deceleration_km_s2 * 1 
    state.velocity_km_s = max(0, state.velocity_km_s) 
    
    # 3. Check for Landing Success/Failure
    if state.velocity_km_s <= SIM_CONSTANTS["IMPACT_VELOCITY_MAX"]:
        state.status = "SURFACE_DATA"
        state.velocity_km_s = 0.0 
        return "Soft landing successful! Preparing to collect scientific data."
    elif retro_burn_duration_s > 10 and deceleration_km_s2 < -0.5: # Simple check for excessive deceleration
         state.error_code = "OVER_BURN_FAILURE"
         state.status = "FAILURE"
         return "FAILURE: Retro-burn was too powerful, vehicle destroyed by excessive stress."
    elif state.velocity_km_s > SIM_CONSTANTS["IMPACT_VELOCITY_MAX"]:
        state.error_code = "HIGH_VELOCITY_IMPACT"
        state.status = "FAILURE"
        return "CATASTROPHIC FAILURE: Impacted the surface at high velocity."

    return "Landing in progress. Current velocity: {:.3f} km/s. IMPACT IMMINENT!".format(state.velocity_km_s)

@_safe_action_wrapper
def collect_data(state):
    """Simulates the collection of scientific data on the surface."""
    if state.status != "SURFACE_DATA":
        return "Not on the surface."

    if state.fuel < SIM_CONSTANTS["DATA_COLLECTION_FUEL_COST"]:
        state.error_code = "INSUFFICIENT_FUEL_DATA"
        state.status = "FAILURE"
        return "FAILURE: Insufficient power for data systems. Must abort mission."
        
    state.fuel -= SIM_CONSTANTS["DATA_COLLECTION_FUEL_COST"]
    state.collected_data_units = state.required_data_units
    state.mission_day += 5 
    state.status = "RETURN_PREP"
    
    return "Data collection complete! Preparing for launch back to Earth."

@_safe_action_wrapper
def return_home(state):
    """Final check for a successful return home."""
    if state.status != "RETURN_PREP":
        return "Cannot initiate return home sequence."
        
    if state.fuel < SIM_CONSTANTS["FUEL_FOR_RETURN_BURN"]:
        state.error_code = "STRANDED_NO_RETURN_FUEL"
        state.status = "FAILURE"
        return "FAILURE: Not enough fuel for the return burn. Crew is stranded."

    if state.collected_data_units >= state.required_data_units:
        state.fuel -= SIM_CONSTANTS["FUEL_FOR_RETURN_BURN"]
        state.status = "SUCCESS"
        return "Mission COMPLETE! Crew is on course for Earth return."
    else:
        state.error_code = "MISSION_GOAL_FAILED"
        state.status = "FAILURE"
        return "FAILURE: Mission aborted. Did not collect required scientific data."