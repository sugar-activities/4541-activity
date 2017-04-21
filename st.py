# st.py
import g,random,utils,pygame,math

class Star:
    def __init__(self,cx,cy):
        self.cxy=(cx,cy); self.colour=0 # image # 0..6

class Cell:
    def __init__(self,r,c,x,y):
        self.r=r; self.c=c; self.x=x; self.y=y
        self.val=0 # 0-8 neighbour count
        self.show=False
        self.star=False
        self.colour=None

class St:
    def __init__(self,n): # eg n=5->5x5
        self.n=n
        self.cells=[]
        self.d=g.gold.get_width(); s=self.d*n; margin=g.sy(9.6)-s/2
        x0=g.sx(32)-margin-s; y0=margin
        y=y0
        for r in range(n):
            x=x0
            for c in range(n):
                cell=Cell(r,c,x,y); self.cells.append(cell)
                x+=self.d
            y+=self.d
        self.x0=x0
        self.green_w=g.sy(.1)
        self.d2=self.d/2

    def setup(self):
        for cell in self.cells: cell.show=False; cell.star=False
        n=0; colr=1; self.target=int(self.n*1.5)
        for t in range(1000): # avoid loop
            r=random.randint(0,self.n-1); c=random.randint(0,self.n-1)
            cell=self.cellrc(r,c)
            if not cell.star:
                cell.star=True; n+=1; cell.colour=colr; colr+=1
                if colr==len(g.stars): colr=1
                if n>=self.target: break
        for cell in self.cells: cell.val=self.neighbour_k(cell.r,cell.c)
        self.found=0; self.wrong=0; self.finished=False
        self.setup_stars()
        self.set_green(0,0); g.circle_c=None

    def setup_stars(self):
        self.stars=[]
        a=-math.pi/2; da=math.pi*2/self.target
        x0=self.x0/2; y0=g.sy(9.5); r=g.sy(5.5)
        for i in range(self.target):
            cx=x0+r*math.cos(a); cy=y0+r*math.sin(a); a+=da
            self.stars.append(Star(cx,cy))
        g.smiley_c=(x0,y0)
        
    def draw(self,demo=False):
        w=g.sy(.02)
        for cell in self.cells:
            if cell.show:
                rect=(cell.x,cell.y,self.d+1,self.d+1)
                pygame.draw.rect(g.screen,utils.BLUE,rect,w)
                cxy=(cell.x+self.d2,cell.y+self.d2)
                if cell.star:
                    utils.centre_blit(g.screen,g.stars[cell.colour],cxy)
                else:
                    if cell.val!=None:
                        utils.display_number(str(cell.val),cxy,g.font2)
            else:
                g.screen.blit(g.gold,(cell.x,cell.y))
        if not demo:
            for star in self.stars:
                utils.centre_blit(g.screen,g.stars[star.colour],star.cxy)
            rect=pygame.Rect(self.green.x,self.green.y,self.d,self.d)
            pygame.draw.rect(g.screen,utils.GREEN,rect,self.green_w)

    def left_click(self):
        cell=self.which()
        if cell==None: return False
        if cell.show: return True
        if cell.star:
            self.found+=1
            self.stars[self.found-1].colour=cell.colour
            if not self.need_to_guess(): self.wrong+=1
        cell.show=True
        return True

    def right_click(self):
        cell=self.which()
        if cell==None: return False
        if cell.show: return True
        if cell.star:
            self.found+=1
            self.stars[self.found-1].colour=cell.colour
        else:
            if not self.need_to_guess(): self.wrong+=1
        cell.show=True
        return True

    def which(self):
        for cell in self.cells:
            if utils.mouse_in(cell.x,cell.y,cell.x+self.d,cell.y+self.d):
                return cell
        return None
        
    def cellrc(self,r,c):
        if r<0 or c<0: return None
        if r>=self.n or c>=self.n: return None
        ind=r*self.n+c
        return self.cells[ind]

    def neighbours(self,r,c):
        drc=((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        ns=[]
        for dr,dc in drc:
            cell=self.cellrc(r+dr,c+dc)
            if cell!=None: ns.append(cell)
        return ns
            
    def neighbour_k(self,r,c):
        k=0; ns=self.neighbours(r,c)
        for cell in ns:
            if cell.star: k+=1
        return k

    def need_to_guess(self):
        for cell in self.cells:
            if cell.show:
                if not cell.star:
                    ns=self.neighbours(cell.r,cell.c)
                    k1=0 # star neighbours showing
                    k2=0 # hidden neighbours
                    for cell1 in ns:
                        if cell1.show:
                            if cell1.star: k1+=1
                        else:
                            k2+=1
                    if k2>0:
                        if cell.val==k1:
                            g.circle_c=(cell.x+self.d2,cell.y+self.d2)
                            #print 1,cell.r,cell.c,cell.val,k1,k2###
                            return False # no need to guess
                        if cell.val==(k1+k2):
                            g.circle_c=(cell.x+self.d2,cell.y+self.d2)
                            #print 2,cell.r,cell.c,cell.val,k1,k2###
                            return False # no need to guess
        return True

    def inc_r(self):
        r,c=self.green.r,self.green.c
        r+=1
        if r==self.n: r=0
        self.set_green(r,c)

    def inc_c(self):
        r,c=self.green.r,self.green.c
        c+=1
        if c==self.n: c=0
        self.set_green(r,c)

    def dec_r(self):
        r,c=self.green.r,self.green.c
        r-=1
        if r<0: r=self.n-1
        self.set_green(r,c)

    def dec_c(self):
        r,c=self.green.r,self.green.c
        c-=1
        if c<0: c=self.n-1
        self.set_green(r,c)

    def set_green(self,r,c):
        self.green=self.cellrc(r,c)
        x,y=self.green.x,self.green.y
        x+=self.d*.8; y+=self.d*.8
        g.pos=x,y; pygame.mouse.set_pos(g.pos)

    def complete(self):
        if self.finished: return True
        if self.found<self.target: return False
        self.finished=True
        return True

    def demo(self):
        total=random.randint(0,8)
        if total>0:
            n=0; colr=1
            for t in range(1000): # avoid loop
                r=random.randint(0,2); c=random.randint(0,2)
                if r==1 and c==1:
                    pass
                else:
                    cell=self.cellrc(r,c)
                    if not cell.star:
                        cell.star=True; n+=1; cell.colour=colr; colr+=1
                        if colr==len(g.stars): colr=1
                        if n>=total: break
        for cell in self.cells: cell.val=None; cell.show=True
        self.cellrc(1,1).val=total

                
                
                
        
        
            
            
