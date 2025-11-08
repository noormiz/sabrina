# mission_core.py

import numpy as np
import random 

class MissionState:
    """Tracks all the critical variables for the space mission."""
    def __init__(self):
        # Mission Status
        self.status = "PRE_LAUNCH"      # Current phase: PRE_LAUNCH, LAUNCH, CRUISE, LANDING, SUCCESS, FAILURE
        self.error_code = None          # Stores a specific code like "LOW_FUEL" if failure occurs
        self.mission_day = 0            # Tracks time/steps taken

        # Vehicle Parameters (Simplified)
        self.initial_fuel = 1000        # Max fuel units
        self.fuel = self.initial_fuel   # Current fuel units
        self.dry_mass = 500             # Mass of the rocket without fuel (kg)
        self.current_mass = self.fuel + self.dry_mass # Total mass
        
        # Position & Velocity (Simplified for 2D, Step-based)
        self.velocity_km_s = 0.0        # Current velocity (km/s)
        self.altitude_km = 0.0          # Current altitude/distance from Earth (km)
        self.target_distance_km = 400000 # Target planet distance (e.g., simplified Moon distance)

        # Data Collection
        self.collected_data_units = 0   # Data points gathered at the target
        self.required_data_units = 50   # Goal for mission success
        
    def get_current_state(self):
        """Returns a dictionary of current state for easy display/logging."""
        # Convert the object's attributes to a dictionary
        return self.__dict__


# Simplified Constants
G_EARTH = 9.81 * 0.001 # Simplified gravity constant (km/s^2)
FUEL_BURN_RATE = 1     # Fuel consumed per unit of thrust

def launch_step(state, thrust_percent):
    """
    Simulates the launch phase based on user-input thrust.
    Thrust is a value from 0 to 100.
    """
    # 1. Input Validation
    if state.status != "PRE_LAUNCH":
        return "Not in the launch phase."
        
    if not 0 <= thrust_percent <= 100:
        state.error_code = "INVALID_THRUST_INPUT"
        state.status = "FAILURE"
        return "Invalid input."

    # 2. Calculate Fuel and Mass Changes
    actual_thrust = thrust_percent * 1000 # Convert percent to an arbitrary thrust unit (Newtons)
    fuel_consumed = thrust_percent * FUEL_BURN_RATE
    
    # Check for failure BEFORE changing state (critical for AI feedback)
    if state.fuel < fuel_consumed:
        state.error_code = "LOW_FUEL_LAUNCH"
        state.status = "FAILURE"
        return "Launch aborted due to insufficient fuel."
        
    # Apply changes if successful
    state.fuel -= fuel_consumed
    state.current_mass = state.dry_mass + state.fuel
    
    # 3. Apply Simplified Physics (Newton's 2nd Law: F_net = m * a)
    # F_net = Thrust - Drag (simplified to a constant) - Gravity
    # Acceleration = F_net / Mass
    
    # Simplified Net Force (Ignore drag for a quick hack)
    net_force_N = actual_thrust - (state.current_mass * G_EARTH)
    
    # Acceleration
    acceleration_km_s2 = net_force_N / state.current_mass
    
    # Apply change in velocity (assuming a fixed 10-second burn/step)
    BURN_TIME_S = 10
    state.velocity_km_s += acceleration_km_s2 * BURN_TIME_S
    
    # Update position (simplified distance = velocity * time)
    state.altitude_km += state.velocity_km_s * BURN_TIME_S
    state.mission_day += 1

    # 4. Check for Stage Transition (did we reach orbit/escape velocity?)
    ESCAPE_VELOCITY = 11.2 # km/s (Simplified threshold)
    if state.velocity_km_s >= ESCAPE_VELOCITY:
        state.status = "CRUISE"
        return "Launch successful! Entering Cruise Phase."
    
    # 5. Check for catastrophic failure (e.g., low thrust/gravity too strong)
    if state.altitude_km < 0:
         state.error_code = "GRAVITY_FAIL"
         state.status = "FAILURE"
         return "Failed to overcome gravity and crashed back to Earth."

    return "Launch in progress. Velocity updated."


# mission_core.py (Continued)

FUEL_PER_DAY = 0.5     # Fuel consumed per mission day for life support/minor corrections
CRUISE_STEP_DAYS = 10  # How many days each "step" represents

def cruise_step(state):
    """
    Simulates a 10-day cruise step towards the target planet.
    Checks for fuel, updates position, and checks for arrival.
    """
    # 1. Input Validation
    if state.status != "CRUISE":
        return "Not currently in the cruise phase."

    # 2. Calculate Fuel Consumption
    fuel_consumed = CRUISE_STEP_DAYS * FUEL_PER_DAY
    
    # Check for failure (running out of fuel mid-cruise)
    if state.fuel < fuel_consumed:
        state.error_code = "OUT_OF_FUEL_CRUISE"
        state.status = "FAILURE"
        return "CRITICAL FAILURE: Ran out of fuel mid-course. Vehicle is adrift."
        
    # Apply changes
    state.fuel -= fuel_consumed
    state.mission_day += CRUISE_STEP_DAYS
    state.current_mass = state.dry_mass + state.fuel # Mass slightly decreases

    # 3. Update Position
    # Since velocity is constant (or nearly constant) in space, we use distance = speed * time
    # This is highly simplified!
    distance_traveled = state.velocity_km_s * (CRUISE_STEP_DAYS * 86400) # days to seconds
    state.altitude_km += distance_traveled
    
    # Check for Stage Transition (Did we arrive?)
    if state.altitude_km >= state.target_distance_km:
        state.altitude_km = state.target_distance_km # Set exactly to target for cleaner transition
        state.status = "LANDING_PREP"
        return "Arrival at target planet! Preparing for landing sequence."

    # 4. Success message for continuing the journey
    distance_remaining = state.target_distance_km - state.altitude_km
    return f"Cruising... Mission Day {state.mission_day}. Distance remaining: {distance_remaining:,.0f} km."

    # mission_core.py (Continued)

