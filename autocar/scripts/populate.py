import json
import sys

LANE_OFFSET_Y = 3.0
FIRST_LANE_Y = 24.5

if len(sys.argv) < 2:
    print("Please specify the config file.")

config_path = sys.argv[1]

with open(config_path, 'r') as f:
    config = json.load(f)


y_lane = FIRST_LANE_Y


poses = [(config["autonomous_car_start_pos"], y_lane)]
count = 1

for i in range(config["num_lanes"]):
    num_car_lane = config['num_cars_per_lane'][i]
    for j in range(num_car_lane):
        x = config["car_start_poses"][i][j]
        pos = (x, y_lane)
        poses.append(pos)
        count += 1

    y_lane -= LANE_OFFSET_Y

print("1 autonomous car + %d other cars." % (count-1))

# --------- Generating .world file ------------------------

with open('../maps/world/world_base.world', 'r') as f:
    world_base = f.read()

with open('../maps/world/_active_world.world', 'w') as f:
    f.write(world_base + '\n')
    s = "gc( pose [%.1f %.1f 0.0 0.0] name \"car%d\" color \"red\")\n" % (poses[0][0], poses[0][1], 0)
    f.write(s)

    for i in range(1,count):
        s = "gc( pose [%.1f %.1f 0.0 0.0] name \"car%d\" color \"green\")\n" % (poses[i][0], poses[i][1], i)
        f.write(s)

# --------- Generating .launch file ------------------------

with open("../launch/launchfile_base", 'r') as f:
    launchfile_base = f.read()

with open("../launch/template", 'r') as f:
    template = f.read()

with open("../launch/_active_launchfile.launch", 'w') as f:

    f.write("<launch>\n")
    f.write(launchfile_base + '\n')

    for i in range(1,count):
        formatted = (template % (i,i,i,i,i,i)) + '\n'
        f.write(formatted)
    
    f.write("</launch>\n")

# --------- Generating .rviz file ------------------------

with open("../maps/rviz_settings/rviz_base_upper", "r") as f:
    base_upper = f.read()
with open("../maps/rviz_settings/rviz_base_lower", "r") as f:
    base_lower = f.read()
with open("../maps/rviz_settings/template", "r") as f:
    template = f.read()

with open("../maps/rviz_settings/_active_rviz.rviz", 'w') as f:

    f.write(base_upper + '\n')

    for i in range(1,count):
        formatted = (template % (i,i)) + '\n'
        f.write(formatted)
    
    f.write(base_lower + '\n')




    


