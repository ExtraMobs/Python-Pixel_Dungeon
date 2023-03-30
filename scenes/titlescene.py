from gameengine.engine import Engine
from noosa.camera import Camera
from scenes.pixelscene import PixelScene


class TitleScene(PixelScene):
    TXT_PLAY		= "Play"
    TXT_HIGHSCORES	= "Rankings"
    TXT_BADGES		= "Badges"
    TXT_ABOUT		= "About"

    def create(self):
        super().create()
        
        # TODO
        # Music.INSTANCE.play( Assets.THEME, true );
		# Music.INSTANCE.volume( 1f );
  
        self.ui_camera.visible = False
        
        w = Camera.main.width
        h = Camera.main.height
        
        # archs = Archs()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        if Engine.request_quit:
            Engine.system_exit()
