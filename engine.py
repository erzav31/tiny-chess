import json,os,sys,urllib.request
U=os.environ.get("MAKEFUN_ENV_URL") or sys.exit("MAKEFUN_ENV_URL is not set")
V=[0,100,320,330,500,900,0]
W=[0,0,12,10,6,4,-6]
KN=[-33,-31,-18,-14,14,18,31,33]
KG=[-17,-16,-15,-1,1,15,16,17]
DG=[-17,-15,15,17]
RG=[-16,-1,1,16]
B=[0]*128
S=1
CR=0
EP=-1
K=[4,116]
Z=0
SC=0
PH=6400
NB=[2,2]
R=[]
_x=987654321
for _ in range(833):
    _x=(6364136223846793005*_x+1442695040888963407)&0xFFFFFFFFFFFFFFFF
    R.append(_x)
TT={}
KI=[[0,0] for _ in range(128)]
NOD=0
BUD=120000
class Out(Exception):pass
def mv(f,t,pr):return f|(t<<7)|(pr<<14)
def uci(m):
    f=m&127;t=(m>>7)&127
    s=chr(97+(f&7))+str((f>>4)+1)+chr(97+(t&7))+str((t>>4)+1)
    p=m>>14
    return s+('xpnbrq'[p] if p else '')
def atk(sq,by):
    if by>0:
        if not (sq-15)&0x88 and B[sq-15]==1:return 1
        if not (sq-17)&0x88 and B[sq-17]==1:return 1
    else:
        if not (sq+15)&0x88 and B[sq+15]==-1:return 1
        if not (sq+17)&0x88 and B[sq+17]==-1:return 1
    for o in KN:
        t=sq+o
        if not t&0x88 and B[t]==2*by:return 1
    for o in KG:
        t=sq+o
        if not t&0x88 and B[t]==6*by:return 1
    for o in DG:
        t=sq+o
        while not t&0x88:
            p=B[t]
            if p:
                if p==3*by or p==5*by:return 1
                break
            t+=o
    for o in RG:
        t=sq+o
        while not t&0x88:
            p=B[t]
            if p:
                if p==4*by or p==5*by:return 1
                break
            t+=o
    return 0
def gen(cap):
    ms=[]
    for sq in range(128):
        if sq&0x88:continue
        p=B[sq]
        if p*S<=0:continue
        a=abs(p)
        if a==1:
            d=16*S
            lr=7 if S>0 else 0
            sr=1 if S>0 else 6
            t=sq+d
            if not t&0x88 and B[t]==0:
                if not cap:
                    ms.append(mv(sq,t,5 if (t>>4)==lr else 0))
                    if (sq>>4)==sr and B[t+d]==0:ms.append(mv(sq,t+d,0))
                elif (t>>4)==lr:ms.append(mv(sq,t,5))
            for dd in (d-1,d+1):
                t=sq+dd
                if t&0x88:continue
                if B[t]*S<0 or t==EP:ms.append(mv(sq,t,5 if (t>>4)==lr else 0))
        elif a==2 or a==6:
            for o in KN if a==2 else KG:
                t=sq+o
                if not t&0x88 and B[t]*S<=0 and (not cap or B[t]!=0):ms.append(mv(sq,t,0))
            if a==6 and not cap:
                if S>0 and sq==4:
                    if CR&1 and B[5]==0 and B[6]==0 and not atk(4,-1) and not atk(5,-1) and not atk(6,-1):ms.append(mv(4,6,0))
                    if CR&2 and B[1]==0 and B[2]==0 and B[3]==0 and not atk(4,-1) and not atk(3,-1) and not atk(2,-1):ms.append(mv(4,2,0))
                if S<0 and sq==116:
                    if CR&4 and B[117]==0 and B[118]==0 and not atk(116,1) and not atk(117,1) and not atk(118,1):ms.append(mv(116,118,0))
                    if CR&8 and B[113]==0 and B[114]==0 and B[115]==0 and not atk(116,1) and not atk(115,1) and not atk(114,1):ms.append(mv(116,114,0))
        else:
            for o in DG if a==3 else RG if a==4 else DG+RG:
                t=sq+o
                while not t&0x88:
                    q=B[t]
                    if q==0:
                        if not cap:ms.append(mv(sq,t,0))
                    elif q*S<0:
                        ms.append(mv(sq,t,0));break
                    else:break
                    t+=o
    return ms
def sv(p,sq):
    a=abs(p)
    if a==6:return 0
    f=sq&7;r=sq>>4
    c=7-max(abs(2*f-7),abs(2*r-7))
    x=V[a]+(W[a]*c)//2
    if a==1:x+=(r if p>0 else 7-r)*5
    elif a==4 and ((r==6 and p>0) or (r==1 and p<0)):x+=20
    return x if p>0 else -x
def kc(sq):
    return 7-max(abs(2*(sq&7)-7),abs(2*(sq>>4)-7))
