#  Copyright (c) 2025 John Vedder
#  MIT License

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

#  ka, kd, and ks are ambient, diffuse, and specular coefficients
ka=0.1
kd=0.7
ks=0.2

# Ia and Il are ambient light and light intensity
Ia=0.2
Il=1.0

# shininess exponent (higher = sharper highlights)
shininess=32

# Define light and viewer positions
light_pos = np.array([25.0, 25.0, 25.0])
view_pos  = np.array([ 0.0,  0.0, 25.0])

# Define Torus major radius and minor (tube) radius
R=10.0
r=3.0

# Pixels per geometry unit
pix_scale = 30

# Define text size
text_size = 32
text_line_height = 40
text_color = 0

def torus_point_and_normal(phi, theta):
    # phi is around the torus
    # theta is around the tube
    
    # Point on the torus
    x = (R + r * np.cos(theta)) * np.cos(phi)
    y = (R + r * np.cos(theta)) * np.sin(phi)
    z = r * np.sin(theta)
    point = np.array([x, y, z])
    
    # Normal vector (unit)
    nx = np.cos(phi) * np.cos(theta)
    ny = np.sin(phi) * np.cos(theta)
    nz = np.sin(theta)
    normal = np.array([nx, ny, nz])

    #compute black/white stripes 
    color = int(128 * np.sin(16 * phi)) + 128
    color = min(max(color,0),255)
    
    
    #return point, normal / np.linalg.norm(normal)  # Just in case
    return (point, normal, color) 

def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm != 0 else v

def blinn_phong_illumination(point, normal):
    # Vectors
    L = normalize(light_pos - point)
    V = normalize(view_pos - point)
    #V = np.array([0.0, 0.0, 1.0])
    H = normalize(L + V)

    # Terms
    ambient = ka * Ia
    diffuse = kd * Il * max(0.0, np.dot(normal, L))
    specular = ks * Il * max(0.0, np.dot(normal, H)) ** shininess

    return ambient + diffuse + specular


min_intensity = 9999.0
max_intensity = 0.0

min_grey = 9999
max_grey = 0

# Size is (y,x), 192 is default background color (#C0C0C0)
grey = np.full( (1024 + 3*text_line_height, 1024), 192, dtype=np.uint8)

# Compute angle step size to cove all pixels
phi_steps   = int(np.ceil( 2.0 * np.pi * (R+r) * pix_scale * 1.414))
theta_steps = int(np.ceil( np.pi * r * pix_scale * 1.414))

print ('Phi Steps:', phi_steps)
print ('Theta Steps:', theta_steps)

step = 0
start_time = datetime.now()
print("Start Time:", start_time)
for phi in np.linspace(0, 2.0*np.pi, phi_steps):
    for theta in np.linspace(0.0, np.pi, theta_steps):

        #point on torus    
        (point, normal, color) = torus_point_and_normal(phi, theta)

        # Compute illumination
        intensity = blinn_phong_illumination(point, normal)
        min_intensity = min(min_intensity,intensity)
        max_intensity = max(max_intensity,intensity)

        # compute grey scale
        g = int(color/3) + int(192 * intensity)
        #g = int(color * intensity)
        min_grey = min(min_grey,g)
        max_grey = max(max_grey,g)
        g = min(max(g,0),255)

        #set pixel
        x = 512 + int(point[0] * pix_scale)
        y = 512 + int(point[1] * pix_scale)
        grey[y,x] = g

end_time = datetime.now()
print("End Time:", end_time)
run_time_sec = (end_time-start_time).total_seconds()
print("Compute Run Time:", round(run_time_sec,3) ,"sec.") 

print("Intensity Range:",round(min_intensity,2), round(max_intensity,2))
print("Grey Range:",min_grey, max_grey)

print("Creating Image...")
image = Image.fromarray(grey, mode='L')

# Label Image
print("Labeling Image...")
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("arial.ttf", text_size)

text = datetime.now().strftime('%m/%d/%Y %H:%M')
text_position = (10, 10)
draw.text(text_position, text, fill=text_color, font=font)

text = 'color = int(128 * np.sin(16*phi)) + 128'
text_position = (10, 1024 + 0 * text_line_height)
draw.text(text_position, text, fill=text_color, font=font)

text = 'grey = int(color/3) + int(192 * intensity)'
text_position = (10, 1024 + 1 * text_line_height)
draw.text(text_position, text, fill=text_color, font=font)

text = 'Intensity: (' + str(round(min_intensity,2)) +', ' + str(round(max_intensity,2)) + '); '
text += 'Grey: (' + str(min_grey) + ', ' + str(max_grey) + '); ' 
text_position = (10, 1024 + 2 * text_line_height)
draw.text(text_position, text, fill=text_color, font=font)

print("Saving Image...")
image.save('torus-stripes.png')

print("Done.")



