# # test_mission_core.py

# from mission_core import MissionState, launch_step

# def test_launch_scenarios():
#     print("--- Running Launch Scenarios Test ---")

#     # Scenario 1: Successful Launch (High Thrust)
#     print("\n[Scenario 1: High Thrust Test]")
#     state_high_thrust = MissionState()
#     print(f"Initial State: {state_high_thrust.get_current_state()}")
    
#     # Use a high thrust value (e.g., 90%)
#     result = launch_step(state_high_thrust, 90)
    
#     # Check the key success indicators
#     print(f"Result: {result}")
#     print(f"Status: {state_high_thrust.status}")
#     print(f"Velocity: {state_high_thrust.velocity_km_s:.2f} km/s")
#     print(f"Fuel Left: {state_high_thrust.fuel:.2f}")

#     # Scenario 2: Failure - Insufficient Fuel
#     print("\n[Scenario 2: Low Fuel Failure Test]")
#     state_low_fuel = MissionState()
#     # Manually drain the fuel before the launch attempt
#     state_low_fuel.fuel = 5 
    
#     result = launch_step(state_low_fuel, 90)
    
#     # Check the failure indicators
#     print(f"Result: {result}")
#     print(f"Status: {state_low_fuel.status}")
#     print(f"Error Code: {state_low_fuel.error_code}")
#     print(f"Fuel Left: {state_low_fuel.fuel:.2f}")

#     # Scenario 3: Failure - Invalid Input
#     print("\n[Scenario 3: Invalid Input Test]")
#     state_invalid = MissionState()
#     result = launch_step(state_invalid, 150) # Thrust > 100%
    
#     print(f"Result: {result}")
#     print(f"Status: {state_invalid.status}")
#     print(f"Error Code: {state_invalid.error_code}")


# if __name__ == "__main__":
#     test_launch_scenarios()

# test_mission_core.py (Modified)

# ... (Include the test_launch_scenarios function from before) ...
from mission_core import MissionState, launch_step, cruise_step 
def test_cruise_scenarios():
    print("\n--- Running Cruise Scenarios Test ---")

    # Scenario 1: Successful Cruise (3 steps to completion)
    print("\n[Scenario 1: Successful Cruise Test]")
    state_cruise = MissionState()
    
    # Manually transition the state to CRUISE (simulating a prior successful launch)
    state_cruise.status = "CRUISE"
    state_cruise.fuel = 50 
    state_cruise.altitude_km = 399990 # Start very close to the target
    
    result = cruise_step(state_cruise)
    print(f"Result (Step 1): {result}")
    
    # Run again until destination is reached
    result = cruise_step(state_cruise)
    print(f"Result (Step 2): {result}")
    
    print(f"Status: {state_cruise.status}")
    print(f"Mission Day: {state_cruise.mission_day}")
    print(f"Fuel Left: {state_cruise.fuel:.2f}")

    # Scenario 2: Failure - Out of Fuel
    print("\n[Scenario 2: Out of Fuel Failure Test]")
    state_fuel_fail = MissionState()
    state_fuel_fail.status = "CRUISE"
    state_fuel_fail.fuel = 1 # Not enough for 10 days of cruise (needs 5)
    
    result = cruise_step(state_fuel_fail)
    
    print(f"Result: {result}")
    print(f"Status: {state_fuel_fail.status}")
    print(f"Error Code: {state_fuel_fail.error_code}")

if __name__ == "__main__":
    # test_launch_scenarios() # Keep this commented out if you just want to test cruise
    test_cruise_scenarios()