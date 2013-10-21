import pygame
import rpgmenu
import pygwrap
import random
import image

class MenuRedrawer( object ):
    def __init__( self , caption = None , screen = None , backdrop = "bg_kde_thintentacles.jpg" ):
        self.caption = caption
        self.backdrop = image.Image( backdrop )
        self.counter = 0

        self.rect = pygame.Rect( screen.get_width()/2 - 200 , screen.get_height()/2 - 220, 400, 64 )

    def __call__( self , screen ):
        self.backdrop.tile( screen , ( self.counter * 5 , self.counter ) )
        if self.caption:
            pygwrap.default_border.render( screen , self.rect )
            pygwrap.draw_text( screen , pygwrap.SMALLFONT , self.caption , self.rect , do_center = True )
        self.counter += 5



def get_player_input( screen, caption, choices ):
    # Allow the player to select one choice from choices.
    menu = rpgmenu.Menu( screen , x=120, y=228, w=400, h=200, border = pygwrap.gold_border )
    menu.predraw = MenuRedrawer( caption , screen )
    for i in choices:
        menu.add_item( str( i ) , i )
    menu.add_alpha_keys()

    return menu.query()

if __name__ == "__main__":
    pygame.init()

    # Set the screen size.
    screen = pygame.display.set_mode((640,640))
    rpgmenu.init()

    # Set up the choices, enemy choices, and empty list for the player.
    choices = [ "Apple", "Banana", "Coconut", "Damson" ]
    enemy = [ random.choice( choices ) , random.choice( choices ) ]
    player = []

    # Round one. Fight!
    c1 = get_player_input( screen , "Welcome to Game of Zon! Make your first choice, mortal." , choices )
    player.append( c1 )

    # Round two. Fight!
    c2 = get_player_input( screen , "Very interesting. Make your second choice!" , choices )
    player.append( c2 )

    # Round three- decide on the winner.
    # Remove the player's choices from Enemy.
    for i in player:
        if i in enemy:
            enemy.remove( i )

    if len( enemy ) == 2:
        msg = "Congratulations! You have completely defeated your enemy!"
    elif enemy:
        msg = "The game ends in a draw..."
    else:
        msg = "You have chosen poorly. You die."

    rect = pygame.Rect( 64, 64, 512, 512 )
    pygwrap.default_border.render( screen , rect )
    pygwrap.draw_text( screen , pygwrap.SMALLFONT , msg , rect , do_center = True )
    pygame.display.flip()

    while True:
        ev = pygame.event.wait()
        if ( ev.type == pygame.MOUSEBUTTONDOWN ) or ( ev.type == pygame.QUIT ) or (ev.type == pygame.KEYDOWN):
            break