PLANET_GRAVITY = 0.0005 # Simplified gravity constant of the target planet
IMPACT_VELOCITY_MAX = 0.05 # km/s maximum for a safe landing

def landing_step(state, retro_burn_duration_s):
    """
    Simulates the landing retro-burn based on user-input duration.
    Retro-burn duration is in seconds.
    """
    if state.status != "LANDING_PREP":
        return "Not in the landing prep phase."

    # 1. Calculate Fuel and Mass Changes
    FUEL_PER_SECOND = 1.5 # Landing burns are high consumption
    fuel_consumed = retro_burn_duration_s * FUEL_PER_SECOND

    if state.fuel < fuel_consumed:
        state.error_code = "LOW_FUEL_LANDING_CRASH"
        state.status = "FAILURE"
        return "CRITICAL FAILURE: Ran out of fuel during retro-burn, leading to impact."

    state.fuel -= fuel_consumed
    state.current_mass = state.dry_mass + state.fuel
    
    # 2. Apply Physics (Deceleration)
    # Landing involves slowing down the current velocity (deceleration)
    
    # Thrust Force is proportional to duration (simplified)
    retro_thrust = retro_burn_duration_s * 500
    
    # Simplified Net Force (Ignore drag, just thrust vs. planet gravity)
    net_force_N = retro_thrust - (state.current_mass * PLANET_GRAVITY)
    
    # Deceleration = F_net / Mass
    deceleration_km_s = net_force_N / state.current_mass
    
    # Apply change to velocity (subtraction for deceleration)
    state.velocity_km_s -= deceleration_km_s * 1 
    # Use a fixed time step of 1s for the final moment

    # 3. Check for Landing Success/Failure
    if state.velocity_km_s <= IMPACT_VELOCITY_MAX and state.velocity_km_s >= 0:
        state.status = "SURFACE_DATA"
        state.velocity_km_s = 0.0 # Stop movement for clean state
        return "Soft landing successful! Preparing to collect scientific data."
    elif state.velocity_km_s < 0:
        # User over-burned, or our calculation resulted in negative velocity (bad physics)
        state.error_code = "OVER_BURN_FAILURE"
        state.status = "FAILURE"
        return "FAILURE: Retro-burn was too powerful, the vehicle was destroyed by excessive stress."
    elif state.velocity_km_s > IMPACT_VELOCITY_MAX:
        state.error_code = "HIGH_VELOCITY_IMPACT"
        state.status = "FAILURE"
        return "CATASTROPHIC FAILURE: Impacted the surface at high velocity."

    return "Landing step incomplete (should not happen in this model)."


# (Continue to Step 7 below)
# mission_core.py (Continued)

DATA_COLLECTION_FUEL_COST = 50 # Fuel cost to keep systems running for data collection

def collect_data(state):
    """Simulates the collection of scientific data on the surface."""
    if state.status != "SURFACE_DATA":
        return "Not on the surface."

    if state.fuel < DATA_COLLECTION_FUEL_COST:
        state.error_code = "INSUFFICIENT_FUEL_DATA"
        state.status = "FAILURE"
        return "FAILURE: Insufficient power for data systems. Must abort mission."
        
    # Success: Collect data and burn fuel
    state.fuel -= DATA_COLLECTION_FUEL_COST
    state.collected_data_units = state.required_data_units # Collect all needed data instantly
    state.mission_day += 5 # Time taken to collect data
    state.status = "RETURN_PREP"
    
    return "Data collection complete! Preparing for launch back to Earth."

    # mission_core.py (Continued)

def return_home(state):
    """Final check to see if we can return home successfully."""
    if state.status != "RETURN_PREP":
        return "Cannot initiate return home sequence."
        
    # Check if we have enough fuel for the return burn (simplified)
    FUEL_FOR_RETURN_BURN = 100 
    if state.fuel < FUEL_FOR_RETURN_BURN:
        state.error_code = "STRANDED_NO_RETURN_FUEL"
        state.status = "FAILURE"
        return "FAILURE: Not enough fuel for the return burn. Crew is stranded."

    # Final Success Check
    if state.collected_data_units >= state.required_data_units:
        state.fuel -= FUEL_FOR_RETURN_BURN
        state.status = "SUCCESS"
        return "Mission COMPLETE! Crew is on course for Earth return."
    else:
        state.error_code = "MISSION_GOAL_FAILED"
        state.status = "FAILURE"
        return "FAILURE: Mission aborted. Did not collect required scientific data."