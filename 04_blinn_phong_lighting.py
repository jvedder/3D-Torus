#  Copyright (c) 2025 John Vedder
#  MIT License

import numpy as np
from PIL import Image

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
    
    #return point, normal / np.linalg.norm(normal)  # Just in case
    return point, normal 

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


max_intensity = 0.0
grey = np.full( (1024, 1024), 192, dtype=np.uint8)

phi_steps   = int(np.ceil( 2.0 * np.pi * (R+r) * pix_scale * 1.414))
theta_steps = int(np.ceil( np.pi * r * pix_scale * 1.414))

print ('phi steps  ', phi_steps)
print ('theta steps', theta_steps)

step = 0
for phi in np.linspace(0, 2.0*np.pi, phi_steps):
    step = step +1
    print(step, round(max_intensity,2))
    for theta in np.linspace(0.0, np.pi, theta_steps):

        #point on torus    
        point, normal = torus_point_and_normal(phi, theta)

        # Compute illumination
        intensity = blinn_phong_illumination(point, normal)
        max_intensity = max(max_intensity,intensity)

        #set pixel
        x = 512 + int(point[0] * pix_scale)
        y = 512 + int(point[1] * pix_scale)
        i = 64 + int(192 * intensity)
        i = min(max(i,0),255)
        grey[y,x] = i

image = Image.fromarray(grey, mode='L')
image.save('torus.png')



