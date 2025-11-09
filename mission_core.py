import random
import copy # For deep copying the state history

# --- CONSTANTS AND PLANETARY DATA ---

SIM_CONSTANTS = {
    "G_EARTH": 9.81 * 0.001,        # Simplified gravity constant (km/s^2)
    "FUEL_PER_DAY": 2.0,            # Routine fuel consumed per mission day (increased for realism)
    "CRUISE_STEP_DAYS": 10,         # How many days each "cruise step" represents
    "ESCAPE_VELOCITY": 8.0,         # km/s (Lowered to make launch easier - still educational)
    "IMPACT_VELOCITY_MAX": 0.15,    # km/s maximum for a safe landing (more forgiving for kids)
    "PLANET_GRAVITY_BASE": 0.0005,  # Base gravity constant
    "FUEL_PER_SECOND_BURN": 2.0,    # Fuel per second of burn (slightly higher)
    "DATA_COLLECTION_FUEL_COST": 40, # Reduced for better balance
    "REQUIRED_DATA_UNITS": 50,
    "FUEL_FOR_RETURN_BURN": 80,     # Reduced for better balance
    "LAUNCH_FUEL_BASE": 20,         # Base fuel cost for launch
    "LAUNCH_FUEL_MULTIPLIER": 8,    # Multiplier for TWR (more intuitive)
}

EXOPLANETS = {
    "Aetheria": {
        "name": "Aetheria", "type": "Frozen Moon", "distance": "15 Light Years",
        "icon": "🚀", "bgColor": "bg-indigo-900", "focus": "Orbital Mechanics & Scale",
        # Scaled down by 100 for gameplay: 1.5B km -> 15M km (takes ~2-3 steps at 8-10 km/s)
        "simDistanceKm": 15000000, "gravityFactor": 0.8, "atmosphereDrag": 0.1,
        "atmosphere_elements": ["Nitrogen", "Methane", "Argon"],  # Elements in atmosphere for spectroscopy
        "transit_depth": 0.008,  # Dip depth (0.8% brightness drop) - small moon
        "transit_duration_hours": 2.5,  # Transit duration in hours
        "orbital_period_days": 12.5,  # Days between transits
        "planet_star_radius_ratio": 0.089,  # Rp/Rs ratio (calculated from depth)
    },
    "TerraNova": {
        "name": "Terra Nova", "type": "Rocky Super-Earth", "distance": "40 Light Years",
        "icon": "🌋", "bgColor": "bg-red-900", "focus": "Gravity & Thrust",
        # Scaled down: 4B km -> 40M km (takes ~5-6 steps at 8-10 km/s)
        "simDistanceKm": 40000000, "gravityFactor": 2.5, "atmosphereDrag": 0.5,
        "atmosphere_elements": ["Carbon Dioxide", "Sulfur Dioxide", "Nitrogen"],
        "transit_depth": 0.015,  # Dip depth (1.5% brightness drop) - larger planet
        "transit_duration_hours": 4.0,
        "orbital_period_days": 18.0,
        "planet_star_radius_ratio": 0.122,  # Rp/Rs ratio
    },
    "Kyperus": {
        "name": "Kyperus", "type": "Ocean World", "distance": "22 Light Years",
        "icon": "🌊", "bgColor": "bg-blue-900", "focus": "Atmosphere & Pressure",
        # Scaled down: 2.2B km -> 22M km (takes ~3-4 steps at 8-10 km/s)
        "simDistanceKm": 22000000, "gravityFactor": 1.2, "atmosphereDrag": 3.0,
        "atmosphere_elements": ["Water Vapor", "Oxygen", "Nitrogen"],
        "transit_depth": 0.012,  # Dip depth (1.2% brightness drop) - medium planet
        "transit_duration_hours": 3.2,
        "orbital_period_days": 15.0,
        "planet_star_radius_ratio": 0.110,  # Rp/Rs ratio
    }
}

