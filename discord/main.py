

import time
import board
import neopixel
import discord
import random

from discord.ext import commands

client = commands.Bot(command_prefix = "#", presences = True, members = True, guilds=True)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name = "#help"))
    print("We have power")


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 50

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




@client.command()
async def red(ctx):
    await ctx.send("It is red")
    pixels.fill((0, 0, 0))
    pixels.show()
    pixels.fill((0, 255, 0))
    pixels.show()
    print("change") 


@client.command()
async def blue(ctx):
    await ctx.send("It is blue")
    pixels.fill((0, 0, 0))
    pixels.show()
    pixels.fill((0, 0, 255))
    pixels.show()
    print("change") 

@client.command()
async def green(ctx):
    await ctx.send("It is green")
    pixels.fill((0, 0, 0))
    pixels.show()
    pixels.fill((255, 0, 0))
    pixels.show()
    print("change") 

@client.command()
async def white(ctx):
    await ctx.send("It is white")
    pixels.fill((0, 0, 0))
    pixels.show()
    pixels.fill((255, 250, 250))
    pixels.show()
    print("change")     

@client.command()
async def rainbow(ctx):
    await ctx.send("It is a rainbow_cycle")
    rainbow_cycle(0.001)
    print("change") 
    
@client.command()
async def light(ctx,x: int,y: int,z: int):
    await ctx.send("It is light")
    pixels.fill((0, 0, 0))
    pixels.show()
    pixels.fill((x, y, z))
    pixels.show()
    print("change")
    print(x,y,z) 
    
@client.command()
async def Alive(ctx):
    await ctx.send("Alive")
   




client.run('TOKEN')
