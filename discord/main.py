
# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import discord
import random


pixel_pin = board.D18


# The number of NeoPixels
num_pixels = 50


pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

from discord.ext import commands
        
client = commands.Bot(command_prefix = '.', intents=intents, presences = True, members = True, guilds=True)

@client.event
async def on_ready():
    # Setting `Playing ` status
    await client.change_presence(activity=discord.Game(name=".help is a thing")) # changed from bot - client
    print("we have powered on, I an alive.")



