# Testing out multi-threading and seeing if it goes better than async build
# FYI: Async build failed

import pygame
import threading
import queue

FRAMES_SETTING = 100
SET_IS_END = False # Setting this to true wont let the program run...

def event_hook(queue):
    global SET_IS_END
    while not SET_IS_END:
        item = pygame.fastevent.wait()
        if item.type != pygame.NOEVENT:
            queue.put(item)
        #print("Got event: %s" % item)
        #print("Appended event!")

def event_handler(queue):
    global SET_IS_END
    while not SET_IS_END:
        x = queue.get()
        if x.type == pygame.NOEVENT:
            return
        
        elif x.type == pygame.QUIT:
            SET_IS_END = True

        elif x.type == pygame.KEYDOWN:
            if x.key == pygame.K_q:
                print("sex")

            else:
                print(x.key)
        return

def animation_handler(screen):
    screen.fill(
        (0, 0, 255) # Random color
    )
    pygame.display.flip()

if __name__ == "__main__":
    SET_IS_END = False
    event_queue = queue.Queue() 
    screen = pygame.display.set_mode(
        (
            512, 512
        )
    )
    pygame.init()
    pygame.fastevent.init()
    
    # We're going to use a seperate thread for event handling
    # This may make a difference in performance
    event_thread = threading.Thread(target=event_hook, args = (event_queue,)).start()
    event_task_thread = threading.Thread(target=event_handler, args=(event_queue,)).start()
    animation_thread = threading.Thread(target=animation_handler, args=(screen,)).start()
    