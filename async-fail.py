# This is a testing enviornment, Nothing in this file is supposed to be incorporated into the final project
# Most of the content here is basically just me not knowing how things in the pygame framework function

# Defining some testing constants, these are simple settings which should be straight forward
FRAMES = 1

# Importing our framework
import pygame

# We're going to make an attempt at using asyncronous functions
# This will help run things at the same time, but this is not a substitute for multi-threading
import asyncio

# Some other modules which will help with misc. tasks
import time

def pygame_event_loop(loop, event_queue):
    while True:
        event = pygame.event.wait() # Fetches events from our framework
        asyncio.run_coroutine_threadsafe(
            # Adding our event to a asyncio.Queue object, to be handled asyncronously
            event_queue.put(
                event 
            ),
            loop = loop # References our event loop
        )

# Our asyncronous event handler
async def pygame_event_handler(event_queue):
    while True:
        event = await event_queue.get()
        if event.type == pygame.QUIT:
            break # This will break the event handler

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                print('fuck')

        if event.type == pygame.NOEVENT:
            return
        
        else: # Logging for now
            print("[PG-EVENT]", event, sep='\t')
    
    # Upon breaking the event handler, this will be called
    # Basically quits the loop somewhat gracefully I hope
    asyncio.get_event_loop().stop()

async def animation_handler(screen):
    # The "backmost" color, will be the initially drawn colour before all other 

    ct = 0 # Setting initial time
    while True:
        lt, ct = ct, 0 # Sets and overwrites my time variables
        await asyncio.sleep(
            1 / 60 # A tick
        )
        print('penis')

        sur = pygame.screen.get_surface()

        sur.fill(
            (0, 0, 50)
        )
        print('blue')

        
        pygame.draw.rect(
            (255, 0, 150),
            pygame.Rect(10, 10, 10, 10)
        )
        sur.blit()
        # Here is where I will handle animations

        pygame.display.flip()

if __name__ == "__main__":
    loop = asyncio.get_event_loop() # Fetching the event loop
    event_queue = asyncio.Queue()

    # Initializing our framework
    pygame.init()

    # Adding a nice window title
    pygame.display.set_caption("A test") 

    # Setting our mode, I want to make sure that this view works with tile width
    # Basically the formula would be: (tile_size * view) * size_mod
    # If TILE_SIZE is 16, and we wanna see 16 blocks, with a 2x size mod:
    # 16 * 16 = 256 * 2 = 512
    screen = pygame.display.set_mode(
        (
            512, # Width
            512 # Height
        )
    )

    # This handles all of the keystrokes and inputs that a user will send
    pygame_event_task = loop.run_in_executor(
        None, # I don't really know what this does
        pygame_event_loop, # Our event handler coroutine

        # Supplying the args
        loop,
        event_queue
    )

    # Telling our animation task to run
    animation_task = loop.create_task(
        animation_handler(screen)
    )

    # Telling our event redirector to run
    pygame_event_reditector_task = loop.create_task(
        pygame_event_handler(event_queue)
    )

    try:
        # Tell our async loop to run forever
        # By running this function it will basically "block" the rest of our code
        # So untill our loop stops, which happens with our event handler, it wont reach the next part of code
        # This allows my code to be clean af and removes extra stuff
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

    finally:
        # Stop all of our async tasks
        pygame_event_task.cancel()
        animation_task.cancel()
        pygame_event_reditector_task.cancel()

    # Tells the framework to bug off
    pygame.quit()


