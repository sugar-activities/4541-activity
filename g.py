# g.py - globals
import pygame,utils,random

app='Star Catcher'; ver='1'
ver='21'
ver='22'
# added top
ver='23'
# tablet mode
# demo intro
# circle non guess area
ver='24'
# counts no of top level successes
ver='25'
# green set to (0,0)
ver='26'
# red circle cleared on setup
ver='27'
# new icon
# fixed png permissions
ver='28'
# widescreen
ver='29'
# only square key or V accpeted at demo screen
ver='30'
# name change from Stars
ver='31'
# only square key or V accpeted at demo screen
ver='32'
# any key or click starts

UP=(264,273,316)
DOWN=(258,274,312)
LEFT=(260,276,44)
RIGHT=(262,275,46)
CROSS=(259,120)
CIRCLE=(265,111)
SQUARE=(263,32)
TICK=(257,13)
NUMBERS={pygame.K_1:1,pygame.K_2:2,pygame.K_3:3,pygame.K_4:4,\
           pygame.K_5:5,pygame.K_6:6,pygame.K_7:7,pygame.K_8:8,\
           pygame.K_9:9,pygame.K_0:0}

def init(): # called by run()
    random.seed()
    global redraw
    global screen,w,h,font1,font2,clock
    global factor,offset,imgf,message,version_display
    global pos,pointer
    redraw=True
    version_display=False
    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill((70,0,70))
    pygame.display.flip()
    w,h=screen.get_size()
    if float(w)/float(h)>1.5: #widescreen
        offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    else:
        h=int(.75*w) # allow for toolbar - works to 4:3
        offset=0
    factor=float(h)/24 # measurement scaling factor (32x24 = design units)
    imgf=float(h)/900 # image scaling factor - all images built for 1200x900
    clock=pygame.time.Clock()
    if pygame.font:
        t=int(40*imgf); font1=pygame.font.Font(None,t)
        t=int(60*imgf); font2=pygame.font.Font(None,t)
    message=''
    pos=pygame.mouse.get_pos()
    pointer=utils.load_image('pointer.png',True)
    pygame.mouse.set_visible(False)
    
    # this activity only
    global best,gold,stars,level,smiley,smiley_c,sad,top_img,top_xy1,top_xy2
    global mouse_img,top,circle_img,circle_c,top_xy3
    level=1
    best=1
    gold=utils.load_image('gold.png',False)
    stars=[]
    for i in range(7):
        stars.append(utils.load_image(str(i)+'.png',True,'stars'))
    smiley=utils.load_image('smiley.png',True)
    sad=utils.load_image('sad.png',True)
    smiley_c=None # set in st.py when setting up stars
    top=0 # counts no. of successes at level 8
    top_img=utils.load_image('top.png',True)
    top_xy1=(sx(1.2),sy(.5)); top_xy2=(top_xy1[0],sy(16.2))
    top_xy3=(sx(1),sy(20.2))
    mouse_img=utils.load_image('mouse.png',True)
    circle_img=utils.load_image('circle.png',True); circle_c=None
    
def sx(f): # scale x function
    return int(f*factor+offset+.5)

def sy(f): # scale y function
    return int(f*factor+.5)
