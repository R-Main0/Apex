import services.lighting.govee_local as govee_local
import services.xbox as xbox
import services.lighting.govee_api as govee_api
import variables.state as state
import services.controller as controller
import services.audio as audio
import services.wallpaper as wallpaper
import variables.config as config
import keyboard
import time
import random

#--- Device Variables ---
STRIP_IP = "192.168.1.97"
LAMP_IP = "192.168.1.174"
CLOSET_IP = "192.168.1.175"
BATHROOM_IP1 = "192.168.1.102"
BATHROOM_IP2 = "192.168.1.142"

def show_message():
    print("Hello from action system!")

def home():
    randint = random.randint(0, 2)
    r, g, b, playlist = config.RGBpresets[randint]
    wallpaper.setPlaylist(playlist)
    govee_local.switchAll(1)
    time.sleep(.2)
    govee_local.brightnessAll(100)
    time.sleep(.2)
    #if (playlist != "Fall"):
    #    govee_local.color(LAMP_IP, 220, 140, 50)
    #else:
    govee_local.color(LAMP_IP, r, g, b)
    govee_local.color(CLOSET_IP, 220, 140, 50)
    govee_local.color(BATHROOM_IP1, 220, 140, 50)
    govee_local.color(BATHROOM_IP2, 220, 140, 50)
    govee_local.color(STRIP_IP, r, g, b)
    govee_local.brightness(STRIP_IP, 50)
    
def wake():
    print("Waking up systems...")
    govee_local.switchAll(1)

def sleep():
    print("Sleeping...")
    audio.enqueue_sound("universfield-soft-cinematic-piano-outro-151764.wav")

    time.sleep(.5)
    govee_local.switch(LAMP_IP, 0)
    time.sleep(.5)
    govee_local.switch(BATHROOM_IP1, 0)
    govee_local.switch(BATHROOM_IP2, 0)
    time.sleep(.7)
    govee_local.switch(CLOSET_IP, 0)
    time.sleep(1)
    govee_local.switch(STRIP_IP, 0)
    time.sleep(1)
    
    state.night = True
    keyboard.press_and_release('windows+x')
    time.sleep(0.2)
    keyboard.press_and_release('u')
    time.sleep(0.2)
    keyboard.press_and_release('s')    

def night():
    print("Activating night mode...")
    govee_local.brightnessAll(10)
    govee_local.colorAll(220, 140, 50)
    state.night = True

def fade():
    print("Welcome Aubrey...")
    govee_local.colorAll(255, 158, 158)
    govee_local.color(LAMP_IP, 255, 50, 255)
    govee_local.color(STRIP_IP, 255, 100, 170)
    govee_local.brightnessAll(30)
    wallpaper.setWallpaper("Fade")

def clear():
    print("Clearing Screen...")
    keyboard.press_and_release('windows+d')
    wallpaper.play()
    
def deactivate():
    print("Shutting Down Systems...")
    govee_local.brightness(STRIP_IP, 50)
    controller.end()

def xbox_on():
    print("Activating xbox...")
    govee_local.brightness(CLOSET_IP, 1)
    govee_local.brightness(BATHROOM_IP1, 1)
    govee_local.brightness(BATHROOM_IP2, 1)
    govee_local.colorAll(0, 0, 255)
    govee_local.color(LAMP_IP, 50, 0, 255)
    govee_local.color(STRIP_IP, 50, 0, 255)
    xbox.power_on()

    
def party():
    print("Lets break it DOWN!")
    govee_api.sceneAll("party")
    wallpaper.setWallpaper("Party")

def real():
    govee_api.sceneAll("rainbow")
    wallpaper.setWallpaper("Real")

def interstellar():
    print("Its necessary.....")
    govee_local.brightnessAll(100)
    govee_local.colorAll(255, 255, 255)
    wallpaper.setWallpaper("Interstellar")

def boot():
    print("Initializing...")
    govee_local.switchAll(0)
    time.sleep(.8)
    govee_local.switch(LAMP_IP, 1)
    govee_local.brightness(LAMP_IP, 100)
    time.sleep(.7)
    govee_local.switch(BATHROOM_IP1, 1)
    govee_local.brightness(BATHROOM_IP1, 100)
    govee_local.switch(BATHROOM_IP2, 1)
    govee_local.brightness(BATHROOM_IP2, 100)
    time.sleep(.7)
    govee_local.switch(CLOSET_IP, 1)
    govee_local.brightness(CLOSET_IP, 100)
    time.sleep(.5)
    govee_local.switch(STRIP_IP, 1)
    govee_local.brightness(STRIP_IP, 100)
    time.sleep(1)
    govee_local.brightnessAll(1)
    time.sleep(.5)
    home()


def rise():
    govee_local.brightnessAll(100)
    govee_local.brightness(STRIP_IP, 1)
    govee_api.scene("sunrise", 0, "H6062")
    govee_local.color(LAMP_IP, 225, 75, 10)
    govee_local.color(CLOSET_IP, 10, 50, 200)
    govee_local.color(BATHROOM_IP1, 225, 75, 10)
    govee_local.color(BATHROOM_IP2, 10, 50, 200)
    wallpaper.setWallpaper("Rise")

def fire():
    govee_local.brightnessAll(100)
    govee_api.sceneAll("fire")
    wallpaper.setWallpaper("Fire")

def rotate():
    while True:
        home()
        time.sleep(10)
        rise()
        time.sleep(10)
        fade()
        time.sleep(10)
        interstellar()
        time.sleep(10)
        deep()
        time.sleep(10)

def deep():
    wallpaper.setWallpaper("Deep")
    govee_local.switch(CLOSET_IP, 0)
    govee_local.switch(BATHROOM_IP1, 0)
    govee_local.switch(BATHROOM_IP2, 0)
    govee_local.color(STRIP_IP, 255, 0, 0)
    govee_local.color(LAMP_IP, 0, 0, 255)

def explosion():
    print("Exploding...")
    audio.enqueue_sound("mixkit-explosive-impact-from-afar-2758.wav")