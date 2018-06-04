'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform
from path import Path

AGENT_MODES = {
    KEY._1: 'seek',
    KEY._2: 'arrive_slow',
    KEY._3: 'arrive_normal',
    KEY._4: 'arrive_fast',
    KEY._5: 'flee',
    #KEY._6: 'pursuit'
    KEY._7: 'follow_path',
    KEY._8: 'wander'
}


class Agent(object):

    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.9,
        'normal': 0.5,
        'fast': 0.1
    }

    def __init__(self, world=None, scale=30.0, mass=1.0, mode='seek'):
        # keep a reference to the world object
        self.world = world
        self.mode = mode
        # where am i and where am i going? random
        dir = radians(random()*360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.force = Vector2D()  # current steering force
        self.acceeration = Vector2D()  # current steering force
        self.mass = mass
        # limits?
        self.max_speed = 20.0 * scale
        self.max_force = 500.0
        # data for drawing this agent
        self.color = 'ORANGE'
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]
        self.path = Path()
        self.randomise_path()
        self.waypoint_threshold = 50.0
        self.show_info = False
        self.wander_target = Vector2D(1, 0)
        self.wander_dist = 1.0 * scale
        self.wander_radius = 1.0 * scale
        self.wander_jitter = 10.0 * scale
        self.bRadius = scale

    def randomise_path(self):
        cx = self.world.cx
        cy = self.world.cy
        margin = min(cx, cy) * (1/6)
        pathpoints = randrange(2, 10)
        self.path.create_random_path(pathpoints, (0+margin), (0+margin), (cx-margin), (cy-margin))

    def calculate(self, delta):
        # reset the steering force
        mode = self.mode
        if mode == 'seek':
            force = self.seek(self.world.target)
        elif mode == 'arrive_slow':
            force = self.arrive(self.world.target, 'slow')
        elif mode == 'arrive_normal':
            force = self.arrive(self.world.target, 'normal')
        elif mode == 'arrive_fast':
            force = self.arrive(self.world.target, 'fast')
        elif mode == 'flee':
            force = self.flee(self.world.target)
##        elif mode == 'pursuit':
##            force = self.pursuit(self.world.hunter)
        elif mode == 'follow_path':
            force = self.follow_path()
        elif mode == 'wander':
            force = self.wander(delta)
        else:
            force = Vector2D()
        force.x /= self.mass
        force.y /= self.mass
        self.force = force
        return force

    def update(self, delta):
        ''' update vehicle position and orientation '''
        force = self.calculate(delta)
        force.truncate(self.max_force)
        # new velocity
        self.vel += force * delta
        # check for limits of new velocity
        self.vel.truncate(self.max_speed)
        # update position
        self.pos += self.vel * delta
        # update heading is non-zero velocity (moving)
        if self.vel.length_sq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()
        # treat world as continuous space - wrap new position if needed
        self.world.wrap_around(self.pos)

    def render(self, color=None):
        ''' Draw the triangle agent with color'''
        if self.mode == 'follow_path':
            self.path.render()
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)

        if self.mode == 'wander':
            wnd_pos = Vector2D(self.wander_dist, 0)
            wld_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)
            egi.green_pen()
            egi.circle(wld_pos, self.wander_radius)
            egi.red_pen()
            wnd_pos = (self.wander_target + Vector2D(self.wander_dist, 0))
            wld_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)
            egi.circle(wld_pos, 3)
        # draw it!
        egi.closed_shape(pts)

        if self.show_info:
            s = 0.5 # <-- scaling factor
            # force
            egi.red_pen()
            egi.line_with_arrow(self.pos, self.pos + self.force * s, 5)
            # velocity
            egi.grey_pen()
            egi.line_with_arrow(self.pos, self.pos + self.vel * s, 5)
            # net (desired) change
            egi.white_pen()
            egi.line_with_arrow(self.pos+self.vel * s, self.pos+ (self.force+self.vel) * s, 5)
            egi.line_with_arrow(self.pos, self.pos+ (self.force+self.vel) * s, 5)

    def speed(self):
        return self.vel.length()

    #--------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def flee(self, hunter_pos):
        ''' move away from hunter position '''
        if ((self.pos.x < hunter_pos.x + 100) and (self.pos.x > hunter_pos.x - 100)):
            if ((self.pos.y < hunter_pos.y + 100) and (self.pos.y > hunter_pos.y - 100)):
                desired_vel = (self.pos - hunter_pos).normalise() * self.max_speed
                return (desired_vel - self.vel)
        return Vector2D()

    def arrive(self, target_pos, speed):
        ''' this behaviour is similar to seek() but it attempts to arrive at
            the target position with a zero velocity'''
        decel_rate = self.DECELERATION_SPEEDS[speed]
        to_target = target_pos - self.pos
        dist = to_target.length()
        if dist > 0:
            # calculate the speed required to reach the target given the
            # desired deceleration rate
            speed = dist / decel_rate
            # make sure the velocity does not exceed the max
            speed = min(speed, self.max_speed)
            # from here proceed just like Seek except we don't need to
            # normalize the to_target vector because we have already gone to the
            # trouble of calculating its length for dist.
            desired_vel = to_target * (speed / dist)
            return (desired_vel - self.vel)
        return Vector2D(0, 0)

    def pursuit(self, evader):
        ''' this behaviour predicts where an agent will be in time T and seeks
            towards that point to intercept it. '''
## OPTIONAL EXTRA... pursuit (you'll need something to pursue!)
        return Vector2D()

    def follow_path(self):
        to_point = self.path.current_pt() - self.pos
        dist = to_point.length()
        if self.path.is_finished():
            decel_rate = self.DECELERATION_SPEEDS['normal']
            if dist > 0:
                # calculate the speed required to reach the target given the
                # desired deceleration rate
                speed = dist / decel_rate
                # make sure the velocity does not exceed the max
                speed = min(speed, self.max_speed)
                # from here proceed just like Seek except we don't need to
                # normalize the to_target vector because we have already gone to the
                # trouble of calculating its length for dist.
                desired_vel = to_point * (speed / dist)
                return (desired_vel - self.vel)
            return Vector2D(0, 0)
        else:
            if dist < self.waypoint_threshold:
                self.path.inc_current_pt()
            desired_vel = to_point.normalise() * self.max_speed
            return (desired_vel - self.vel)
                
    def wander(self, delta):
        wt = self.wander_target
        jitter_tts = self.wander_jitter * delta
        wt += Vector2D(uniform(-1, 1) * jitter_tts, uniform(-1, 1) * jitter_tts)
        wt.normalise()
        wt *= self.wander_radius
        target = wt + Vector2D(self.wander_dist, 0)
        wld_target = self.world.transform_point(target, self.pos, self.heading, self.side)
        return self.seek(wld_target)
