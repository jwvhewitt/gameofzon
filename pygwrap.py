# Wrapper for pygame which should seamlessly handle the android stuff whether
# this program is run on a phone or not. Started as a wrap border routine,
# added a word wrapping function, then decided to merge in the android wrapper.
# Later on I may expand this unit to make burritos.

# Word wrapper taken from the PyGame wiki plus
# the list-printer from Anne Archibald's GearHead Prime demo.

import pygame
from itertools import chain
import image

# Import the android module. If we can't import it, set it to None - this
# lets us test it, and check to see if we want android-specific behavior.
try:
    import android

except ImportError:
    android = None


INPUT_CURSOR = None
SMALLFONT = None

INIT_DONE = False

# The FPS the game runs at.
FPS = 30

# Use a timer to control FPS.
TIMEREVENT = pygame.USEREVENT
pygame.time.set_timer(TIMEREVENT, 1000 / FPS)

# Remember whether or not this unit has been initialized, since we don't need
# to initialize it more than once.
INIT_DONE = False

# Store whether or not a quit signal has been received here.
GOT_QUIT = False


def wait_event():
    # Wait for input, then return it when it comes.
    ev = pygame.event.wait()

    # Android-specific:
    if android:
        if android.check_pause():
            android.wait_for_resume()

    # Record if a quit event took place
    if ev.type == pygame.QUIT:
        global GOT_QUIT
        GOT_QUIT = True

    return ev


class Border( object ):
    def __init__( self , border_width=16, tex_width=32, border_name="", tex_name="", tl=0, tr=0, bl=0, br=0, t=1, b=1, l=2, r=2 ):
        # tl,tr,bl,br are the top left, top right, bottom left, and bottom right frames
        # Bug: The border must be exactly half as wide as the texture.
        self.border_width = border_width
        self.tex_width = tex_width
        self.border_name = border_name
        self.tex_name = tex_name
        self.border = None
        self.tex = None
        self.tl = tl
        self.tr = tr
        self.bl = bl
        self.br = br
        self.t = t
        self.b = b
        self.l = l
        self.r = r

    def render( self, screen, dest ):
        """Draw this decorative border at dest on screen."""
        # We're gonna draw a decorative border to surround the provided area.
        # Step one: Determine the size of our box. Both dimensions should be 
        # a multiple of TEX_WIDTH. 

        if self.border == None:
            self.border = image.Image( self.border_name, self.border_width, self.border_width )
        if self.tex == None:
            self.tex = image.Image( self.tex_name, self.tex_width, self.tex_width )

        # W32 and H32 will store the number of columns/rows. 
        W32 = ( dest.width + self.border_width ) / self.tex_width + 1
        H32 = ( dest.height + self.border_width ) / self.tex_width + 1

        # X0 and Y0 will store the upper left corner of the box.
        X0 = dest.left - ( ( ( W32 * self.tex_width ) - dest.width ) / 2 )
        Y0 = dest.top - ( ( ( H32 * self.tex_width ) - dest.height ) / 2 )

        # Draw the backdrop.
        for X in range( W32 ):
            Dest_X = X0 + X * self.tex_width
            for Y in range( H32 ):
                Dest_Y = Y0 + Y * self.tex_width
                self.tex.render( screen , ( Dest_X , Dest_Y ) )

        self.border.render( screen , ( X0 - self.border_width / 2 , Y0 - self.border_width / 2 ) , self.tl )
        self.border.render( screen , ( X0 - self.border_width / 2 , Y0 - self.border_width / 2 + H32 * self.tex_width ) , self.bl )
        self.border.render( screen , ( X0 - self.border_width / 2 + W32 * self.tex_width , Y0 - self.border_width / 2 ) , self.tr )
        self.border.render( screen , ( X0 - self.border_width / 2 + W32 * self.tex_width , Y0 - self.border_width / 2 + H32 * self.tex_width ) , self.br )

        for X in range( 1 , W32 * 2 ):
            Dest_X = X0 + X * self.border_width - self.border_width / 2
            Dest_Y = Y0 - self.border_width / 2
            self.border.render( screen , ( Dest_X , Dest_Y ) , self.t )
            Dest_Y = Y0 + H32 * self.tex_width - self.border_width / 2
            self.border.render( screen , ( Dest_X , Dest_Y ) , self.b )
        for Y in range( 1 ,H32 * 2 ):
            Dest_Y = Y0 + Y * self.border_width - self.border_width / 2
            Dest_X = X0 - self.border_width / 2
            self.border.render( screen , ( Dest_X , Dest_Y ) , self.l )
            Dest_X = X0 + W32 * self.tex_width - self.border_width / 2
            self.border.render( screen , ( Dest_X , Dest_Y ) , self.r )

default_border = Border( border_name="sys_defborder.png", tex_name="sys_defbackground.png" )
map_border = Border( border_name="sys_mapborder.png", tex_name="sys_maptexture.png", tl=0, tr=1, bl=2, br=3, t=4, b=6, l=7, r=5 )
gold_border = Border( border_width=8, tex_width=16, border_name="sys_rixsborder.png", tex_name="sys_rixstexture.png", tl=0, tr=3, bl=4, br=5, t=1, b=1, l=2, r=2 )


