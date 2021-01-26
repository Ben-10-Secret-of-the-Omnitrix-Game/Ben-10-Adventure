import pygame_gui
import pygame

from pygame.transform import scale

from .game_engine import RESOLUTION, ga, manager



HD = (1280, 720)
FULL_HD = (1920, 1080)

def vertical(size, startcolor, endcolor):
    """
    Draws a vertical linear gradient filling the entire surface. Returns a
    surface filled with the gradient (numeric is only 2-3 times faster).
    """
    height = size[1]
    bigSurf = pygame.Surface((1, height)).convert_alpha()
    dd = 1.0/height
    sr, sg, sb, sa = startcolor
    er, eg, eb, ea = endcolor
    rm = (er-sr)*dd
    gm = (eg-sg)*dd
    bm = (eb-sb)*dd
    am = (ea-sa)*dd
    for y in range(height):
        bigSurf.set_at((0, y),
                       (int(sr + rm*y),
                        int(sg + gm*y),
                        int(sb + bm*y),
                        int(sa + am*y))
                       )
    return scale(bigSurf, size)

def draw_main_screen():
    # background_gradient = vertical(win_size, (118, 174, 62, 255), (9, 48, 21, 255))

    if RESOLUTION <= HD:
        sab = pygame_gui.elements.UIButton(pygame.Rect(500, 360, 272, 50), '', manager=manager)
        sab.drawable_shape.states['normal'].surface.blit(ga.start_adventure_button_x2, (0, 0))
        sab.drawable_shape.active_state.has_fresh_surface = True
        
        ob = pygame_gui.elements.UIButton(pygame.Rect(540, 410, *ga.options_button_x2.get_rect()[2:]), '', manager=manager)
        ob.drawable_shape.states['normal'].surface.blit(ga.options_button_x2, (0, 0))
        ob.drawable_shape.active_state.has_fresh_surface = True
    elif RESOLUTION >= FULL_HD:
        sab_size = ga.start_adventure_button_x2.get_rect()[2:]
        sab_new = scale(ga.start_adventure_button_x2, (sab_size[0] * 2, sab_size[1] * 2))
        sab = pygame_gui.elements.UIButton(pygame.Rect(350, 300, *sab_new.get_rect()[2:]), '', manager=manager)
        sab.drawable_shape.states['normal'].surface.blit(sab_new, (0, 0))
        sab.drawable_shape.active_state.has_fresh_surface = True
        
        ob_size = ga.options_button_x2.get_rect()[2:]
        ob_new = scale(ga.options_button_x2, (ob_size[0] * 2, ob_size[1] * 2))
        ob = pygame_gui.elements.UIButton(pygame.Rect(450, 400, *ob_new.get_rect()[2:]), '', manager=manager)
        ob.drawable_shape.states['normal'].surface.blit(ob_new, (0, 0))
        ob.drawable_shape.active_state.has_fresh_surface = True