import pygame
import numpy as np
import random as r

pygame.init()

r.seed()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('pygame renderer')
clock = pygame.time.Clock()

camera_position = [0, 0, -10]
camera_direction = [10, 0, 0]
camera_up = [0, 0, 0]

projection_plane_width = 16
projection_plane_height = 9
projection_plane_distance = 0.5

projection_plane_left = -projection_plane_width / 2
projection_plane_right = projection_plane_width / 2
projection_plane_bottom = -projection_plane_height / 2
projection_plane_top = projection_plane_height / 2

class Prism:
    def __init__(self, pos: list[int, int, int], sizeWHD: list[int, int, int], rot: list[int, int, int]):
        self.width = sizeWHD[0]
        self.height = sizeWHD[1]
        self.depth = sizeWHD[2]

        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]

        self.rot = rot[0]
        self.rot2 = rot[1]
        self.rot3 = rot[2]

        self.shape = [
            [(-1*self.width), (1*self.height), (-1*self.depth)], 
            [(-1*self.width), (1*self.height), (1*self.depth)],
            [(1*self.width), (1*self.height), (1*self.depth)],
            [(1*self.width), (1*self.height), (-1*self.depth)],
            [(0*self.width), (-1*self.height), (0*self.depth)],
        ]

        self.vertices = [
            [(-1*self.width), (1*self.height), (-1*self.depth)], 
            [(-1*self.width), (1*self.height), (1*self.depth)],
            [(1*self.width), (1*self.height), (1*self.depth)],
            [(1*self.width), (1*self.height), (-1*self.depth)],
            [(0*self.width), (-1*self.height), (0*self.depth)],
        ]
        
        
        self.faces = [
            [0, 1, 2, 3],
            [4, 1, 0],
            [4, 2, 1],
            [4, 2, 3],
            [4, 0 ,3],
        ]

        self.normals = []
        for face in self.faces:
            face_vertices = [self.vertices[i] for i in face]
            self.normals.append(calculate_normal(face_vertices))

    def update(self, sceneFaces):
        self.normals = []
        for face in self.faces:
            face_vertices = [self.vertices[i] for i in face]
            self.normals.append(calculate_normal(face_vertices))

        if self.rot != 0:
            if self.rot > 6.27:
                self.rot = 0
            if self.rot < -6.27:
                self.rot = 0
        elif self.rot2 != 0:
            if self.rot2 > 6.27:
                self.rot2 = 0
            if self.rot2 < -6.27:
                self.rot2 = 0
        elif self.rot3 != 0:
            if self.rot3 > 6.27:
                self.rot3 = 0
            if self.rot3 < -6.27:
                self.rot3 = 0

        if (self.rot != 0 or self.rot2 != 0 or self.rot3 != 0):
            for i, vertex in enumerate(self.shape):
                self.vertices[i] = rotate_around_axes(vertex, rotation_axis, self.rot, rotation_axis2, self.rot2, rotation_axis3, self.rot3, self.x, self.y, self.z)

        sceneFaces.append([self.vertices, self.faces, self.normals])


class Cube:
    def __init__(self, pos: list[float, float, float], sizeWHD: list[float, float, float], rot: list[float, float, float]):
        self.width = sizeWHD[0]
        self.height = sizeWHD[1]
        self.depth = sizeWHD[2]

        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]

        self.rot = rot[0]
        self.rot2 = rot[1]
        self.rot3 = rot[2]

        self.shape = [
            [(-1*self.width), (-1*self.height), (-1*self.depth)],
            [(-1*self.width), (-1*self.height), (1*self.depth)],
            [(-1*self.width), (1*self.height), (-1*self.depth)],
            [(-1*self.width), (1*self.height), (1*self.depth)],
            [(1*self.width), (-1*self.height), (-1*self.depth)],
            [(1*self.width), (-1*self.height), (1*self.depth)],
            [(1*self.width), (1*self.height), (-1*self.depth)],
            [(1*self.width), (1*self.height), (1*self.depth)],
        ]

        self.vertices = [
            [(-1*self.width), (-1*self.height), (-1*self.depth)],
            [(-1*self.width), (-1*self.height), (1*self.depth)],
            [(-1*self.width), (1*self.height), (-1*self.depth)],
            [(-1*self.width), (1*self.height), (1*self.depth)],
            [(1*self.width), (-1*self.height), (-1*self.depth)],
            [(1*self.width), (-1*self.height), (1*self.depth)],
            [(1*self.width), (1*self.height), (-1*self.depth)],
            [(1*self.width), (1*self.height), (1*self.depth)],
        ]
        

        self.faces = [
            [0, 1, 3, 2],
            [1, 5, 7, 3], 
            [7, 6, 4, 5], 
            [4, 0, 2, 6], 
            [2, 3, 7, 6], 
            [4, 5, 1, 0],
        ]

        self.normals = []
        for face in self.faces:
            face_vertices = [self.vertices[i] for i in face]
            self.normals.append(calculate_normal(face_vertices))

    def update(self, sceneFaces):
        self.normals = []
        for face in self.faces:
            face_vertices = [self.vertices[i] for i in face]
            self.normals.append(calculate_normal(face_vertices))

        if self.rot != 0:
            if self.rot > 6.27:
                self.rot = 0
            if self.rot < -6.27:
                self.rot = 0
        elif self.rot2 != 0:
            if self.rot2 > 6.27:
                self.rot2 = 0
            if self.rot2 < -6.27:
                self.rot2 = 0
        elif self.rot3 != 0:
            if self.rot3 > 6.27:
                self.rot3 = 0
            if self.rot3 < -6.27:
                self.rot3 = 0
        if (self.rot != 0 or self.rot2 != 0 or self.rot3 != 0):
            for i, vertex in enumerate(self.shape):
                self.vertices[i] = rotate_around_axes(vertex, rotation_axis, self.rot, rotation_axis2, self.rot2, rotation_axis3, self.rot3, self.x, self.y, self.z)
                
        sceneFaces.append([self.vertices, self.faces, self.normals])

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

