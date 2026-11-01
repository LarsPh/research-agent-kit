import numpy as np, sys, os
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out=sys.argv[1]; os.makedirs(out+"/renders",exist_ok=True)
names=["pelvis","spine","head","l_shoulder","l_hand","r_shoulder","r_hand","l_hip","l_knee","l_foot","r_hip","r_knee","r_foot","nose"]
parents=[-1,0,1,1,3,1,5,0,7,8,0,10,11,2]
# Y up, character faces +Z, left side is +X
rest=np.array([[0,1,0],[0,1.4,0],[0,1.7,0],[0.2,1.45,0],[0.5,1.1,0.1],[-0.2,1.45,0],[-0.5,1.6,0.25],[0.1,1,0],[0.1,0.55,0.05],[0.1,0.1,0],[-0.1,1,0],[-0.1,0.55,0.05],[-0.1,0.1,0],[0,1.68,0.12]])
T=60; fps=30.0
def rot_y(a):
    c,s=np.cos(a),np.sin(a); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
root=[];J=[]
for t in range(T):
    a=0.4*np.sin(2*np.pi*t/T)  # sway
    R=rot_y(a); p=rest.copy()
    p[6]+= [0,0.15*np.sin(2*np.pi*t/20),0]  # right hand waves
    J.append((R@p.T).T+[0,0,0.02*t]); root.append(R)
J=np.array(J); root=np.array(root)
F=np.diag([-1,1,1])  # exporter bug: x negated
Jb=J@F.T; rootb=np.einsum("ij,tjk,kl->til",F,root,F)
np.savez(out+"/motion_a.npz",joints=J,root_rot=root,fps=fps,names=np.array(names),parents=np.array(parents))
np.savez(out+"/motion_b.npz",joints=Jb,root_rot=rootb,fps=fps,names=np.array(names),parents=np.array(parents))
for tag,jj in [("a",J),("b",Jb)]:
    fig,axs=plt.subplots(1,4,figsize=(10,3.5))
    for ax,t in zip(axs,[0,15,30,45]):
        p=jj[t]
        for i,pa in enumerate(parents):
            if pa>=0: ax.plot([p[i,0],p[pa,0]],[p[i,1],p[pa,1]],'k-',lw=2)
        ax.scatter(p[:,0],p[:,1],s=10); ax.set_xlim(-1,1); ax.set_ylim(0,2); ax.set_aspect('equal'); ax.set_title(f"frame {t}"); ax.axis('off')
    fig.suptitle(f"motion_{tag} (front camera)"); fig.savefig(out+f"/renders/{tag}.png",dpi=80); plt.close(fig)
open(out+"/retarget.py","w").write('''"""Retarget a motion clip onto the target rig: root rotation -> quaternion -> rig yaw."""
import sys, numpy as np
from scipy.spatial.transform import Rotation as R
m = np.load(sys.argv[1])
q = R.from_matrix(m["root_rot"]).as_quat()          # (T,4) x,y,z,w
yaw = R.from_quat(q).as_euler("yxz")[:, 0]
fwd = np.stack([np.sin(yaw), np.zeros_like(yaw), np.cos(yaw)], 1)
print("target rig forward at frames 0,15,30,45:")
for t in [0, 15, 30, 45]:
    print(t, np.round(fwd[t], 3))
np.save(sys.argv[1].replace(".npz", "_rig_forward.npy"), fwd)
''')
open(out+"/README.md","w").write("motion_a.npz and motion_b.npz are the same take exported from two exporters. joints: (T,J,3) world positions; root_rot: (T,3,3); fps; names; parents. Rig convention: Y up, character faces +Z.\n")