def make(m):
    global S,CR,EP,Z,SC,PH,NB
    f=m&127;t=(m>>7)&127;pr=m>>14
    p=B[f];c=B[t]
    f6=(f&7)+((f>>4)<<3);t6=(t&7)+((t>>4)<<3)
    Z^=R[(p+6)*64+f6]
    epc=-1;cp=0;rf=-1;rt=-1
    if abs(p)==1 and t==EP and c==0:
        epc=t-16*S;cp=B[epc]
        Z^=R[(cp+6)*64+(epc&7)+((epc>>4)<<3)]
        B[epc]=0
    elif c:Z^=R[(c+6)*64+t6]
    np=pr*S if pr else p
    Z^=R[(np+6)*64+t6]
    B[t]=np;B[f]=0
    SC-=sv(p,f)
    if c:SC-=sv(c,t)
    if epc>=0:SC-=sv(cp,epc)
    SC+=sv(np,t)
    if c and abs(c)!=1:PH-=V[abs(c)]
    if abs(c)==3:NB[0 if c<0 else 1]-=1
    if pr:PH+=V[pr]-100
    if abs(p)==6:
        K[0 if p>0 else 1]=t
        if t-f==2:rf,rt=f+3,f+1
        elif f-t==2:rf,rt=f-4,f-1
        if rf>=0:
            r=B[rf]
            Z^=R[(r+6)*64+(rf&7)+((rf>>4)<<3)];Z^=R[(r+6)*64+(rt&7)+((rt>>4)<<3)]
            B[rt]=r;B[rf]=0
            SC-=sv(r,rf);SC+=sv(r,rt)
    oe=EP;oc=CR
    EP=t-16*S if abs(p)==1 and abs(t-f)==32 else -1
    if abs(p)==6:CR&=~(3 if p>0 else 12)
    if f==0 or t==0:CR&=~2
    if f==7 or t==7:CR&=~1
    if f==112 or t==112:CR&=~8
    if f==119 or t==119:CR&=~4
    Z^=R[832]
    S=-S
    return (c,epc,cp,oe,oc,rf,rt,np,p)
def unmake(m,u):
    global S,CR,EP,Z,SC,PH,NB
    f=m&127;t=(m>>7)&127
    c,epc,cp,oe,oc,rf,rt,np,p=u
    S=-S
    Z^=R[832]
    CR=oc;EP=oe
    f6=(f&7)+((f>>4)<<3);t6=(t&7)+((t>>4)<<3)
    Z^=R[(p+6)*64+f6]
    if epc>=0:Z^=R[(cp+6)*64+(epc&7)+((epc>>4)<<3)]
    elif c:Z^=R[(c+6)*64+t6]
    Z^=R[(np+6)*64+t6]
    SC+=sv(p,f)
    if c:SC+=sv(c,t)
    if epc>=0:SC+=sv(cp,epc)
    SC-=sv(np,t)
    if c and abs(c)!=1:PH+=V[abs(c)]
    if abs(c)==3:NB[0 if c<0 else 1]+=1
    if abs(np)!=abs(p):PH-=V[abs(np)]-100
    if rf>=0:
        r=B[rt]
        Z^=R[(r+6)*64+(rf&7)+((rf>>4)<<3)];Z^=R[(r+6)*64+(rt&7)+((rt>>4)<<3)]
        B[rf]=r;B[rt]=0
        SC+=sv(r,rf);SC-=sv(r,rt)
    B[f]=p;B[t]=c
    if epc>=0:B[epc]=cp
    if abs(p)==6:K[0 if p>0 else 1]=f
def legal(ms):
    out=[]
    for m in ms:
        u=make(m)
        if not atk(K[0] if S<0 else K[1],S):out.append(m)
        unmake(m,u)
    return out
def ev():
    k=8*(kc(K[0])-kc(K[1]))*(6400-2*PH)//6400
    b=(30 if NB[0]==2 else 0)-(30 if NB[1]==2 else 0)
    return (SC+k+b)*S
def order(ms,tt,ki):
    ms.sort(key=lambda m:(0 if m==tt else 1 if m==ki[0] or m==ki[1] else 2,-(V[abs(B[(m>>7)&127])] if B[(m>>7)&127] else 0)))
def qs(a,b,pl):
    global NOD
    NOD+=1
    if NOD>BUD:raise Out
    st=ev()
    if st>=b:return b
    if st>a:a=st
    if pl>12:return a
    ms=gen(1)
    order(ms,0,(0,0))
    for m in ms:
        t=(m>>7)&127
        v=B[t]
        vv=100 if t==EP else V[abs(v)]
        if st+vv+(800 if m>>14 else 150)<a:continue
        u=make(m)
        try:
            if atk(K[0] if S<0 else K[1],S):continue
            s=-qs(-b,-a,pl+1)
        finally:unmake(m,u)
        if s>=b:return b
        if s>a:a=s
    return a
