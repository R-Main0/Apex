import subprocess

projectIDs = {
    "Space" : 3041448036,
    "Fade" : 2784382079,
    "Party": 3628687733,
    "Fire" : 3138763620,
    "Interstellar": 2465407361,
    "Rise": 3350162681,
    "Deep": 1320654109,
    "real": 860024140
}

def setWallpaper(name):
    projectPath = fr"C:\Program Files (x86)\Steam\steamapps\workshop\content\431960\{projectIDs[name]}\project.json"
    subprocess.Popen([r"C:\Program Files (x86)\Steam\steamapps\common\wallpaper_engine\wallpaper32.exe", 
                      "-control", "openWallpaper", "-file",  projectPath])

def setPlaylist(name):
    subprocess.Popen([r"C:\Program Files (x86)\Steam\steamapps\common\wallpaper_engine\wallpaper32.exe", 
                      "-control", "openPlaylist", "-playlist",  name])

def play():
    subprocess.Popen([r"C:\Program Files (x86)\Steam\steamapps\common\wallpaper_engine\wallpaper32.exe", 
                      "-control", "play"])
    
def pause():
    subprocess.Popen([r"C:\Program Files (x86)\Steam\steamapps\common\wallpaper_engine\wallpaper32.exe", 
                      "-control", "pause"])
