import os
import pickle

import pygame

local_path = os.path.join(os.path.abspath(""), "cache.pixeldungeon")

default_zero_surface = pygame.Surface((0,0), pygame.SRCALPHA)

def check_func_name(func, context):
    if (func_name := func.__qualname__) not in cache.keys():
        func_cache = {}
        cache[func_name] = func_cache
        return check_func_name(func, context)
    elif context not in cache[func_name].keys():
        func_cache = {}
        if context == "surface":
            surfaces_cache.append(func_cache)
        cache[func_name][context] = func_cache
        return func_cache
    else:
        return cache[func_name][context]


def cache_surface(func):
    func_cache = check_func_name(func, "surface")

    def t(surface, *args):
        if (raw := surface.get_buffer().raw) not in func_cache.keys():
            surface_cache = {}
            func_cache[raw] = surface_cache
        else:
            surface_cache = func_cache[raw]
        if (args := (round(args[0], 2), round(args[1], 2))) not in surface_cache:
            result = func(surface, *args)
            surface_cache[args] = default_zero_surface if 0 in result.get_size() else result
        return surface_cache[args]

    return t


def cache_color(func):
    func_cache = check_func_name(func, "color")

    def t(rgba, rmgmbmam, ragabaaa):
        if ((1, 1, 1, 1), (0, 0, 0, 0)) == (rmgmbmam, ragabaaa):
            return rgba
        elif (args := (rgba, rmgmbmam, ragabaaa)) not in func_cache.keys():
            func_cache[args] = func(*args)
        return func_cache[args]

    return t


def save():
    for func_cache in surfaces_cache:
        for _, surface_out in func_cache.items():
            for param, surface in surface_out.items():
                surface_out[param] = (pygame.image.tobytes(surface, "RGBA"), surface.get_size(), "RGBA")
    pickle.dump([cache, surfaces_cache], open(local_path, "wb"))


def load():
    global cache
    global surfaces_cache
    cache, surfaces_cache = pickle.load(open(local_path, "rb"))
    for func_cache in surfaces_cache:
        for _, surface_out in func_cache.items():
            for param, surface_data in surface_out.items():
                bytes_, size,format_ = surface_data
                if 0 in size:
                    surface_out[param] = default_zero_surface
                else:
                    surface_out[param] = pygame.image.frombytes(bytes_, size, format_)

if os.path.exists(local_path):
    load()
    
else:
    cache = {}
    surfaces_cache = []

