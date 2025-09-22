import os

#screen size
screen_width = 600
screen_height = 800
FPS = 144

#define colours
red = (255,0,0)
green = (0,255,0)

#paths
asset_dir =  "assets"
img_dir = os.path.join(asset_dir, "img")
sound_dir = os.path.join(asset_dir, "sound")
music_dir = os.path.join(asset_dir, "music")

#assets
spaceship_img = os.path.join(img_dir, "spaceship_no_bg.png")
bullet_img = os.path.join(img_dir, "bullet2.png")
enemy_bullet_img = os.path.join(img_dir, "bullet3.png")
booster_img = os.path.join(img_dir, "lightning.png")
background_img = os.path.join(img_dir, "navy cosmos.png")
boss_img = os.path.join(img_dir, "boss1.png")
laser_sound = os.path.join(sound_dir, "Laser_Sound.mp3")
music = os.path.join(music_dir, "Music_Space_Invaders.wav")


