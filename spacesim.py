import pygame, sys
import math

pygame.init()
WIDTH, HEIGHT = 1000, 800  
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Gravity Sim')
white = (255, 255, 255)
blue = (0,0,255)
yellow = (255,255,0)
grey = (80,70,80)
Font = pygame.font.SysFont('Helvetica',18)
class Planet:
    AU = 149.6e6 * 1000
    grav = 6.6742e-11
    ren_scale = 250 / AU
    time_excel = 3600 * 24  # a second = a day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.sun = False
        self.orbit = []
        self.distance_to_sun = 0
        self.x_v = 0
        self.y_v = 0

    def draw(self,win):
        x = self.x * self.ren_scale + WIDTH / 2
        y = self.y * self.ren_scale + HEIGHT / 2
        z = self.distance_to_sun * self.ren_scale / 2
        if len(self.orbit) > 2:
            upd_point = []
            upd_point_to_sun = []
            for point in self.orbit:
                if len(point) == 3:
                    x, y, z = point
                else:
                    x, y = point
                    z = 0
                x = x * self.ren_scale + WIDTH/2
                y = y * self.ren_scale + WIDTH/2
                z = z * self.ren_scale 
                upd_point.append((x, y))
                upd_point_to_sun.append((self.distance_to_sun * self.ren_scale, z))
            pygame.draw.lines(win,self.color,False,upd_point,2)
        pygame.draw.circle(win,self.color, (x, y), self.radius)
        if not self.sun:
            distance_text = Font.render(f'{round(self.distance_to_sun/1609344,1)}Mile',1,white)
            win.blit(distance_text,(x - distance_text.get_width()/2,y - distance_text.get_width()/2))


    def attract(self,other):
        other_x , other_y = other.x ,other.y
        distance_x = other.x - self.x #find distance
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2) #given that C2=a2+b2
        if other.sun:
            self.distance_to_sun = distance
        force = self.grav * self.mass * other.mass / distance**2 #f=g Mm/r^2
        zeta = math.atan2(distance_y,distance_x)
        #triangulate forces 
        force_x = math.cos(zeta)*force
        force_y = math.sin(zeta)*force
        return force_x,force_y
    
    def upd_position(self,planet):
        total_fx = total_fy = 0
        for planet in planet:
            if self == planet:
                continue
            fx,fy = self.attract(planet)
            total_fx += fx
            total_fy += fy
        #velosity
        self.x_v += total_fx / self.mass * self.time_excel
        self.y_v += total_fy / self.mass * self.time_excel
        #calculate position
        self.x += self.x_v * self.time_excel
        self.y += self.y_v * self.time_excel
        self.orbit.append((self.x,self.y))
    def distance_to_Star(self,planet):
        absolute_dist = self.x - self.distance_to_sun
        upd_point_to_sun = []
        for planet in planet : 
            if self == planet :
                continue
            upd_point_to_sun.append((self.distance_to_sun,absolute_dist))
        pygame.draw.lines(win,self.color,False,upd_point_to_sun,2)


def main():
    run = True
    frame_sync = pygame.time.Clock()
    Sun = Planet(0, 0, 30, white, 1.9889 * 10**30)  # using real mass
    Sun.sun = True
    Earth = Planet(-1.2* Planet.AU,0,16,blue,5.98 * 10**24 )
    Earth.y_v=24.0 * 1000
    commet = Planet(-2*Planet.AU,0,5,white,7.348 * 10**24 )
    commet.y_v=11.1 * 1000
    Venus = Planet(-0.8*Planet.AU,1,14,yellow,4.867 * 10**24 )
    Venus.y_v=30.0 * 1000
    mercury=Planet(-0.387*Planet.AU,0,8,grey,3.30 * 10**23)
    mercury.y_v=47.0 * 1000
    planets = [Sun,Earth,mercury,commet,Venus]
    
    while run:
        frame_sync.tick(60)
        win.fill((0, 0, 0))

        for event in pygame.event.get():  # check if the game is in a running state, if not, exit
            if event.type == pygame.QUIT:
                run = False 

        for planet in planets: 
            planet.upd_position(planets)
            planet.distance_to_Star(planets)
            planet.draw(win)

        pygame.display.update()

    pygame.quit()

main()