def truncline(text, font, maxwidth):
        real=len(text)       
        stext=text           
        l=font.size(text)[0]
        cut=0
        a=0                  
        done=1
        old = None
        while l > maxwidth:
            a=a+1
            n=text.rsplit(None, a)[0]
            if stext == n: 
                cut += 1
                stext= n[:-cut]
            else:
                stext = n
            l=font.size(stext)[0]
            real=len(stext)               
            done=0                        
        return real, done, stext             
        
def wrapline(text, font, maxwidth): 
    done=0                      
    wrapped=[]                  
                               
    while not done:             
        nl, done, stext=truncline(text, font, maxwidth) 
        wrapped.append(stext.strip())                  
        text=text[nl:]                                 
    return wrapped
 
 
def wrap_multi_line(text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)


def render_text(font, text, width, color = (255,255,255), do_center= False ):
    # Return an image with prettyprinted text.
    lines = wrap_multi_line( text , font , width )

    imgs = [ font.render(l, True, color ) for l in lines]
    h = sum(i.get_height() for i in imgs)
    s = pygame.surface.Surface((width,h))
    s.fill((0,0,0))
    o = 0
    for i in imgs:
        if do_center:
            x = width/2 - i.get_width()/2
        else:
            x = 0
        s.blit(i,(x,o))
        o += i.get_height()
    s.set_colorkey((0,0,0),pygame.RLEACCEL)
    return s

def draw_text( screen , font , text , rect , color = (255,255,255), do_center= False ):
    # Draw some text to the screen with the provided options.
    myimage = render_text( font , text , rect.width , color , do_center )
    if do_center:
        myrect = myimage.get_rect( center = rect.center )
    else:
        myrect = rect
    screen.set_clip( rect )
    screen.blit( myimage , myrect )
    screen.set_clip( None )


ALLOWABLE_CHARACTERS = u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890()-=_+,.?"'

def input_string( screen , font , redrawer = None, prompt = "Enter text below", prompt_color = (255,255,255), input_color = (240,240,50), border=default_border ):
    # Input a string from the user.
    it = []
    keep_going = True
    cursor_frame = 1

    myrect = pygame.Rect( screen.get_width() / 2 - 200 , screen.get_height() / 2 - 32 , 400 , 64 )
    prompt_image = font.render( prompt, True, prompt_color )

    while keep_going:
        ev = wait_event()

        if ev.type == TIMEREVENT:
            if redrawer != None:
                redrawer( screen )
            border.render( screen , myrect )
            mystring = "".join( it )
            myimage = font.render( mystring, True, input_color )
            screen.blit( prompt_image , ( screen.get_width() / 2 - prompt_image.get_width() / 2 , screen.get_height() / 2 - prompt_image.get_height() - 2 ) )
            screen.set_clip( myrect )
            screen.blit( myimage , ( screen.get_width() / 2 - myimage.get_width() / 2 , screen.get_height() / 2 ) )
            INPUT_CURSOR.render( screen , ( screen.get_width() / 2 + myimage.get_width() / 2 + 2 , screen.get_height() / 2 ) , cursor_frame / 3 )
            screen.set_clip( None )
            cursor_frame = ( cursor_frame + 1 ) % ( INPUT_CURSOR.num_frames() * 3 )
            pygame.display.flip()


        elif ev.type == pygame.KEYDOWN:
            if ( ev.key == pygame.K_BACKSPACE ) and ( len( it ) > 0 ):
                del it[-1]
            elif ( ev.key == pygame.K_RETURN ) or ( ev.key == pygame.K_ESCAPE ):
                keep_going = False
            elif ( ev.unicode in ALLOWABLE_CHARACTERS ) and ( len( ev.unicode ) > 0 ):
                it.append( ev.unicode )
        elif ev.type == pygame.QUIT:
            keep_going = False
    return "".join( it )


def init():
    global INIT_DONE
    if not INIT_DONE:
        global INPUT_CURSOR
        INPUT_CURSOR = image.Image( "sys_textcursor.png" , 8 , 16 )

        global SMALLFONT
        SMALLFONT = pygame.font.Font( "image/VeraBd.ttf" , 16 )

        if android:
            android.init()
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

        # Set key repeat.
        pygame.key.set_repeat( 200 , 75 )

        INIT_DONE = True

if __name__ == "__main__":
    pygame.init()

    myfont = pygame.font.Font( "image/VeraBd.ttf" , 16 )

    # Set the screen size.
    screen = pygame.display.set_mode((640,640))
    text = render_text( myfont , "This is an example of an overly long line that will probably need to be split into multiple lines. I used to use song lyrics for this, but have decided against it as I didn't think of it at the time." , 300 , color = (125,250,180) )

    init()

    init()

    init()

    screen.fill((0,0,0))

    default_border.render(screen , pygame.rect.Rect(50,50,300,300))
    screen.blit( text , (50,50) )
    pygame.display.flip()

    while True:
        ev = pygame.event.wait()
        if ( ev.type == pygame.MOUSEBUTTONDOWN ) or ( ev.type == pygame.QUIT ) or (ev.type == pygame.KEYDOWN):
            break



