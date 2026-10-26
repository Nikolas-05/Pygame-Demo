# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 17:07:49 2026

@author: andre
"""

import pygame as pg
import Lasers

try:
    from pygame._sdl2 import controller as sdl_controller
except ImportError:
    sdl_controller = None

DEADZONE = 0.4                 # how far the stick must be pushed to count
JUMP_BUTTON = 0                # plain joysticks: the button numbers, as on an Xbox controller
THROW_BUTTON = 2
_pads = []                     # (device, is it a gamepad?) for each connected controller
_pad_count = -1
_gamepad_ids = set()           # instance ids of the controllers opened as gamepads
PAD_NAMES = {}                 # SDL gamepad button -> 'a', 'b', 'x', 'y', 'back' or 'start'
JOY_NAMES = {0: 'a', 1: 'b', 2: 'x', 3: 'y', 6: 'back', 7: 'start'}   # plain joysticks, Xbox order

def open_pads():
    # opens every connected controller (again whenever one is plugged in or unplugged)
    global _pads, _pad_count, PAD_NAMES
    count = pg.joystick.get_count()
    if count == _pad_count: return
    _pad_count, _pads = count, []
    _gamepad_ids.clear()
    if sdl_controller:
        try:
            if not sdl_controller.get_init(): sdl_controller.init()
            PAD_NAMES = {pg.CONTROLLER_BUTTON_A: 'a', pg.CONTROLLER_BUTTON_B: 'b', pg.CONTROLLER_BUTTON_X: 'x',
                         pg.CONTROLLER_BUTTON_Y: 'y', pg.CONTROLLER_BUTTON_BACK: 'back',
                         pg.CONTROLLER_BUTTON_START: 'start'}
        except Exception:
            pass
    for i in range(count):
        try:
            if sdl_controller and sdl_controller.is_controller(i):
                pad = sdl_controller.Controller(i)
                _gamepad_ids.add(pad.as_joystick().get_instance_id())
                _pads.append((pad, True))
            else:
                _pads.append((pg.joystick.Joystick(i), False))
        except Exception:
            pass
def get_controller():
    # the first connected controller as (device, is it a gamepad?), or (None, False)
    open_pads()
    return _pads[0] if _pads else (None, False)
def pad_button(event):
    # which controller button an event is a press of: 'a', 'b', 'x', 'y', 'back', 'start', or
    # None (not a press, or another button). a gamepad's presses come as CONTROLLERBUTTONDOWN;
    # SDL sends them as JOYBUTTONDOWN too, which is only used for plain joysticks
    if event.type == getattr(pg, 'CONTROLLERBUTTONDOWN', -1):
        return PAD_NAMES.get(event.button)
    if event.type == pg.JOYBUTTONDOWN and getattr(event, 'instance_id', None) not in _gamepad_ids:
        return JOY_NAMES.get(event.button)
    return None


def read_controls():
    # {'left', 'right', 'up', 'down', 'jump', 'throw'}: True while held. the controller if there
    # is one, otherwise the arrow keys, SPACE and F
    pad, gamepad = get_controller()
    if pad and gamepad:
        # left stick (-32768..32767) or D-pad; A / Cross jumps, X / Square throws
        x = pad.get_axis(pg.CONTROLLER_AXIS_LEFTX) / 32767
        y = pad.get_axis(pg.CONTROLLER_AXIS_LEFTY) / 32767
        b = lambda button: bool(pad.get_button(button))
        return {'left': x < -DEADZONE or b(pg.CONTROLLER_BUTTON_DPAD_LEFT),
                'right': x > DEADZONE or b(pg.CONTROLLER_BUTTON_DPAD_RIGHT),
                'up': y < -DEADZONE or b(pg.CONTROLLER_BUTTON_DPAD_UP),
                'down': y > DEADZONE or b(pg.CONTROLLER_BUTTON_DPAD_DOWN),
                'shoot': b(pg.CONTROLLER_BUTTON_X)}
                # 'jump': b(pg.CONTROLLER_BUTTON_A), 'throw': b(pg.CONTROLLER_BUTTON_X)}
    if pad:
        x = pad.get_axis(0) if pad.get_numaxes() > 0 else 0
        y = pad.get_axis(1) if pad.get_numaxes() > 1 else 0
        hx, hy = pad.get_hat(0) if pad.get_numhats() > 0 else (0, 0)     # D-pad: hat y is +1 for up
        button = lambda b: bool(pad.get_button(b)) if pad.get_numbuttons() > b else False
        return {'left': x < -DEADZONE or hx < 0, 'right': x > DEADZONE or hx > 0,
                'up': y < -DEADZONE or hy > 0, 'down': y > DEADZONE or hy < 0,
                'shoot': button(THROW_BUTTON)}
                # 'jump': button(JUMP_BUTTON), 'throw': button(THROW_BUTTON)}
    keys = pg.key.get_pressed()
    return {'left': keys[pg.K_LEFT], 'right': keys[pg.K_RIGHT], 'up': keys[pg.K_UP],
            'down': keys[pg.K_DOWN], 'shoot': keys[pg.K_SPACE]}  #, 'jump': keys[pg.K_SPACE], 'throw': keys[pg.K_f]}


PLAYER_WIDTH = 40              # the spaceship image is big, so it is scaled down to this width


class Spaceship(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.controls = {'left': False, 'right': False, 'up': False, 'down': False, 'shoot': False}
        self.speed = 4
        image = pg.image.load('Demo_images/spaceship.PNG').convert_alpha()
        height = round(image.get_height() * PLAYER_WIDTH / image.get_width())
        self.image = pg.transform.smoothscale(image, (PLAYER_WIDTH, height))
        self.rect = self.image.get_rect(midbottom=(200, 400))
        self.lasers = []
        self.scroll = 0                        # added: sideways scroll, read by Main.py
        self.last_laser_timer = 0
        self.time_bt_shot = 0.2                # seconds between shots

    def spaceship_imput(self, obstacles):
        self.controls = keys = read_controls()

        self.moving = False
        self.scroll = 0                        # added: how far the world slides sideways this frame
        if keys['left']:
            self.scroll = -self.speed          # adjusted: the ship stays put and the world scrolls instead
            self.moving = True
        if keys['right']:
            self.scroll = self.speed           # adjusted: the ship stays put and the world scrolls instead
            self.moving = True
        if keys['up']:
            self.rect.y -= self.speed
            self.moving = True
        if keys['down']:
            self.rect.y += self.speed
            self.moving = True
        if keys['shoot'] and (pg.time.get_ticks()-self.last_laser_timer)/1000 > self.time_bt_shot:
            self.lasers.append(Lasers.Laser(self.rect.centerx, self.rect.top, owner=self))
            self.last_laser_timer = pg.time.get_ticks()

        for obs in obstacles:
            if self.rect.colliderect(obs.rect):
                if self.rect.centerx < obs.rect.centerx: self.rect.right = obs.rect.left
                else: self.rect.left = obs.rect.right

    def update(self, screen_size=(800, 400), obstacles=()):
        self.spaceship_imput(obstacles)
        # keep the ship on the screen
        self.rect.clamp_ip(pg.Rect((0, 0), screen_size))
