import  pygame , random , math , time

pygame.init ( )
pygame.mixer.init ( )
pygame.mixer.music.load ("galau.mp3")

screen  =  pygame.display.set_mode ( ( 0 , 0 ) , pygame.FULLSCREEN )
W , H  =  screen.get_width ( ) , screen.get_height ( )
jam  =  pygame.time.Clock ( )

font_main  =  pygame.font.Font ( None , 75 )
font_sub  =  pygame.font.Font ( None , 52 )

CX , CY  =  W // 2  +  300 , H // 2  +  20

# KALO MASIH KECEPETAN, GANTI OFFSET JADI 0.5 ATAU 1.0
#KALO KELAMBATAN, GANTI JADI -0.5
OFFSET  =  0.0

LIRIK_DASAR  = [
    ( 2.5 , "Tapi kamu harus tahu itu" ),
    ( 4.7 , "Aku mati perlahan" ),
    ( 6.9 , "Berlari melalui lorong-lorong" ),
    ( 9.6 , "rumah berhantu Anda" ),
    ( 12.5 , "Dan bagian tersulitnya" ),
    ( 14.8 , "adalah bahwa kita berdua tahu" ),
    ( 17.2 , "Apa yang terjadi padamu" ),
    ( 19.8 , "Mengapa kamu sendirian" ),
    ( 22.0 , "Selamat Natal," ),    
    ( 23.5 , "jangan telepon" ),     
    ( 25.5 , "Selamat Natal," ),
    ( 27.0 , "Aku sama sekali bukan milikmu" ) ,
    ( 29.0 , "Selamat Natal," ),
    ( 30.8 , "tolong jangan hubungi saya" ),  
]

LIRIK  = [(item[0] + OFFSET, item[1]) for item in LIRIK_DASAR]

def  heart ( t , scale , cx , cy ):
    x  =  16  *  math . sin ( t ) ** 3
    y  =  13 * math.cos ( t ) - 5 * math.cos ( 2 * t ) - 2 * math.cos ( 3 * t ) - math.cos ( 4 * t )   
    return  cx  +  x * scale , cy  -  y * scale

class Thread :
    def  __init__ ( self , scale ):
        self.scale = scale
        self.ang  =  random.uniform ( 0 , 6.28 )
        r  =  random.uniform( 5 , 70 )
        self.x  =  CX  +  math.cos(self.ang) * r
        self.y  =  CY  +  math.sin( self.ang ) * r
        self.vx = random.uniform( -2 , 2 )  
        self.vy = random.uniform( -2 , 2 )  
        self.t = random.uniform( 0 , 6.28 )  
        self.speed = random.uniform( 0.025 , 0.045 )  
        self.off = random.uniform( 0 , 1000 )  
        self.trail = [ ( self.x , self.y ) ] 
        self.mati = 0
    def  update ( self ):
        self.mati  +=  0.05
        self.t +=  self.speed
        tx , ty  =  heart ( self.t , 22 * self.scale , CX , CY )
        tx  +=  math.sin ( self.off ) * 9
        ty  +=  math.cos ( self.off * 1.3 ) * 9
        dx  =  tx  -  self . x ; dy  =  ty  -  self . y
        self.vx += dx * 0.12 ; self.vy += dy * 0.12        
        self.vx  *= 0.80 ; self.vy *= 0.80    
        self.x +=  self.vx ; self.y += self.vy  
        self.trail.append ( ( self.x , self.y ) )
        if len( self.trail ) > 145 : self.trail.pop ( 0 ) 
    def  draw ( self , surf ):
        if len ( self.trail ) > 10 : 
            pygame.draw.aalines ( surf , ( 255 , 255 , 255 ) , False , self.trail )

bintang = [[ random . uniform ( 0 , W ), random . uniform ( 0 , H ), random . uniform ( 0.2 , 0.9 )] for  _  in range( 250 )]
firework = []; last_fw = 0
threads = []
for scale , count in[( 1.0 , 20 ), ( 0.74 , 16 ), ( 0.52 , 14 ), ( 0.34 , 10 ), ( 0.20 , 8 )]:
    for _  in range ( count ):threads.append(Thread(scale))

pygame.mixer.music.play ( )
mulai = time.time(); idx = 0 ; ditampilkan = [ ] ; berjalan = True
while berjalan:
    for e in  pygame.event.get ( ) :
        if  e.type == pygame.QUIT or( e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE ) :   
            berjalan = False
    time_passed = time.time()-mulai
    screen.fill( ( 0 , 0 , 0 ) )
    for s in bintang:
        pygame.draw.circle ( screen , ( 100 , 100 , 100 ), ( int ( s [ 0 ] ), int ( s [ 1 ] )) , 1 )
        s [ 1 ] += s [ 2 ]
        if s [ 1 ] > H : s [ 1 ] = -5 ; s [ 0 ] = random.uniform ( 0 , W )
    if time_passed- last_fw > 0.75 :
        fx  =  random.randint ( 100 , W - 100 )
        fy  =  random.randint ( 50 , 350 )
        col= random.choice([( 255 , 230 , 120 ),( 120 , 220 , 255 ) , ( 255 , 120 , 160 )])
        for _ in range ( 35 ):
            a = random.uniform ( 0 , 6.28 ) ; sp = random.uniform ( 1.8 , 5.0 )
            firework.append ( [ fx , fy , math.cos ( a ) * sp , math.sin ( a ) * sp , 0 , col , 4 ] )
        last_fw = time_passed
    for fw in firework [:]:
        fw [ 0 ] += fw [ 2 ]; fw [ 1 ] += fw [ 3 ]; fw [ 3 ] += 0.06 ; fw [ 4 ] += 1
        if fw [ 4 ] > 38 : firework.remove ( fw )
        else :
            pygame.draw.circle ( screen , fw [ 5 ], ( int ( fw [ 0 ] ), int ( fw [ 1 ] ) ) , fw [ 6 ] )
    for  th  in  threads : th . update (); th . draw ( screen )
    pygame.draw.circle ( screen , ( 180 , 230 , 255 ) , ( CX , CY - 5 ) , 5 )
    if  idx  <  len ( LIRIK) and time_passed  >=  LIRIK [ idx ][ 0 ]:
        ditampilkan.append ( LIRIK [ idx ] [ 1 ] )
        if len( ditampilkan ) > 2 : ditampilkan.pop ( 0 )
        idx += 1
    lx = 70
    ly_start  =  H // 2  -  120
    for i , txt  in enumerate (ditampilkan):
        f  =  font_main  if  i == len ( ditampilkan ) - 1  else  font_sub
        col = ( 255 , 255 , 255 ) if i == len( ditampilkan ) - 1  else ( 110 , 110 , 110 )
        y = int ( ly_start  +  i * 70 )
        surf = f.render ( txt , True , col )
        screen.blit ( surf , ( lx , y ) )
    pygame.display.flip ( )
    jam.tick( 90 )
    if time_passed >  42 : berjalan = False
pygame.quit()