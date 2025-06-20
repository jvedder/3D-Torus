#  Copyright (c) 2025 John Vedder
#  MIT License

import numpy as np
from PIL import Image

#  ka, kd, and ks are ambient, diffuse, and specular coefficients
ka = 0.1
kd = 0.7
ks = 0.2

# Ia and Il are ambient light and light intensity
Ia = 0.2
Il = 1.0

# shininess exponent (higher = sharper highlights)
shininess = 32

# Define light and viewer positions
light_pos = np.array([25.0, 25.0, 25.0])
view_pos  = np.array([ 0.0,  0.0, 25.0])

# Define Torus major radius, minor (tube) radius, bulb radius
R = 10.0
r = 3.0
rb = 0.25

# Pixels per geometry unit
pix_scale = 30


def torus_point_and_normal(phi, theta, bulbs):
    # phi is around the torus
    # theta is around the tube

    # Option1: Modulate minor r with phi to create bulbs
    re = r + rb * np.sin(float(bulbs) * phi)

    # Option 2: Modulate minor r by +/-rb as f(phi) to create bulbs
    # compute effective minor radius, re
    # re = r + 2.0 * abs(rb * np.sin(float(bulbs) * phi)) - 1.0
    
    # Point on the torus
    x = (R + re * np.cos(theta)) * np.cos(phi)
    y = (R + re * np.cos(theta)) * np.sin(phi)
    z = re * np.sin(theta)
    point = np.array([x, y, z])
    
    # Normal vector (unit)
    # TODO: need to adjust for bulbous slope in theta
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


def set_pixel(grey, point, intensity):
    x = 512 + int(point[0] * pix_scale)
    y = 512 + int(point[1] * pix_scale)
    i = 64 + int(192 * intensity)
    i = min(max(i,0),255)
    grey[y,x] = i


def make_image(bulbs):
    # Calculate required number of steps
    phi_steps   = int(np.ceil( 2.0 * np.pi * (R+r+rb) * pix_scale * 1.414))
    theta_steps = int(np.ceil( np.pi * (r+rb) * pix_scale * 1.414))

    # background is a light grey (#C0C0C0)
    grey = np.full( (1024, 1024), 192, dtype=np.uint8)
    
    for phi in np.linspace(0, 2.0*np.pi, phi_steps):
        for theta in np.linspace(0.0, np.pi, theta_steps):

            #point on torus
            point, normal = torus_point_and_normal(phi, theta, bulbs)

            # Compute illumination
            intensity = blinn_phong_illumination(point, normal)

            #set pixel intensity
            set_pixel(grey, point, intensity)

    image = Image.fromarray(grey, mode='L')
    image.save('bulbs-' + str(bulbs) +'.png')


for bulbs in range(1,12):
    print ('bulbs-abs-', bulbs)
    make_image(bulbs)
print ('Done.')

