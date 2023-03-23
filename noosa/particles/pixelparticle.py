from noosa.pseudopixel import PseudoPixel


class PixelParticle(PseudoPixel):
    size = None
    
    lifespan = None
    left = None
    
    def __init__(self,) -> None:
        super().__init__()
    
        self.origin.xy = 0.5
        
    def reset(self,x,y,color,size,lifespan):
        self.revive()
        
        self.x = x
        self.y = y
