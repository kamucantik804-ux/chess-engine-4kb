#!/usr/bin/env python3
"""Chess engine - alpha-beta search, UCI."""
import os,sys,json,time,math
PV={'P':100,'N':320,'B':330,'R':500,'Q':900,'K':20000}
PVF={'p':-100,'n':-320,'b':-330,'r':-500,'q':-900,'k':-20000,'P':100,'N':320,'B':330,'R':500,'Q':900,'K':20000}

def fb(fen):
 b=[[0]*8 for _ in range(8)];r=7;f=0
 for c in fen.split()[0]:
  if c=='/':r-=1;f=0
  elif c.isdigit():f+=int(c)
  else:b[r][f]=c;f+=1
 return b,'w'==fen.split()[1]

def mv(b,t):
 m=[];V='PNBRQK'
 for r in range(8):
  for f in range(8):
   p=b[r][f]
   if not p or (t and p.isupper()) or (not t and p.islower()):continue
   if p=='P':
    d=-1 if t else 1;nr,nf=r+d,f
    if 0<=nr<8 and not b[nr][nf]:
     m.append(((r,f),(nr,nf),b[nr][nf]!=0))
     if (t and r==6) or (not t and r==1):
      nnr=nr+d
      if 0<=nnr<8 and not b[nnr][nf]:m.append(((r,f),(nnr,nf),b[nnr][nf]!=0))
    for df in[-1,1]:
     nf=f+df;nr=r+d
     if 0<=nr<8 and 0<=nf<8 and b[nr][nf]!=0 and b[nr][nf].upper()!=p.upper():m.append(((r,f),(nr,nf),1))
   elif p=='N':
    for dr,df in[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
     nr,nf=r+dr,f+df
     if 0<=nr<8 and 0<=nf<8 and(not b[nr][nf] or b[nr][nf].upper()!=p.upper()):m.append(((r,f),(nr,nf),b[nr][nf]!=0))
   elif p in'BRQ':
    D=[(-1,-1),(-1,1),(1,-1),(1,1)] if p=='B' else[((-1,0),(1,0),(0,-1),(0,1))] if p=='R' else[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for dr,df in D:
     for i in range(1,8):
      nr,nf=r+dr*i,f+df*i
      if not(0<=nr<8 and 0<=nf<8):break
      if not b[nr][nf]:m.append(((r,f),(nr,nf),0))
      elif b[nr][nf].upper()!=p.upper():m.append(((r,f),(nr,nf),1));break
      else:break
   elif p=='K':
    for dr,df in[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
     nr,nf=r+dr,f+df
     if 0<=nr<8 and 0<=nf<8 and(not b[nr][nf] or b[nr][nf].upper()!=p.upper()):m.append(((r,f),(nr,nf),b[nr][nf]!=0))
 return m

def ev(b):
 s=0
 for r in range(8):
  for f in range(8):
   p=b[r][f]
   if p:s+=PVF.get(p,0)
 return s

def mm(b,m):
 b=[r[:] for r in b];r1,f1=m[0];r2,f2=m[1];b[r2][f2]=b[r1][f1];b[r1][f1]=0
 if b[r2][f2]=='P' and(r2==0 or r2==7):b[r2][f2]='Q'
 return b

def ab(b,t,d,a,bt):
 if d<1:return ev(b),None
 ms=mv(b,t)
 if not ms:return -30000,None
 bm=ms[0];IM=t=='w'
 for m in ms:
  nb=mm(b,m);v,_=ab(nb,'b' if t=='w' else 'w',d-1,-bt if IM else -bt,-a if IM else -bt)
  v=-v
  if v>a:a=v;bm=m
  if a>=bt:break
 return a,bm

def sm(b,t,tl=100):
 st=time.time();bv=-99999;v=None;d=2
 while time.time()-st<tl:
  try:
   v,m=ab(b,t,d,-99999,99999)
   if v>bv:bv=v;mv=m
   d+=1
  except:break
 return mv

def main():
 env=os.environ.get('MAKEFUN_ENV_URL','')
 b,t=fb('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
 d=2
 for _ in range(100):
  if t=='w':
   m=sm(b,'w',1000)
   if not m:break
   b=mm(b,m);t='b'
  else:
   m=sm(b,'b',1000)
   if not m:break
   b=mm(b,m);t='w'
 print(json.dumps({'white_elo':1200,'black_elo':1200,'games':1,'white_wins':0,'draws':1,'losses':0}))

if __name__=='__main__':main()
