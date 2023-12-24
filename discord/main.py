import time
import board
import neopixel
import discord
import random
import threading  # Import the threading module

rainbow_running = False
fire_running = False

from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix = "%", presences = True, members = True, guilds=True, intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name = "%help"))
    print("We have power")
    pixels.fill((0, 0, 0))
    pixels.show()


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 100

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB



pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)


#wheel for cycles 
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


# Define the function to run the rainbow cycle
def run_rainbow():
    global rainbow_running
    rainbow_running = True
    while rainbow_running:
        rainbow_cycle(0.001)
    rainbow_running = False

# Start the rainbow cycle in a separate thread
def start_rainbow_cycle():
    global rainbow_thread
    rainbow_thread = threading.Thread(target=run_rainbow)
    rainbow_thread.start()

# Stop the rainbow cycle
def stop_rainbow_cycle():
    global rainbow_running
    if rainbow_running:
        rainbow_running = False
        rainbow_thread.join()

# Define the function to run the fire effect
def run_fire():
    global fire_running
    fire_running = True
    while fire_running:
        fire_effect()
    fire_running = False

def start_fire_effect():
    global fire_thread
    fire_thread = threading.Thread(target=run_fire)
    fire_thread.start()

def stop_fire_effect():
    global fire_running
    if fire_running:
        fire_running = False
        fire_thread.join()

def fire_effect():
    bottem_sectoon = num_pixels // 3
    top_section = num_pixels - bottem_sectoon
    for i in range(bottem_sectoon):
        pixels[i] = (0, random.randint(200,255), 0)
    for i in range(bottem_sectoon, top_section):
        pixels[i] = (random.randint(50, 165), 255 , 0)
    for i in range(top_section, num_pixels):
        pixels[i] = (random.randint(190, 255), random.randint(190, 255), random.randint(0, 50))
    pixels.show()
    time.sleep(random.uniform(0.05, 0.2))


def set_light(r, g, b):
    stop_fire_effect()
    stop_rainbow_cycle()
    pixels.fill((0, 0, 0))
    pixels.show()
    pixels.fill((g, r, b))
    pixels.show()
    print("change")

@client.command()
async def red(ctx):
    await ctx.send("It is red")
    set_light(255, 0, 0)


@client.command()
async def blue(ctx):
    stop_rainbow_cycle()
    await ctx.send("It is blue")
    set_light(0, 0, 255)

@client.command()
async def green(ctx):
    stop_rainbow_cycle()
    await ctx.send("It is green")
    set_light(0, 255, 0)

@client.command()
async def white(ctx):
    stop_rainbow_cycle()
    await ctx.send("It is white")
    set_light(255, 255, 255)
    
@client.command()
async def pink(ctx):
    stop_rainbow_cycle()
    await ctx.send("It is Pink")
    set_light(255, 105, 180)
    
@client.command()
async def cyan(ctx):
    await ctx.send("It is cyan")
    set_light(0, 255, 255)

    
@client.command()
async def rainbow(ctx):
    stop_fire_effect()
    global rainbow_running
    if not rainbow_running:
        start_rainbow_cycle()
        await ctx.send("Rainbow effect started.")

@client.command(help= "lets use custom colors r = red g = green b = blue")
async def light(ctx,r: int,g: int,b: int):
    await ctx.send("It is light")
    set_light(r, g, b)
    
    
@client.command(help = "n = LED number then r = red g = green b = blue")
async def led(ctx,n: int,r: int,g: int,b: int):
    await ctx.send("It is light")
    pixels[n] = (g, r, b)
    pixels.show()

    
@client.command()
async def Alive(ctx):
    await ctx.send("Alive")
   
@client.command()
async def fire(ctx):
    stop_rainbow_cycle()
    global fire_running
    if not fire_running:
        start_fire_effect()
        await ctx.send("Fire effect started.")



client.run('TOKEN')
