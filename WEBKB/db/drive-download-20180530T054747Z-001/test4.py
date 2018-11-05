f1=open("ann4.txt")

f3=open("rewriteformulas_whole.txt")
import sys

fid=[]
f=[]
ff={}
for i in f3:
	p=i.strip("\n '").split(":")
	ff[p[0]]=p[1]
	f.append(p[1])
f11=open("proof_f4.txt","w")
#f12=open("proof2.txt","w")
#f13=open("proof3.txt","w")
#f14=open("proof4.txt","w")
#f15=open("proof5.txt","w")
L1=[]
L2=[]
L3=[]
L4=[]
L5=[]
L11=[]
L12=[]
L13=[]
L14=[]
L15=[]
for i in f1:
	p=i.strip("\n").split(":")
	#if '4.0' in p[1]:
	if len(p)>2:
		jj=p[1].strip("\n ' ").split(",")
		for k in jj:
			 i1=k.strip("'")
			 L1.append(i1)
		for i2 in L1:
				#print(i2)
				i3=i2.strip(" ' ")
				for tt in f:
					#print(tt)
					if i2 in tt:
						f11.write(str(tt)+"\n")
						print(tt)
		jj1=p[2].strip("\n \t").split(",")
		for kk in jj1:
				m=str(kk)+"(p2)"
				for tt in f:
					if m in tt:
						f11.write(str(tt)+"\n")
						print(tt)
		