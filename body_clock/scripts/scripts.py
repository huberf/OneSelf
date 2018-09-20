import math

def clock_x_y(hour):
    around = hour / 24.0
    sin = math.sin(around*2*3.141592654)
    cos = math.cos(around*2*3.141592654)
    x2 = 300*sin + 300
    x1 = (300-30)*sin + 300
    y2 = -(300)*cos + 300
    y1 = -(300-30)*cos + 300
    #print("Hour:", hour, "--", "x1:", x1, "y1:", y1, "x2:", x2, "y2:", y2)
    print('<line id="hour{hour}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"></line>'.format(hour=hour, x1=x1, y1=y1, x2=x2, y2=y2))

# Generate lines for all 24 hours
for i in range(0, 24):
    clock_x_y(i)
