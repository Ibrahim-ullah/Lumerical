import numpy as np
import matplotlib.pyplot as plt
import os
import importlib.util as imp

os.add_dll_directory("C:\\Program Files\\Lumerical\\v202\\api\\python\\lumapi.py")
lumapi = imp.spec_from_file_location("Lumapi", "C:\\Program Files\\Lumerical\\v202\\api\\python\\lumapi.py")


Radii = [10e-9,25e-9,50e-9]


for i in range(len(radii)):
    fdtd = lumapi.FDTD()
    
    
    Xsize = 240e-9
    Ysize = 240e-9
    Zsize = 240e-9
    
    R = float(Radii[i])
    
    WL_Start = 200e-9    #wavelength of start and end of the wavelength
    WL_End   = 1000e-9
    
    
    
    #adding a simulation region
    fdtd.addfdtd()
    fdtd.set("x",0.0)
    fdtd.set("x span",Xsize)
    fdtd.set("y",0.0)
    fdtd.set("y span",Ysize)
    fdtd.set("z",0.0)
    fdtd.set("z span",Zsize)
    fdtd.set("dimension","3D")
    fdtd.set("simulation time",500e-15)
    fdtd.set("mesh type","uniform")
    fdtd.set("dx",2.5e-9)
    fdtd.set("dy",2.5e-9)
    fdtd.set("dz",2.5e-9)
    
    
    
    # adding a TFSF source
    fdtd.addtfsf()
    fdtd.set("x",0.0)
    fdtd.set("x span",Xsize-40e-9)
    fdtd.set("y",0.0)
    fdtd.set("y span",Ysize-40e-9)
    fdtd.set("z",0.0)
    fdtd.set("z span",Zsize-40e-9)
    fdtd.set("injection axis","x")
    fdtd.set("wavelength start",WL_Start)
    fdtd.set("wavelength stop",WL_End)
    
    
    #adding a movie monitor
    fdtd.addmovie()
    fdtd.set("x",0.0)
    fdtd.set("x span",Xsize)
    fdtd.set("y",0.0)
    fdtd.set("y span",Ysize)
    fdtd.set("z",0.0)
    
    
    #adding an object
    fdtd.addsphere()
    fdtd.set("radius",R)
    fdtd.set("material","Au (Gold) - Johnson and Christy")
    
    
    #adding a powermonitor
    fdtd.addpower()
    fdtd.set("name","DFT")
    fdtd.set("monitor type","2D Z-normal")
    fdtd.set("x",0.0)
    fdtd.set("x span",Xsize)
    fdtd.set("y",0.0)
    fdtd.set("y span",Ysize)
    fdtd.set("z",0.0)
    fdtd.setglobalmonitor("frequency points", 100)
    
    fdtd.save("GoldSphere.fsp")
    fdtd.run()
    
    E = fdtd.getresult("DFT","E")
    lambda_value = E['lambda'] #since lambda is a keyword in python
    lambda_value = lambda_value[:,0] #this will grab all the value of first column.
    
    x = E['x'] #previously x.shape returned (97,1)
    x = x[:,0] # x.shape returned (97,)
    y = E['y']
    y = y[:,0]
    z = E['z']
    
    E = E['E']
    
    Ex = E[:, :, 0, :, 0]
    Ey = E[:, :, 0, :, 0]
    Ez = E[:, :, 0, :, 0]
    
    Emag = np.sqrt(np.abs(Ex)**2 + np.abs(Ey)**2 + np.abs(Ez)**2)
    
    lambda_want = 500e-9
    index = np.argmin(np.abs(lambda_value-lambda_want))
    
    plt.contourf(y,x, Emag[:,:,index],100)
    plt.xlabel('y')  #the reason to give y as xlabel depends on the polarization direction of the source.
    plt.ylabel('x')
    plt.colorbar()
    plt.show()
    fdtd.close()
    
    

















