import numpy as np, sys, os
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out=sys.argv[1]; os.makedirs(out+"/renders",exist_ok=True); rng=np.random.default_rng(0)
def box(c,s,n):
    return np.array(c)+(rng.random((n,3))-0.5)*np.array(s)
# a chair: seat, back (at -Z), 4 legs; Y up
parts=[box([0,0.45,0],[0.9,0.08,0.9],3000),box([0,0.95,-0.42],[0.9,0.9,0.08],2500)]
for x in (-0.4,0.4):
    for z in (-0.4,0.4): parts.append(box([x,0.2,z],[0.07,0.42,0.07],400))
P=np.concatenate(parts); P-=P.mean(0); P/=np.linalg.norm(P,axis=1).max()
col=np.tile([0.6,0.35,0.2],(len(P),1))+rng.normal(0,0.03,(len(P),3))
op=np.full(len(P),0.9)
def save(name,P,col,op): np.savez(out+f"/{name}.npz",xyz=P,rgb=np.clip(col,0,1),opacity=op)
save("method_a",P+rng.normal(0,0.004,P.shape),col,op)
# method B: same quality, but in its own frame: scale 2.5, rotated 90 deg about Y, shifted, plus faint floaters
c,s=np.cos(np.pi/2),np.sin(np.pi/2); Ry=np.array([[c,0,s],[0,1,0],[-s,0,c]])
PB=(Ry@(P*2.5).T).T+[0.6,0.3,0]+rng.normal(0,0.01,P.shape)
fl=rng.uniform(-6,6,(300,3)); PB=np.concatenate([PB,fl]); colB=np.concatenate([col,rng.random((300,3))]); opB=np.concatenate([op,np.full(300,0.03)])
save("method_b",PB,colB,opB)
render=r'''"""Shared renderer for both methods: orthographic front view (camera on +Z looking at -Z), fixed bounds."""
import sys, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
def draw(ax, path, title):
    d = np.load(path); p, c, o = d["xyz"], d["rgb"], d["opacity"]
    order = np.argsort(p[:, 2])
    ax.scatter(p[order, 0], p[order, 1], c=c[order], s=2, alpha=np.clip(o[order], 0, 1))
    ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_aspect("equal"); ax.set_title(title); ax.axis("off")
fig, axs = plt.subplots(1, 2, figsize=(8, 4))
draw(axs[0], "method_a.npz", "Method A"); draw(axs[1], "method_b.npz", "Method B")
fig.savefig("renders/compare.png", dpi=90)
'''
open(out+"/render.py","w").write(render)
open(out+"/README.md","w").write("Gaussian-splat outputs (centres, colours, opacity) of two methods on the same chair capture. render.py draws both with the same camera.\n")
