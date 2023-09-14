import pygame
from gameengine import resources
from gameengine.nodes.graphicnode import GraphicNode


class PDImage(GraphicNode):
    def __init__(self, asset_or_src):
        super().__init__(resources.surface.get(asset_or_src))