# Spectroscopy data: Wavelength positions (in nanometers) for absorption lines
SPECTROSCOPY_ELEMENTS = {
    "Nitrogen": {"wavelengths": [337, 358, 380, 410], "color": "#64ffda", "description": "Common in many planetary atmospheres", "category": "temperature_control", "habitability": "neutral"},
    "Oxygen": {"wavelengths": [630, 636, 690, 760], "color": "#00bcd4", "description": "Essential for life as we know it", "category": "habitable", "habitability": "positive"},
    "Carbon Dioxide": {"wavelengths": [430, 500, 570, 650], "color": "#ff6b9d", "description": "Greenhouse gas, traps heat", "category": "greenhouse", "habitability": "moderate"},
    "Methane": {"wavelengths": [340, 380, 420, 450], "color": "#f8b500", "description": "Can indicate biological activity", "category": "habitable", "habitability": "positive"},
    "Water Vapor": {"wavelengths": [720, 820, 940, 1130], "color": "#00e676", "description": "Essential for life", "category": "habitable", "habitability": "positive"},
    "Sulfur Dioxide": {"wavelengths": [280, 310, 340, 370], "color": "#ff9800", "description": "Volcanic activity indicator", "category": "poisonous", "habitability": "negative"},
    "Argon": {"wavelengths": [750, 800, 850, 900], "color": "#9c27b0", "description": "Noble gas, very stable", "category": "neutral", "habitability": "neutral"},
}

def assess_atmosphere(elements):
    """Assess the habitability and characteristics of a planet based on detected elements."""
    assessment = {
        "habitability_score": 0,
        "habitable": False,
        "temperature_control": False,
        "poisonous": False,
        "greenhouse_effect": False,
        "findings": [],
        "conclusion": "",
        "recommendation": ""
    }
    
    # Check for habitable elements
    habitable_elements = ["Oxygen", "Water Vapor", "Methane"]
    found_habitable = [e for e in elements if e in habitable_elements]
    
    if "Oxygen" in elements:
        assessment["habitability_score"] += 3
        assessment["findings"].append("✅ Oxygen detected! Essential for human breathing.")
    if "Water Vapor" in elements:
        assessment["habitability_score"] += 3
        assessment["findings"].append("✅ Water Vapor found! Water is crucial for life.")
    if "Methane" in elements:
        assessment["habitability_score"] += 2
        assessment["findings"].append("🔬 Methane detected! Could indicate biological activity.")
    
    # Check for temperature control
    if "Nitrogen" in elements:
        assessment["temperature_control"] = True
        assessment["habitability_score"] += 1
        assessment["findings"].append("🌡️ Nitrogen present - helps regulate temperature.")
    
    # Check for poisonous elements
    if "Sulfur Dioxide" in elements:
        assessment["poisonous"] = True
        assessment["habitability_score"] -= 2
        assessment["findings"].append("⚠️ Sulfur Dioxide detected - TOXIC! Indicates volcanic activity.")
    
    # Check for greenhouse effect
    if "Carbon Dioxide" in elements:
        assessment["greenhouse_effect"] = True
        assessment["habitability_score"] += 1
        assessment["findings"].append("🌍 Carbon Dioxide found - creates greenhouse effect (traps heat).")
    
    # Determine overall habitability
    if assessment["habitability_score"] >= 5:
        assessment["habitable"] = True
        assessment["conclusion"] = "🌟 This planet shows PROMISING signs for potential habitability!"
        assessment["recommendation"] = "Consider this planet for future colonization missions. Further exploration recommended!"
    elif assessment["habitability_score"] >= 3:
        assessment["habitable"] = "moderate"
        assessment["conclusion"] = "🔍 This planet has MIXED characteristics - some promising, some concerning."
        assessment["recommendation"] = "More detailed analysis needed. Could be habitable with proper equipment."
    else:
        assessment["habitable"] = False
        assessment["conclusion"] = "❌ This planet appears UNSUITABLE for human habitation."
        assessment["recommendation"] = "Not recommended for colonization. May be useful for scientific research only."
    
    return assessment

def get_spectroscopy_data(planet_key):
    """Generate spectroscopy data for a planet."""
    if planet_key not in EXOPLANETS:
        return None
    
    planet = EXOPLANETS[planet_key]
    elements = planet.get("atmosphere_elements", [])
    
    # Generate spectrum data with absorption lines
    spectrum = []
    all_wavelengths = []
    
    for element in elements:
        if element in SPECTROSCOPY_ELEMENTS:
            element_data = SPECTROSCOPY_ELEMENTS[element]
            all_wavelengths.extend(element_data["wavelengths"])
    
    # Create spectrum from 300nm to 1200nm
    for wavelength in range(300, 1201, 5):
        intensity = 100  # Base intensity
        
        # Add absorption lines (reduce intensity at specific wavelengths)
        for element in elements:
            if element in SPECTROSCOPY_ELEMENTS:
                element_wavelengths = SPECTROSCOPY_ELEMENTS[element]["wavelengths"]
                for elem_wl in element_wavelengths:
                    if abs(wavelength - elem_wl) < 3:  # Absorption line width
                        intensity -= 30  # Absorption depth
        
        intensity = max(10, intensity)  # Minimum intensity
        spectrum.append({"wavelength": wavelength, "intensity": intensity})
    
    return {
        "elements": elements,
        "spectrum": spectrum,
        "all_wavelengths": sorted(set(all_wavelengths))
    }