rotation_axis = [1, 0, 0]
rotation_axis2 = [0, 1, 0]
rotation_axis3 = [0, 0, 1]


def rotate_around_axes(vertex, axis1, angle1, axis2, angle2, axis3, angle3, x, y, z):
    c1 = np.cos(angle1)
    s1 = np.sin(angle1)
    t1 = 1 - c1
    x1, y1, z1 = axis1
    rotation_matrix1 = np.array([[t1*x1*x1+c1,   t1*x1*y1-z1*s1, t1*x1*z1+y1*s1],
                                [t1*x1*y1+z1*s1, t1*y1*y1+c1,   t1*y1*z1-x1*s1],
                                [t1*x1*z1-y1*s1, t1*y1*z1+x1*s1, t1*z1*z1+c1  ]])

    c2 = np.cos(angle2)
    s2 = np.sin(angle2)
    t2 = 1 - c2
    x2, y2, z2 = axis2
    rotation_matrix2 = np.array([[t2*x2*x2+c2,   t2*x2*y2-z2*s2, t2*x2*z2+y2*s2],
                                [t2*x2*y2+z2*s2, t2*y2*y2+c2,   t2*y2*z2-x2*s2],
                                [t2*x2*z2-y2*s2, t2*y2*z2+x2*s2, t2*z2*z2+c2  ]])
    
    c3 = np.cos(angle3)
    s3 = np.sin(angle3)
    t3 = 1 - c3
    x3, y3, z3 = axis3
    rotation_matrix3 = np.array([[t3*x3*x3+c3,   t3*x3*y3-z3*s3, t3*x3*z3+y3*s3],
                                [t3*x3*y3+z3*s3, t3*y3*y3+c3,   t3*y3*z3-x3*s3],
                                [t3*x3*z3-y3*s3, t3*y3*z3+x3*s3, t3*z3*z3+c3  ]])
    
    return np.dot(rotation_matrix3, np.dot(rotation_matrix2, np.dot(rotation_matrix1, (vertex[0], vertex[1], vertex[2])))) + [x,y,z]

def calculate_normal(face_vertices):
    v1 = np.array(face_vertices[0])
    v2 = np.array(face_vertices[1])
    v3 = np.array(face_vertices[2])
    return np.cross(v2-v1, v3-v1)

def project_vertex(vertex):
    x = vertex[0] - camera_position[0]
    y = vertex[1] - camera_position[1]
    z = vertex[2] - camera_position[2]
    if (z==0):
        y_proj = y * projection_plane_distance
        x_proj = x * projection_plane_distance
    else: 
        y_proj = y * projection_plane_distance / z
        x_proj = x * projection_plane_distance / z
    

    aspect_ratio = projection_plane_width / projection_plane_height
    y_proj *= aspect_ratio

    return [x_proj, y_proj]

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

def renderFaces(sceneFaces):
    sortedObjs = []
    for obj in sceneFaces:
        for i, face in enumerate(obj[1]):
            face_center = np.mean([obj[0][i] for i in face], axis=0)
            distance = np.linalg.norm(np.array(camera_position) - np.array(face_center))
            if (distance > 1):
                sortedObjs.append((i, obj, distance))
    sortedObjs.sort(key=lambda x: x[2], reverse=True)
    # draw the faces in order of distance from the camera
    

    for i, obj, distance in sortedObjs:
        face = obj[1][i]
        normal = obj[2][i]
        # check if the face is facing towards the camera
        camera_vector = np.array(camera_direction) - np.array(camera_position)
        #if np.dot(normal, camera_vector) > 0:
            #continue
       
        projected_vertices = []
        for vertex in obj[0]:
            projected_vertices.append(project_vertex(vertex))

        points = []
        for vertex_index in face:
            vertex = projected_vertices[vertex_index]
            y = int((vertex[1] + 0.5) * screen.get_height())
            x = int((vertex[0] + 0.5) * screen.get_width())
            newX = clamp(x, -10000, 10000)
            newY = clamp(y, -10000, 10000)
            points.append((newX, newY))
            
        color = colors[i % len(colors)]
        
        pygame.draw.polygon(screen, color, points)

cube = Cube((0, 0, 0), (1, 1, 1), (0, 0, 0))
prism = Prism((2, -2, 1), (1, 1, 1), (1, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            quit()
    
    faces = []

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera_position[2] += 0.1
    if keys[pygame.K_s]:
        camera_position[2] -= 0.1
    if keys[pygame.K_a]:
        camera_position[0] -= 0.1
    if keys[pygame.K_d]:
        camera_position[0] += 0.1
    if keys[pygame.K_SPACE]:
        camera_position[1] -= 0.05
    if keys[pygame.K_LCTRL]:
        camera_position[1] += 0.05
#    if keys[pygame.K_UP]:
#        camera_direction[1] += 0.1
#    if keys[pygame.K_DOWN]:
#        camera_direction[1] -= 0.1
#    if keys[pygame.K_LEFT]:
#        camera_direction[0] += 0.1
#    if keys[pygame.K_RIGHT]:
#        camera_direction[0] -= 0.1
#    if keys[pygame.K_q]:
#        camera_direction[2] += 0.1
#    if keys[pygame.K_e]:
#        camera_direction[2] -= 0.1
            
    screen.fill((31, 31, 31))
    cube.update(faces)

    cube.rot += 0.01
    cube.rot2 += 0.01

    prism.update(faces)
    renderFaces(faces)

    clock.tick(60)
    pygame.display.flip()