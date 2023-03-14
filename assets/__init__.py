from io import BytesIO

from gameengine import Resources


class Assets:
    from .amulet import AMULET
    from .arcs1 import ARCS1
    from .arcs2 import ARCS2
    from .avatars import AVATARS
    from .badges import BADGES
    from .banners import BANNERS
    from .bat import BAT
    from .bee import BEE
    from .blacksmith import BLACKSMITH
    from .brute import BRUTE
    from .buffs import BUFFS
    from .burning_fist import BURNING_FIST
    from .chrome import CHROME
    from .crab import CRAB
    from .dashboard import DASHBOARD
    from .demon import DEMON
    from .dm300 import DM300
    from .effects import EFFECTS
    from .elemental import ELEMENTAL
    from .exp_bar import EXP_BAR
    from .eye import EYE
    from .fireball import FIREBALL
    from .font1x import FONT1X
    from .font2x import FONT2X
    from .font3x import FONT3X
    from .font15x import FONT15X
    from .font25x import FONT25X
    from .game import GAME
    from .ghost import GHOST
    from .gnoll import GNOLL
    from .golem import GOLEM
    from .goo import GOO
    from .hp_bar import HP_BAR
    from .icons import ICONS
    from .items import ITEMS
    from .king import KING
    from .large_buffs import LARGE_BUFFS
    from .larva import LARVA
    from .locked_badge import LOCKED_BADGE
    from .mage import MAGE
    from .mimic import MIMIC
    from .monk import MONK
    from .pet import PET
    from .piranha import PIRANHA
    from .plants import PLANTS
    from .ranger import RANGER
    from .rat import RAT
    from .ratking import RATKING
    from .rogue import ROGUE
    from .rotting_fist import ROTTING_FIST
    from .scorpio import SCORPIO
    from .shadow import SHADOW
    from .shaman import SHAMAN
    from .sheep import SHEEP
    from .shopkeeper import SHOPKEEPER
    from .skeleton import SKELETON
    from .snd_alert import SND_ALERT
    from .snd_badge import SND_BADGE
    from .snd_beacon import SND_BEACON
    from .snd_bee import SND_BEE
    from .snd_blast import SND_BLAST
    from .snd_bones import SND_BONES
    from .snd_boss import SND_BOSS
    from .snd_burning import SND_BURNING
    from .snd_challenge import SND_CHALLENGE
    from .snd_charms import SND_CHARMS
    from .snd_click import SND_CLICK
    from .snd_cursed import SND_CURSED
    from .snd_death import SND_DEATH
    from .snd_degrade import SND_DEGRADE
    from .snd_descend import SND_DESCEND
    from .snd_dewdrop import SND_DEWDROP
    from .snd_door_open import SND_DOOR_OPEN
    from .snd_drink import SND_DRINK
    from .snd_eat import SND_EAT
    from .snd_evoke import SND_EVOKE
    from .snd_falling import SND_FALLING
    from .snd_ghost import SND_GHOST
    from .snd_gold import SND_GOLD
    from .snd_hit import SND_HIT
    from .snd_item import SND_ITEM
    from .snd_levelup import SND_LEVELUP
    from .snd_lightning import SND_LIGHTNING
    from .snd_lullaby import SND_LULLABY
    from .snd_mastery import SND_MASTERY
    from .snd_meld import SND_MELD
    from .snd_mimic import SND_MIMIC
    from .snd_miss import SND_MISS
    from .snd_plant import SND_PLANT
    from .snd_puff import SND_PUFF
    from .snd_ray import SND_RAY
    from .snd_read import SND_READ
    from .snd_rocks import SND_ROCKS
    from .snd_secret import SND_SECRET
    from .snd_shatter import SND_SHATTER
    from .snd_step import SND_STEP
    from .snd_teleport import SND_TELEPORT
    from .snd_tomb import SND_TOMB
    from .snd_trap import SND_TRAP
    from .snd_unlock import SND_UNLOCK
    from .snd_water import SND_WATER
    from .snd_zap import SND_ZAP
    from .specks import SPECKS
    from .spell_icons import SPELL_ICONS
    from .spinner import SPINNER
    from .statue import STATUE
    from .status_pane import STATUS_PANE
    from .succubus import SUCCUBUS
    from .surface import SURFACE
    from .swarm import SWARM
    from .tengu import TENGU
    from .theme import THEME
    from .thief import THIEF
    from .tiles0 import TILES0
    from .tiles1 import TILES1
    from .tiles2 import TILES2
    from .tiles3 import TILES3
    from .tiles4 import TILES4
    from .toolbar import TOOLBAR
    from .undead import UNDEAD
    from .wandmaker import WANDMAKER
    from .warlock import WARLOCK
    from .warrior import WARRIOR
    from .water0 import WATER0
    from .water1 import WATER1
    from .water2 import WATER2
    from .water3 import WATER3
    from .water4 import WATER4
    from .wraith import WRAITH
    from .yog import YOG

    @classmethod
    def init(cls):
        print(cls.__dict__)
        for name, obj in cls.__dict__.items():
            if hasattr(obj, "ext"):
                is_built_in = name[0:2] != "__" and name[-2:] != "__"
                if is_built_in:
                    is_image = obj.ext == "png"
                    is_sound = obj.ext == "mp3"
                    if is_image:
                        Resources.Surface.add_from_file(
                            "IMAGE_" + name, BytesIO(obj.data)
                        )