# --- STATE CLASS ---

class MissionState:
    """Tracks all the critical variables for the space mission."""
    def __init__(self):
        self.status = "SELECTION"       # SELECTION, PRE_LAUNCH, CRUISING, LANDING_PREP, SURFACE_DATA, SPECTROSCOPY, RETURN_PREP, SUCCESS, FAILURE
        self.error_code = None          # Stores a specific error code
        self.mission_day = 0            # Tracks time/steps taken
        self.spectroscopy_completed = False  # Track if spectroscopy activity is done
        self.transit_photometry_completed = False  # Track if transit photometry activity is done

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
    Simplified and balanced for educational purposes.
    """
    if state.status != "PRE_LAUNCH":
        return "Not in the launch phase."
    
    twr = float(twr)

    # 1. Simplified Fuel Consumption: Base cost + TWR multiplier
    # More intuitive: Higher TWR = more fuel, but not too punishing
    fuel_consumed = SIM_CONSTANTS["LAUNCH_FUEL_BASE"] + (twr - 1.0) * SIM_CONSTANTS["LAUNCH_FUEL_MULTIPLIER"]
    fuel_consumed = max(20, fuel_consumed)  # Minimum 20 fuel

    # Check for failure BEFORE changing state
    if state.fuel < fuel_consumed:
        state.error_code = "LOW_FUEL_LAUNCH"
        state.status = "FAILURE"
        return "Launch aborted due to insufficient fuel."
        
    if twr < 1.0:
        state.error_code = "GRAVITY_FAIL"
        state.status = "FAILURE"
        return "Thrust too low. Gravity wins. TWR must be > 1.0 to lift off!"

    # Apply changes
    state.fuel -= fuel_consumed
    state.update_mass()
    
    # 2. Simplified Physics: TWR directly affects velocity gain
    # Increased base velocity to make cruise phase faster
    base_velocity_gain = 8.0  # Base km/s gained from launch (increased from 5.0)
    velocity_gain = base_velocity_gain * (twr - 0.3)  # TWR 1.0 = 0.7x, TWR 1.5 = 1.2x, TWR 2.0 = 1.7x
    velocity_gain = max(5.0, velocity_gain)  # Minimum gain (increased from 2.0)
    
    state.velocity_km_s += velocity_gain
    state.mission_day += 1

    # 3. Check for Stage Transition
    if state.velocity_km_s >= SIM_CONSTANTS["ESCAPE_VELOCITY"]:
        state.status = "CRUISING"
        # Start at 2% of distance (small head start)
        state.altitude_km = state.target_distance_km * 0.02
        
        # Success message with helpful feedback
        if twr >= 1.2 and twr <= 1.8:
            return "Launch successful! Efficient TWR choice. Entering Cruise Phase."
        elif twr < 1.2:
            return "Launch successful, but low TWR used extra fuel. Entering Cruise Phase."
        else:
            return "Launch successful! High TWR was fast but used more fuel. Entering Cruise Phase."

    # Still building velocity
    return f"Launch in progress. Current velocity: {state.velocity_km_s:.2f} km/s. Need {SIM_CONSTANTS['ESCAPE_VELOCITY']} km/s to escape."


@_safe_action_wrapper
def cruise_step(state, burn_duration_s=0):
    """
    Simulates a cruise step towards the target planet. Includes optional mid-course burn.
    Balanced for educational success.
    """
    if state.status != "CRUISING":
        return "Not currently in the cruise phase."

    days = SIM_CONSTANTS["CRUISE_STEP_DAYS"]
    burn_duration_s = int(burn_duration_s)

    # 1. Mid-Course Correction Burn (simplified and more effective)
    if burn_duration_s > 0:
        fuel_consumed_burn = burn_duration_s * SIM_CONSTANTS["FUEL_PER_SECOND_BURN"]
        if state.fuel < fuel_consumed_burn:
            state.error_code = "OUT_OF_FUEL_BURN"
            state.status = "FAILURE" 
            return "CRITICAL FAILURE: Ran out of fuel during mid-course correction."
        
        # More intuitive: Each second of burn adds velocity
        # Increased effectiveness to make burns more impactful
        velocity_increase = burn_duration_s * 0.25  # Increased from 0.15 to 0.25 km/s per second
        state.velocity_km_s += velocity_increase
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
    
    # 3. Update Position (simplified calculation)
    # Distance = velocity * time
    # Distances are already scaled down for gameplay (divided by 10,000)
    seconds_in_step = days * 24 * 3600  # Convert days to seconds
    distance_traveled = state.velocity_km_s * seconds_in_step  # km/s * s = km
    state.altitude_km += distance_traveled
    
    # 4. Check for Arrival
    if state.altitude_km >= state.target_distance_km:
        state.altitude_km = state.target_distance_km
        state.status = "LANDING_PREP"
        # Set reasonable landing velocity based on planet
        planet_data = state.target_planet_data
        # Higher gravity/atmosphere = higher approach velocity
        base_velocity = 2.0 + (planet_data["gravityFactor"] * 0.5) + (planet_data["atmosphereDrag"] * 0.3)
        state.velocity_km_s = min(base_velocity, state.velocity_km_s)  # Don't exceed current velocity
        return "Arrival at target planet! Preparing for landing sequence."

    distance_remaining = state.target_distance_km - state.altitude_km
    progress_percent = (state.altitude_km / state.target_distance_km) * 100
    
    return f"Cruising... Mission Day {state.mission_day}. Distance remaining: {distance_remaining:,.0f} km ({progress_percent:.1f}% complete)."

@_safe_action_wrapper
def landing_step(state, retro_burn_duration_s):
    """
    Simulates the landing retro-burn based on user-input duration.
    Simplified and more predictable for educational purposes.
    """
    if state.status != "LANDING_PREP":
        return "Not in the landing prep phase."

    retro_burn_duration_s = int(retro_burn_duration_s)
    planet_data = state.target_planet_data

    # 1. Calculate Fuel Consumption
    fuel_consumed = retro_burn_duration_s * SIM_CONSTANTS["FUEL_PER_SECOND_BURN"]

    if state.fuel < fuel_consumed:
        state.error_code = "LOW_FUEL_LANDING_CRASH"
        state.status = "FAILURE"
        return "CRITICAL FAILURE: Ran out of fuel during retro-burn, leading to impact."

    state.fuel -= fuel_consumed
    state.update_mass()
    
    # 2. Simplified Physics: More intuitive velocity reduction
    # Each second of burn reduces velocity by a predictable amount
    # Increased significantly to make landing achievable
    base_deceleration = 0.8  # km/s per second of burn (increased from 0.4 for easier landing)
    
    # Planet factors affect deceleration:
    # - Higher gravity = harder to slow down (reduces deceleration)
    # - Higher atmosphere = helps slow down (increases deceleration)
    gravity_penalty = planet_data["gravityFactor"] * 0.05  # Reduced penalty (was 0.1)
    atmosphere_help = planet_data["atmosphereDrag"] * 0.1  # Increased help (was 0.05)
    
    effective_deceleration = base_deceleration - gravity_penalty + atmosphere_help
    effective_deceleration = max(0.5, effective_deceleration)  # Higher minimum (was 0.2)
    
    # Total velocity reduction = burn duration * effective deceleration
    velocity_reduction = retro_burn_duration_s * effective_deceleration
    
    # Apply velocity reduction
    state.velocity_km_s -= velocity_reduction
    state.velocity_km_s = max(0, state.velocity_km_s)  # Can't go negative
    
    # 3. Check for Landing Success/Failure
    if state.velocity_km_s <= SIM_CONSTANTS["IMPACT_VELOCITY_MAX"]:
        state.status = "SURFACE_DATA"
        state.velocity_km_s = 0.0 
        return "Soft landing successful! Preparing to collect scientific data."
    elif state.velocity_km_s > SIM_CONSTANTS["IMPACT_VELOCITY_MAX"]:
        # Give helpful feedback
        velocity_needed = state.velocity_km_s - SIM_CONSTANTS["IMPACT_VELOCITY_MAX"]
        additional_burn_needed = int(velocity_needed / effective_deceleration) + 1
        
        state.error_code = "HIGH_VELOCITY_IMPACT"
        state.status = "FAILURE"
        return f"CATASTROPHIC FAILURE: Impacted at {state.velocity_km_s:.2f} km/s. Need ~{additional_burn_needed} more seconds of retro-burn for safe landing."

    # Still descending
    return f"Landing in progress. Velocity: {state.velocity_km_s:.2f} km/s. Need < {SIM_CONSTANTS['IMPACT_VELOCITY_MAX']} km/s for safe landing."

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