import subprocess
import yaml


rooms = None

def run_navigation(x, y, z, w):
    x = str(x)
    y = str(y)
    z = str(z)
    w = str(w)

    python_interpreter = "/usr/bin/python3"

    # Set the path to your Python script
    python_script = "/home/psevm/catkin_ws/src/auto-nav/scripts/goal_pose.py"

    # Run the Python script using the specified interpreter
    subprocess.run(
        [python_interpreter, python_script, x, y, z, w])
    

def navigate_to_room(room: int):
    global rooms
    
    if rooms is None:    
        with open("room_cords.yaml", 'r') as yaml_file:
            rooms = yaml.safe_load(yaml_file)
    
    room_cords = rooms[f"room{room}"]
 
    print(room_cords)
    run_navigation(room_cords["x"], room_cords["y"], room_cords["z"], room_cords["w"])