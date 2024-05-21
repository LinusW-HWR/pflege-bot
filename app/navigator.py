import subprocess
import yaml



def load_rooms():
    with open("room_cords.yaml", 'r') as yaml_file:
        return yaml.safe_load(yaml_file)

def load_base():
    with open("base_cords.yaml", 'r') as yaml_file:
        return yaml.safe_load(yaml_file)

rooms = load_rooms()
base = load_base()

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
    

def navigate_to_room(room: str):
    global rooms
    
    if room == "base":
        room_cords = base
    else:
        room_cords = rooms[room]
 
    print(f"{room}: {room_cords}")
    run_navigation(room_cords["x"], room_cords["y"], room_cords["z"], room_cords["w"])