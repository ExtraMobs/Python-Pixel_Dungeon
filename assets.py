import enum
import os

import pygame

from gameengine import resources


class Assets(enum.Enum):
    ARCS_BG = "arcs1.png"
    ARCS_FG = "arcs2.png"
    DASHBOARD = "dashboard.png"
    BANNERS = "banners.png"
    BADGES = "badges.png"
    LOCKED = "locked_badge.png"
    AMULET = "amulet.png"
    CHROME = "chrome.png"
    ICONS = "icons.png"
    STATUS = "status_pane.png"
    HP_BAR = "hp_bar.png"
    XP_BAR = "exp_bar.png"
    TOOLBAR = "toolbar.png"
    SHADOW = "shadow.png"
    WARRIOR = "warrior.png"
    MAGE = "mage.png"
    ROGUE = "rogue.png"
    HUNTRESS = "ranger.png"
    AVATARS = "avatars.png"
    PET = "pet.png"
    SURFACE = "surface.png"
    FIREBALL = "fireball.png"
    SPECKS = "specks.png"
    EFFECTS = "effects.png"
    RAT = "rat.png"
    GNOLL = "gnoll.png"
    CRAB = "crab.png"
    GOO = "goo.png"
    SWARM = "swarm.png"
    SKELETON = "skeleton.png"
    SHAMAN = "shaman.png"
    THIEF = "thief.png"
    TENGU = "tengu.png"
    SHEEP = "sheep.png"
    KEEPER = "shopkeeper.png"
    BAT = "bat.png"
    BRUTE = "brute.png"
    SPINNER = "spinner.png"
    DM300 = "dm300.png"
    WRAITH = "wraith.png"
    ELEMENTAL = "elemental.png"
    MONK = "monk.png"
    WARLOCK = "warlock.png"
    GOLEM = "golem.png"
    UNDEAD = "undead.png"
    KING = "king.png"
    STATUE = "statue.png"
    PIRANHA = "piranha.png"
    EYE = "eye.png"
    SUCCUBUS = "succubus.png"
    SCORPIO = "scorpio.png"
    ROTTING = "rotting_fist.png"
    BURNING = "burning_fist.png"
    YOG = "yog.png"
    LARVA = "larva.png"
    GHOST = "ghost.png"
    MAKER = "wandmaker.png"
    TROLL = "blacksmith.png"
    IMP = "demon.png"
    RATKING = "ratking.png"
    BEE = "bee.png"
    MIMIC = "mimic.png"
    ITEMS = "items.png"
    PLANTS = "plants.png"
    TILES_SEWERS = "tiles0.png"
    TILES_PRISON = "tiles1.png"
    TILES_CAVES = "tiles2.png"
    TILES_CITY = "tiles3.png"
    TILES_HALLS = "tiles4.png"
    WATER_SEWERS = "water0.png"
    WATER_PRISON = "water1.png"
    WATER_CAVES = "water2.png"
    WATER_CITY = "water3.png"
    WATER_HALLS = "water4.png"
    BUFFS_SMALL = "buffs.png"
    BUFFS_LARGE = "large_buffs.png"
    SPELL_ICONS = "spell_icons.png"
    FONTS1X = "font1x.png"
    FONTS15X = "font15x.png"
    FONTS2X = "font2x.png"
    FONTS25X = "font25x.png"
    FONTS3X = "font3x.png"
    THEME = "theme.mp3"
    TUNE = "game.mp3"
    HAPPY = "surface.mp3"
    SND_CLICK = "snd_click.mp3"
    SND_BADGE = "snd_badge.mp3"
    SND_GOLD = "snd_gold.mp3"
    SND_OPEN = "snd_door_open.mp3"
    SND_UNLOCK = "snd_unlock.mp3"
    SND_ITEM = "snd_item.mp3"
    SND_DEWDROP = "snd_dewdrop.mp3"
    SND_HIT = "snd_hit.mp3"
    SND_MISS = "snd_miss.mp3"
    SND_STEP = "snd_step.mp3"
    SND_WATER = "snd_water.mp3"
    SND_DESCEND = "snd_descend.mp3"
    SND_EAT = "snd_eat.mp3"
    SND_READ = "snd_read.mp3"
    SND_LULLABY = "snd_lullaby.mp3"
    SND_DRINK = "snd_drink.mp3"
    SND_SHATTER = "snd_shatter.mp3"
    SND_ZAP = "snd_zap.mp3"
    SND_LIGHTNING = "snd_lightning.mp3"
    SND_LEVELUP = "snd_levelup.mp3"
    SND_DEATH = "snd_death.mp3"
    SND_CHALLENGE = "snd_challenge.mp3"
    SND_CURSED = "snd_cursed.mp3"
    SND_TRAP = "snd_trap.mp3"
    SND_EVOKE = "snd_evoke.mp3"
    SND_TOMB = "snd_tomb.mp3"
    SND_ALERT = "snd_alert.mp3"
    SND_MELD = "snd_meld.mp3"
    SND_BOSS = "snd_boss.mp3"
    SND_BLAST = "snd_blast.mp3"
    SND_PLANT = "snd_plant.mp3"
    SND_RAY = "snd_ray.mp3"
    SND_BEACON = "snd_beacon.mp3"
    SND_TELEPORT = "snd_teleport.mp3"
    SND_CHARMS = "snd_charms.mp3"
    SND_MASTERY = "snd_mastery.mp3"
    SND_PUFF = "snd_puff.mp3"
    SND_ROCKS = "snd_rocks.mp3"
    SND_BURNING = "snd_burning.mp3"
    SND_FALLING = "snd_falling.mp3"
    SND_GHOST = "snd_ghost.mp3"
    SND_SECRET = "snd_secret.mp3"
    SND_BONES = "snd_bones.mp3"
    SND_BEE = "snd_bee.mp3"
    SND_DEGRADE = "snd_degrade.mp3"
    SND_MIMIC = "snd_mimic.mp3"


