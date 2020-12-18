# An attempt at learning how gradients work, this program creates a flashing window.
# That's literally it, it make window flash...

import pygame, random, time, math

pygame.init()
screen = pygame.display.set_mode(
    (512, 512)
)

def mathshit(c1, c2, percent):
    r = c1[0] + (math.sqrt(percent ** 2) / 100) * (c2[0] - c1[0])
    g = c1[1] + (math.sqrt(percent ** 2) / 100) * (c2[1] - c1[1])
    b = c1[2] + (math.sqrt(percent ** 2) / 100) * (c2[2] - c1[2])
    return (r, g, b)

while True:
    screen.fill(
        (50, 200, 40)
    )

    start = 255, 255, 0
    end = 0, 0, 0

    #for offset in range(16):
    for p in range(100):
        
        p -= 50
        c = mathshit(start, end, p * 2)
        screen.fill(c)
                #pygame.draw.rect(
                #    screen,
                #    c,
                #    (row * 32, column * 32, 32, 32)
                #)
        pygame.display.flip()
        time.sleep(1 / 60)

    
    

    
