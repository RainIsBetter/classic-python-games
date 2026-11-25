import pygame as p
p.init()
s=p.display.set_mode((800,500)); p.display.set_caption('Pong'); clock=p.time.Clock(); font=p.font.Font(None,48)
a=p.Rect(25,200,15,100); b=p.Rect(760,200,15,100); ball=p.Rect(390,240,20,20); vx,vy=5,4; score=[0,0]
while True:
    for e in p.event.get():
        if e.type==p.QUIT: p.quit(); raise SystemExit
    k=p.key.get_pressed()
    a.y+=6*(k[p.K_s]-k[p.K_w]); b.y+=6*(k[p.K_DOWN]-k[p.K_UP])
    for paddle in (a,b): paddle.clamp_ip(s.get_rect())
    ball.x+=vx; ball.y+=vy
    if ball.top<=0 or ball.bottom>=500: vy=-vy; ball.clamp_ip(s.get_rect())
    if ball.colliderect(a) and vx<0: ball.left=a.right; vx=-vx
    if ball.colliderect(b) and vx>0: ball.right=b.left; vx=-vx
    if ball.right<0 or ball.left>800:
        score[int(ball.right<0)]+=1; ball.center=(400,250); vx=-vx
    s.fill('black'); p.draw.line(s,'gray',(400,0),(400,500),2)
    for r in (a,b): p.draw.rect(s,'white',r)
    p.draw.ellipse(s,'white',ball); s.blit(font.render(f'{score[0]}   {score[1]}',True,'white'),(350,20)); p.display.flip(); clock.tick(60)