class BannerSprites(enum.Enum):
    PIXEL_DUNGEON = enum.auto()
    BOSS_SLAIN = enum.auto()
    GAME_OVER = enum.auto()
    SELECT_YOUR_HERO = enum.auto()
    PIXEL_DUNGEON_SIGNS = enum.auto()


class Flames(enum.Enum):
    BLIGHT = enum.auto()
    FLIGHT = enum.auto()
    FLAME1 = enum.auto()
    FLAME2 = enum.auto()


def load_files():
    for asset_var in Assets.__members__.values():
        ext = os.path.splitext(asset_var.value)[-1]
        path = os.path.join("assets\\", asset_var.value)
        if ext == ".png":
            resources.surface.add_from_file(asset_var, path)
        elif ext == ".mp3":
            resources.sound.add_from_file(asset_var, path)

    # BannerSprites
    resources.surface.set(
        BannerSprites.PIXEL_DUNGEON,
        resources.surface.slice(Assets.BANNERS, pygame.Rect(0, 0, 128, 70))[0],
    )
    resources.surface.set(
        BannerSprites.BOSS_SLAIN,
        resources.surface.slice(Assets.BANNERS, pygame.Rect(0, 70, 128, 35))[0],
    )
    resources.surface.set(
        BannerSprites.GAME_OVER,
        resources.surface.slice(Assets.BANNERS, pygame.Rect(0, 105, 128, 35))[0],
    )
    resources.surface.set(
        BannerSprites.SELECT_YOUR_HERO,
        resources.surface.slice(Assets.BANNERS, pygame.Rect(0, 140, 128, 21))[0],
    )
    resources.surface.set(
        BannerSprites.PIXEL_DUNGEON_SIGNS,
        resources.surface.slice(Assets.BANNERS, pygame.Rect(0, 161, 128, 57))[0],
    )

    # Flames
    resources.surface.set(
        Flames.BLIGHT,
        resources.surface.slice(Assets.FIREBALL, pygame.Rect(0, 0, 32, 32))[0],
    )
    resources.surface.set(
        Flames.FLIGHT,
        resources.surface.slice(Assets.FIREBALL, pygame.Rect(32, 0, 32, 32))[0],
    )
    resources.surface.set(
        Flames.FLAME1,
        resources.surface.slice(Assets.FIREBALL, pygame.Rect(64, 0, 32, 32))[0],
    )
    resources.surface.set(
        Flames.FLAME2,
        resources.surface.slice(Assets.FIREBALL, pygame.Rect(96, 0, 32, 32))[0],
    )
