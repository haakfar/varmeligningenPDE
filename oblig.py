import numpy as np
from matplotlib import pyplot as plt


#Denne koden skal produsere en 2d-graf som bruker farge til å illustrere temperaturutviklingen på en gullplate.
#Platen er diskretisert i et gitt antall punkter, som alle får en gitt starttemperatur. Ettersom tiden går, vil hvert punkt få en ny temperatur basert på gjennomsnittet av sine nabopunkter.

#Den termiske diffusiviteten til gull, hentet fra Wikipedia: https://en.wikipedia.org/wiki/Thermal_diffusivity er 127 mm^2/s
a = 127

#Sidelengden til platen (den er kvadratisk) [mm]
lengde = 100 

#Antallet punkter i én retning  [punkter]
punkter = 100

#Tiden simulasjonen skal vare [s]
tid = 10

#Starttemperatur for platen: [C]
T_start = 30



#Dette er stegstørrelsen, altså avstanden mellom hvert punkt
dx = lengde/punkter
dy = lengde/punkter


#Tidssteg, denne utregningen gjøres siden det er et krav om hvor lite tidssteget må være for å få en god fungerende simulasjon
dt =  min(dy**2 / (4 * a)  ,  dx**2 / (4 * a))


tidspunkt = int(tid/dt)


u=np.zeros((punkter,punkter)) + T_start 

#Startkondisjon basert på ligningen T_xy = x + 100*sin(y):

for i in range(1,punkter -1):
    for j in range(1,punkter -1):
        u[i,j] = 100*np.sin((i)/10)+ j  #100*np.sin((j/dy)/10)
        


#Randkrav

u[0,:] = np.linspace(20,20,punkter)
u[-1,:] = np.linspace(20,20,punkter)

u[:,0] = np.linspace(20,20,punkter)
u[:,-1] = np.linspace(20,20,punkter)


fig , akse = plt.subplots()

prosent_farge = akse.pcolormesh(u, cmap=plt.cm.jet, vmin=0, vmax=100)
plt.colorbar(prosent_farge, ax=akse)


#Simulator

teller = 0

while teller < tid :
    w = u.copy()

    for i in range(1, punkter -1):
        for j in range(1, punkter -1):

            #Avgjør endring i temperatur i x og y-retning for hvert punkt
            dd_ux = (w[i-1,j] - 2*w[i,j]+ w[i+1,j])/dx**2
            dd_uy = (w[i,j-1] - 2*w[i,j]+ w[i,j+1])/dy**2


            #regner ut hva temperaturen i hvert punkt skal bli basert på diffusiviteten a, tidssteget samt temperaturendringen
            #i hver retning som er regnet ut over
            u[i,j]=dt * a * (dd_ux + dd_uy) + w[i,j]
    
    teller += dt

    #Oppdatering av plottet

    prosent_farge.set_array(u)

    akse.set_title("Distribusjonen på t: {:.3f} [s].".format(teller) )
    plt.pause(0.01)

plt.show()