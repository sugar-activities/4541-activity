#!/usr/bin/python
# StarCatcher.py
"""
    Copyright (C) 2011  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,pygame,utils,sys,load_save,buttons,slider
try:
    import gtk
except:
    pass
import st

class StarCatcher:

    def __init__(self):
        self.journal=True # set to False if we come in via main()
        self.canvas=None # set to the pygame canvas if we come in via activity.py

    def display(self):
        g.screen.fill((255,255,192))
        self.st.draw(self.demo)
        if self.demo:
            g.screen.blit(g.mouse_img,(g.sx(6),g.sy(4.5)))
        else:
            if g.best>1: self.slider.draw()
            if self.smiley:
                utils.centre_blit(g.screen,g.smiley,g.smiley_c)
            if self.sad:
                utils.centre_blit(g.screen,g.sad,g.smiley_c)
            if g.top>0 and g.level==8:
                g.screen.blit(g.top_img,g.top_xy1)
                g.screen.blit(g.top_img,g.top_xy2)
                utils.display_number3(\
                    g.screen,g.top,g.top_xy3,g.font2,utils.BLUE)
            if g.circle_c!=None:
                utils.centre_blit(g.screen,g.circle_img,g.circle_c)
        buttons.draw()

    def win_check(self):
        if self.st.finished: return
        if self.st.complete():
            if self.st.wrong==0:
                if g.level==8: g.top+=1
                if g.best<8:
                    if g.best==g.level:
                        g.best+=1; self.slider_setup()
                self.smiley=True
        if self.st.wrong>0: self.sad=True
        
    def left_click(self):
        if self.demo: self.round_setup(); return
        g.circle_c=None
        if not self.st.left_click(): return False
        self.win_check()
        return True
        
    def right_click(self):
        if self.demo: self.round_setup(); return
        g.circle_c=None
        self.st.right_click(); self.win_check()
        
    def do_button(self,bu):
        if bu=='new': self.round_setup(); return True

    def do_key(self,key):
        if key==pygame.K_v: g.version_display=not g.version_display; return
        if key in g.SQUARE: self.round_setup(); return
        if self.demo: self.round_setup(); return
        if key in g.TICK: self.change_level(); return
        if key in g.CROSS: self.left_click()
        if key in g.CIRCLE: self.right_click()
        if key in g.LEFT: self.st.dec_c()
        if key in g.UP: self.st.dec_r()
        if key in g.RIGHT: self.st.inc_c()
        if key in g.DOWN: self.st.inc_r()

    def change_level(self):
        g.level+=1
        if g.level>g.best: g.level=1
        self.round_setup()
        
    def round_setup(self):
        self.slider=None
        if g.best>1: self.slider_setup()
        self.st=st.St(g.level+2); self.st.setup()
        self.smiley=False; self.sad=False
        self.demo=False

    def demo_setup(self):
        self.slider=None
        self.st=st.St(3); self.st.demo()
        self.smiley=False; self.sad=False
        self.demo=True
        self.ms=pygame.time.get_ticks()
        g.redraw=True
        
    def update(self):
        if not self.demo: return
        ms=pygame.time.get_ticks()
        if ms>self.ms+2000: self.demo_setup()
        
    def slider_setup(self):
        self.slider=slider.Slider(g.sx(16),g.sy(20.5),g.best,utils.GREEN)

    def buttons_setup(self):
        buttons.Button('new',(g.sx(28.5),g.sy(20.5)))

    def flush_queue(self):
        flushing=True
        while flushing:
            flushing=False
            if self.journal:
                while gtk.events_pending(): gtk.main_iteration()
            for event in pygame.event.get(): flushing=True

    def run(self):
        g.init()
        if not self.journal: utils.load()
        load_save.retrieve()
        g.level=g.best; self.demo_setup()
        self.buttons_setup()
        if self.canvas<>None: self.canvas.grab_focus()
        ctrl=False
        pygame.key.set_repeat(600,120); key_ms=pygame.time.get_ticks()
        going=True
        while going:
            if self.journal:
                # Pump GTK messages.
                while gtk.events_pending(): gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    if not self.journal: utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.pos=event.pos
                    g.redraw=True
                    if self.canvas<>None: self.canvas.grab_focus()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    if event.button==1:
                        if self.left_click(): break
                        if g.best>1:
                            if self.slider!=None:
                                if self.slider.mouse():
                                    self.round_setup() # level changed
                                    break
                        bu=buttons.check()
                        if bu!='': self.do_button(bu); self.flush_queue()
                    if event.button==3:
                        self.right_click()
                elif event.type == pygame.KEYDOWN:
                    # throttle keyboard repeat
                    if pygame.time.get_ticks()-key_ms>110:
                        key_ms=pygame.time.get_ticks()
                        if ctrl:
                            if event.key==pygame.K_q:
                                if not self.journal: utils.save()
                                going=False; break
                            else:
                                ctrl=False
                        if event.key in (pygame.K_LCTRL,pygame.K_RCTRL):
                            ctrl=True; break
                        self.do_key(event.key); g.redraw=True
                        self.flush_queue()
                elif event.type == pygame.KEYUP:
                    ctrl=False
            if not going: break
            self.update()
            if g.redraw:
                self.display()
                if g.version_display: utils.version_display()
                g.screen.blit(g.pointer,g.pos)
                pygame.display.flip()
                g.redraw=False
            g.clock.tick(40)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode()
    game=StarCatcher()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
