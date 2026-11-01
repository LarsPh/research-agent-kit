import numpy as np, sys, os, json
import cv2
from PIL import Image
out=sys.argv[1]; os.makedirs(out+"/data/images",exist_ok=True); os.makedirs(out+"/gt",exist_ok=True); rng=np.random.default_rng(1)
def box(c,s,n): return np.array(c)+(rng.random((n,3))-0.5)*np.array(s)
red=box([0,0,0],[1,1,1],6000); grn=box([0.9,0.2,0],[0.4,0.4,0.4],1500)
xyz=np.concatenate([red,grn]); rgb=np.concatenate([np.tile([220,40,30],(len(red),1)),np.tile([40,200,60],(len(grn),1))]).astype(np.uint8)
W_,H=200,150; f=180.0; K=np.array([[f,0,W_/2],[0,f,H/2],[0,0,1]])
def look_at_c2w_gl(eye):
    eye=np.array(eye,float); fwd=-eye/np.linalg.norm(eye); up=np.array([0,0,1.]); right=np.cross(fwd,up); right/=np.linalg.norm(right); u=np.cross(right,fwd)
    M=np.eye(4); M[:3,0]=right; M[:3,1]=u; M[:3,2]=-fwd; M[:3,3]=eye; return M  # OpenGL: camera looks -Z
def render(c2w_cv, xyz, rgb):
    w2c=np.linalg.inv(c2w_cv); pc=(w2c[:3,:3]@xyz.T+w2c[:3,3:4]).T
    img=np.full((H,W_,3),255,np.uint8); zb=np.full((H,W_),np.inf)
    m=pc[:,2]>0.05; pc,c=pc[m],rgb[m]
    uv=(K@pc.T).T; uv=(uv[:,:2]/uv[:,2:]).round().astype(int)
    for (u,v),z,col in zip(uv,pc[:,2],c):
        for du in (0,1):
            for dv in (0,1):
                x,y=u+du,v+dv
                if 0<=x<W_ and 0<=y<H and z<zb[y,x]: zb[y,x]=z; img[y,x]=col
    return img
GL2CV=np.diag([1,-1,-1,1])
frames=[]
eyes=[[4*np.cos(a),4*np.sin(a),1.5] for a in np.linspace(0,2*np.pi,9)[:-1]]
for i,e in enumerate(eyes):
    c2w=look_at_c2w_gl(e); img=render(c2w@GL2CV,xyz,rgb)
    Image.fromarray(img).save(out+f"/data/images/{i:03d}.png"); frames.append({"file_path":f"images/{i:03d}.png","transform_matrix":c2w.tolist()})
json.dump({"fl_x":f,"fl_y":f,"cx":W_/2,"cy":H/2,"w":W_,"h":H,"frames":frames},open(out+"/data/transforms.json","w"),indent=1)
nov=look_at_c2w_gl([3*np.cos(0.4),3*np.sin(0.4),2.0]); json.dump({"transform_matrix":nov.tolist()},open(out+"/data/novel_view.json","w"),indent=1)
Image.fromarray(render(nov@GL2CV,xyz,rgb)).save(out+"/gt/novel_gt.png")
# "trained" model: colours learned from images loaded with cv2 (BGR)
np.savez(out+"/model.npz",xyz=xyz+rng.normal(0,0.01,xyz.shape),rgb=rgb[:,::-1].copy())
