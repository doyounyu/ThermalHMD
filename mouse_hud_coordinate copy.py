import cv2
import numpy as np
import math
# Callback function to capture mouse movements
w = 800
h = 600
off = 50 # offset ----___x

l = w/2 - off + 100 # length of artificial horizon line
lp = 100  # pitch line length
spacep = 100 # pitch line spacing
pc = 100 # pitch constant

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (w, h))
def dottedLine(img, pt1, pt2, color, thickness=1, gap=10, dot_length=12):
    """
    Draw a dotted line using small lines with OpenCV

    Parameters:
    - img: Image on which to draw
    - pt1: The first point of the line segment (x, y)
    - pt2: The second point of the line segment (x, y)
    - color: Line color
    - thickness: Line thickness
    - gap: Distance between dots (actually small lines here)
    - dot_length: Length of each small line segment used as a dot
    """
    # Calculate the Euclidean distance between the two points using sqrt for compatibility
    dist = math.sqrt((pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2)
    # Calculate the number of dots needed, adjusted for the gap and dot length
    dots = int(dist / (gap + dot_length))
    
    # Calculate the step size for x and y, including both gap and dot_length
    stepx = (pt2[0] - pt1[0]) / (dots + 1)
    stepy = (pt2[1] - pt1[1]) / (dots + 1)
    
    for i in range(dots):
        # Start point of the current small line
        start_x = int(pt1[0] + stepx * i)
        start_y = int(pt1[1] + stepy * i)
        # End point of the current small line, based on dot_length
        end_x = int(start_x + stepx/(gap+dot_length) * dot_length)
        end_y = int(start_y + stepy/(gap+dot_length) * dot_length)
        # Draw the small line segment
        cv2.line(img, (start_x, start_y), (end_x, end_y), color, thickness)

    return img

def draw_number(img, number, top_left, scale=1):
    # Define low poly points for each number, scaled and translated
    points = {
        '0': [(1, 1), (1, 3), (2, 4), (4, 4), (5, 3), (5, 1), (4, 0), (2, 0)],
        '1': [(3, 0), (3, 4)],
        '2': [(1, 3), (2, 4), (4, 4), (5, 3), (1, 0), (5, 0)],
        '3': [(1, 4), (4, 4), (3, 2), (4, 0), (1, 0)],
        '4': [(4, 4), (4, 0), (1, 2), (5, 2)],
        '5': [(5, 4), (1, 4), (1, 2), (4, 2), (4, 0), (1, 0)],
        '6': [(4, 4), (2, 2), (4, 2), (5, 1), (4, 0), (2, 0), (1, 1), (2, 2)],
        '7': [(1, 4), (5, 4), (3, 0)],
        '8': [(3, 2), (1, 4), (4, 4), (5, 2), (4, 0), (1, 0), (2, 2), (3, 2), (3, 4), (3, 0)],
        '9': [(2, 0), (4, 2), (2, 2), (1, 3), (2, 4), (4, 4), (5, 3), (4, 2)]
    }

    if str(number) in points:
        for i, point in enumerate(points[str(number)]):
            next_point = points[str(number)][(i + 1) % len(points[str(number)])]
            cv2.line(img, 
                     (int(top_left[0] + point[0] * scale), int(top_left[1] + point[1] * scale)), 
                     (int(top_left[0] + next_point[0] * scale), int(top_left[1] + next_point[1] * scale)), 
                     (255, 255, 255), 2)

def draw_following_square(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        # Create a new black image to avoid drawing over the previous square
        temp_img = np.zeros((h, w, 3), np.uint8)
        # Draw a green square at the mouse location
        cv2.circle(temp_img, (x, y), 10, (0,255,0), 1)
        # cv2.circle(temp_img, (int(w/2), int(h/2)),100,(0, 255, 0), 1)
        roll  = (x - w/2)/(w/2)*np.pi
        pitch = (y - h/2)/(h/2)*np.pi
        
        print(f"pitch: {pitch*57.2958} roll: {roll*57.2958}")
        
        cos_roll = np.cos(roll)
        sin_roll = np.sin(roll)
        y_ofst = pc*pitch

        
        p1 = (int(-off*cos_roll+w/2 -     y_ofst*sin_roll), int(y_ofst*cos_roll -off*sin_roll+h/2))
        p2 = (int(-(off+l)*cos_roll+w/2 - y_ofst*sin_roll), int(y_ofst*cos_roll-(off+l)*sin_roll+h/2))

        p3 = (int(off*cos_roll+w/2 -      y_ofst*sin_roll), int(y_ofst*cos_roll+ off*sin_roll+h/2))
        p4 = (int((off+l)*cos_roll+w/2 -  y_ofst*sin_roll), int(y_ofst*cos_roll+ (off+l)*sin_roll+h/2))

        cv2.line(temp_img, p1, p2, (0,255,0), 1) #left artificial horizon
        cv2.line(temp_img, p3, p4, (0,255,0), 1) #right artificial horizon
        #draw_number(temp_img, 3, p1, 5)
        for i in range(1,7):
            

            y_ofst = pc * pitch - i*spacep
            # x1 = -off
            # y1 = pc*pitch --> i*spacep
            # x2 = -off+lp
            # y2 = pc*pitch
            cent_ofst = 20 #center point offset. 
            
            x1 = (int(-off*cos_roll+w/2 -     (y_ofst+cent_ofst)*sin_roll), int((y_ofst+cent_ofst)*cos_roll -off*sin_roll+h/2))
            x2 = (int(-(off+lp)*cos_roll+w/2 - y_ofst*sin_roll), int(y_ofst*cos_roll-(off+lp)*sin_roll+h/2))

            x3 = (int(off*cos_roll+w/2 -     (y_ofst+cent_ofst)*sin_roll), int((y_ofst+cent_ofst)*cos_roll+ off*sin_roll+h/2))
            x4 = (int((off+lp)*cos_roll+w/2 -  y_ofst*sin_roll), int(y_ofst*cos_roll+ (off+lp)*sin_roll+h/2))
            
            print(f'x1: {x1}, x2: {x2}, x3: {x3}, x4: {x4}')
            #cv2.putText(temp_img, str(i*10), x2, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1 ) # pitch degree
            cv2.putText(temp_img, str(i*10), (x4[0]-20, x4[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1 ) # pitch degree
            
            cv2.line(temp_img, x1, x2, (0,255,0), 1) #left artificial horizon
            cv2.line(temp_img, x3, x4, (0,255,0), 1) #right artificial horizon
            
        for i in range(1,7):
            

            y_ofst = pc * pitch + i*spacep
            # x1 = -off
            # y1 = pc*pitch --> i*spacep
            # x2 = -off+lp
            # y2 = pc*pitch
            cent_ofst = -20 #center point offset. 
            
            x1 = (int(-off*cos_roll+w/2 -     (y_ofst+cent_ofst)*sin_roll), int((y_ofst+cent_ofst)*cos_roll -off*sin_roll+h/2))
            x2 = (int(-(off+lp)*cos_roll+w/2 - y_ofst*sin_roll), int(y_ofst*cos_roll-(off+lp)*sin_roll+h/2))

            x3 = (int(off*cos_roll+w/2 -     (y_ofst+cent_ofst)*sin_roll), int((y_ofst+cent_ofst)*cos_roll+ off*sin_roll+h/2))
            x4 = (int((off+lp)*cos_roll+w/2 -  y_ofst*sin_roll), int(y_ofst*cos_roll+ (off+lp)*sin_roll+h/2))
            
            print(f'x1: {x1}, x2: {x2}, x3: {x3}, x4: {x4}')
            #cv2.putText(temp_img, str(i*10), x2, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1 ) # pitch degree
            cv2.putText(temp_img, str(i*10), (x4[0]-20, x4[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1 ) # pitch degree
            
            dottedLine(temp_img, x1, x2, (0,255,0), 1) #left artificial horizon
            dottedLine(temp_img, x3, x4, (0,255,0), 1) #right artificial horizon


        cv2.putText(temp_img, f"PITCH:  {round(pitch*57.2958)}DEG", (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(temp_img, f"ROLL:   {round(roll*57.2958)}DEG", (10, h - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        print(f"p1: {p1} p2: {p2}")
        ##cv2.putText(temp_img, "f'PITCH :+ {round(pitch)}' ")
        out.write(temp_img)

        cv2.imshow("Image", temp_img)

# Create a black image
img = np.zeros((800, 600, 3), np.uint8)
cv2.namedWindow("Image")

# Set the mouse callback function
cv2.setMouseCallback("Image", draw_following_square)

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
out.release()