def sr(d,a,b,pl):
    global NOD,S,EP,Z
    NOD+=1
    if NOD>BUD:raise Out
    e=TT.get(Z)
    tt=0
    if e and e[0]>=d:
        tt=e[3]
        if e[2]==0:return e[1]
        if e[2]==1 and e[1]>=b:return e[1]
        if e[2]==2 and e[1]<=a:return e[1]
    chk=atk(K[0 if S>0 else 1],-S)
    if chk:d+=1
    if d==0:return qs(a,b,0)
    if d>=3 and PH>900 and not chk and ev()>=b:
        oe=EP
        EP=-1;S=-S;Z^=R[832]
        try:s=-sr(d-3,-b,-b+1,pl+1)
        finally:
            S=-S;Z^=R[832];EP=oe
        if s>=b:return b
    ms=gen(0)
    order(ms,tt,KI[pl] if pl<128 else (0,0))
    best=-10**9;bm=0;fl=2;nleg=0
    for m in ms:
        u=make(m)
        try:
            if atk(K[0] if S<0 else K[1],S):continue
            nleg+=1
            s=-sr(d-1,-b,-a,pl+1)
        finally:unmake(m,u)
        if s>best:best=s;bm=m
        if s>a:a=s;fl=0
        if a>=b:
            fl=1
            if pl<128 and B[(m>>7)&127]==0 and not (m>>14) and m!=KI[pl][0]:
                KI[pl][1]=KI[pl][0];KI[pl][0]=m
            break
    if not nleg:return -100000+pl if atk(K[0 if S>0 else 1],-S) else 0
    if len(TT)>200000:TT.clear()
    TT[Z]=(d,best,fl,bm)
    return best
def root(legal_uci,hist=()):
    global NOD
    NOD=0
    ms=legal(gen(0))
    if not ms:return legal_uci[0]
    if len(ms)==1:return uci(ms[0]) if uci(ms[0]) in legal_uci else legal_uci[0]
    order(ms,0,(0,0))
    best=ms[0]
    scored=[]
    for d in range(1,10):
        try:
            sc=[]
            a=-10**9
            for i,m in enumerate(ms):
                u=make(m)
                try:
                    if i==0:s=-sr(d-1,-10**9,10**9,1)
                    else:
                        s=-sr(d-1,-a-1,-a,1)
                        if s>a:s=-sr(d-1,-10**9,-a,1)
                finally:unmake(m,u)
                sc.append((s,m))
                if s>a:a=s
            sc.sort(key=lambda t:-t[0])
            best=sc[0][1]
            scored=sc
            ms=[m for _,m in sc]
        except Out:break
    for s,m in scored:
        u=make(m)
        z=Z
        unmake(m,u)
        if hist.count(z)<2:
            best=m
            break
    u=uci(best)
    return u if u in legal_uci else legal_uci[0]
def load(fen):
    global S,CR,EP,Z,SC,PH,NB
    B[:]=[0]*128
    parts=fen.split()
    mp={'p':-1,'n':-2,'b':-3,'r':-4,'q':-5,'k':-6,'P':1,'N':2,'B':3,'R':4,'Q':5,'K':6}
    for ri,row in enumerate(parts[0].split('/')):
        r=7-ri;f=0
        for ch in row:
            if ch.isdigit():f+=int(ch)
            else:
                sq=r*16+f;B[sq]=mp[ch]
                if abs(mp[ch])==6:K[0 if mp[ch]>0 else 1]=sq
                f+=1
    S=1 if parts[1]=='w' else -1
    CR=0
    if len(parts)>2:
        for ch in parts[2]:
            if ch=='K':CR|=1
            elif ch=='Q':CR|=2
            elif ch=='k':CR|=4
            elif ch=='q':CR|=8
    EP=-1
    if len(parts)>3 and parts[3]!='-':
        e=parts[3];EP=(ord(e[0])-97)+(int(e[1])-1)*16
    Z=0
    SC=0
    PH=0
    NB=[0,0]
    for sq in range(128):
        if sq&0x88:continue
        p=B[sq]
        if p:
            Z^=R[(p+6)*64+(sq&7)+((sq>>4)<<3)]
            SC+=sv(p,sq)
            if abs(p)!=1 and abs(p)!=6:PH+=V[abs(p)]
            if abs(p)==3:NB[0 if p>0 else 1]+=1
    if S<0:Z^=R[832]
def post(path,body):
    req=urllib.request.Request(U+path,data=json.dumps(body).encode(),headers={"content-type":"application/json"})
    try:
        with urllib.request.urlopen(req) as r:return json.load(r)
    except urllib.error.HTTPError as e:sys.exit(f"{path}: HTTP {e.code}")
if __name__=="__main__":
    HIST=[]
    while True:
        g=post("/game",{})
        if g["status"]=="done":break
        HIST=[]
        while g["status"]=="your_move":
            load(g["fen"])
            HIST.append(Z)
            MV=root(g["legal_moves"],HIST)
            for m in legal(gen(0)):
                if uci(m)==MV:
                    u=make(m);HIST.append(Z);unmake(m,u)
                    break
            g=post("/move",{"game":g["game"],"move":MV})
        print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
    print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)
