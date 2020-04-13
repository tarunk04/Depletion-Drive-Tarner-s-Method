
# coding: utf-8

# # Solution to Depletion Drive Reservoir using Tarner's Method

# ## Introdution 
# ------------
# <font size =3.5>This project is targeted to calculate the future performance of a depletion drive reservoir system using a computer program that can reduce the time of computation and also give more in-depth analysis at one go. This notebook is the demonstration of the project and the steps of solving for depletion drive using Tarner's Method. Tarner's Method is based on the MBE trial and error technique that uses an iterative method to approximate the cumulative oil production at each required pressure stages of depletion.</font>

# ### Python for caluation
# -----------------
# 
# Importing Useful libraries for calculation
# * utils has all the supportive fonctions for Tarner's Method.
# * pandas for tabulation of data

# In[84]:


from utils import *
import pandas as pd
from collections import OrderedDict


# ## Sample Reservoir Data
# -----------------------
# Loading saved reservoir data

# In[32]:


# Create new reservoir
# raw = create_new_reservoir()
# load reservoir
raw = load_reservoir()


# In[87]:


d = {'Bo' : pd.Series(raw['data']['Bo']),
    'Pressure (psi)' : pd.Series(raw['data']['pressure']), 
      'Bg' : pd.Series(raw['data']['Bg']),
     'Rs' : pd.Series(raw['data']['Rs']),
     'Uo/Ug' : pd.Series(raw['data']['viscocity_ratio']),
     
    } 
# pd.DataFrame(OrderedDict(d)).set_index("Pressure (psi)")


# ## Permeability Ratio Curve
# <hr>
# The relative permeability data is required by the program in instantaneous GOR equation and that can be done interploation of the values. There are several different technique. A common technique is least square fit sometimes also called as curve fit. 
# Curve fitting can be used to fit the So and Kg/Ko data and genterate a eqvivalent function for calcuation of Kg/Ko for the required value of So. 
# Using this So and the equation formed using curve fitting (Kg.Ko vs So Plot.ipynb) can be used to calculate Kg/Ko.
# 
# $\frac{K_g}{K_o} = e^{F(S_o)} $
# 
# where ${F(S_o)} = A+B S_o+CS_o^2+...+NS_o^n$  where n is the Degree of  polynomial

# In[36]:


d = { 'So (%)' : pd.Series(raw['data']['So']),
     'Kg/Ko' : pd.Series(raw['data']['rpr'])
    } 
# pd.DataFrame(d)


# In[34]:


degree = 4
coeff = get_rpr_params(raw['data']["rpr"],raw['data']['So'],degree = degree)
raw['data']['K_coeff'] = coeff
# plot_rpr_curve(raw['data']['So'],coeff,compare=True,rp=raw['data']["rpr"])


# In[90]:

#
# from IPython.display import Math
# string =""+str(np.round(coeff[0],3))
#
# for i in range(1,coeff.shape[0]):
#     if coeff[i] > 0:
#         string += '+'+str(np.round(coeff[i],3))+'S_o^'+str(i)
#     else:
#         string += str(np.round(coeff[i],3))+'S_o^'+str(i)
# Math(r'\frac{K_g}{K_o} = e^{'+string+'}')


# # Solving at Each Pressure Stage

# In[95]:


# Solving for each pressure
saturation_th = raw['data']['sth']
raw['data']['Bt'] = cal_Bt(raw['data']['Bo'], raw['data']['Bg'],raw['data']['Rs'][0],raw['data']['Rs'])
raw['data']['Gp'] = np.zeros(raw['data']['pressure'].shape[0])
raw['data']['Np']= np.zeros(raw['data']['pressure'].shape[0])
raw['data']['gor']= np.zeros(raw['data']['pressure'].shape[0])
raw['data']['gor'][0] = raw['data']['Rs'][0]
for i in range(1,raw['data']['pressure'].shape[0]):
    raw['data'] = solve_for_Np(raw['data'], Swi = raw['data']["Swi"] , index = i, sth = saturation_th,Np=raw['data']['Np'][i-1])
# Gp_cal , Np_cal, Rp_cal


# In[96]:


d = {'Pressure (psi)' : pd.Series(raw['data']['pressure']), 
      'Bg' : pd.Series(raw['data']['Bg']),
     'Rs' : pd.Series(raw['data']['Rs']),
     'Bo' : pd.Series(raw['data']['Bo']),
     'Uo/Ug' : pd.Series(raw['data']['viscocity_ratio']),
     'Cumulative Oil Production (MMSTB)' : pd.Series(np.round(raw['data']['Np']*raw['data']["oip"]/1e+6,3)),
     'Cumulative Gas Production (MMscf)' : pd.Series(np.round(raw['data']['Gp']*raw['data']["oip"]/1e+6,3)).cumsum() ,
     'Producing GOR (scf/STB)' : pd.Series(raw['data']['gor']),
     
    } 
df = pd.DataFrame(OrderedDict(d))
df.to_csv("reservoir.csv",index=False)


# In[99]:


# saving reservoir data
save_reservoir_data(raw)


# ## Reservoir Preformance

# In[98]:


# Plots
f = plt.figure(figsize=(10,8))
ax1 = f.add_subplot(111)

ax1.plot(raw["data"]["Np"]*100,raw["data"]["pressure"],label = "Pressure",color="darkorange")
ax1.tick_params(size=4,labelsize=13)
ax1.set_ylabel("Pressure (psi)",fontsize =16)
ax1.set_xlabel("OOIP Recovered (%)",fontsize =16)

ax2 = ax1.twinx()
ax2.plot(raw["data"]["Np"]*100,raw["data"]["gor"],label = "Producing GOR",color="darkviolet")
ax2.tick_params(size=4,labelsize=13)
ax2.set_ylabel("GOR (scf/STB)",fontsize =16)

plt.title("Pressure and producing GOR as a function of \nOOIP recovered.",fontsize=20)
f.legend(loc = "upper left", bbox_to_anchor=(0.15,0.80))
plt.savefig("Pressure and producing GOR as a function of OOIP recovered.")
plt.show()


# In[92]:


# Plots
f = plt.figure(figsize=(10,8))
ax1 = f.add_subplot(111)

ax1.plot(raw["data"]["pressure"],raw["data"]["Np"]*10,label = "Cumulative Oil Production",color="darkorange")
ax1.tick_params(size=4,labelsize=13)
ax1.set_ylabel("Cumulative Oil Production (MMSTB)",fontsize =16)
ax1.set_xlabel("Pressure (psi)",fontsize =16)
ax1.invert_xaxis()

ax2 = ax1.twinx()
ax2.plot(raw["data"]["pressure"],df["Cumulative Gas Production (MMscf)"],label = "Cumulative Gas Production",color="darkviolet")
ax2.tick_params(size=4,labelsize=13)
ax2.set_ylabel("Cumulative Gas Production (MMscf)",fontsize =16)


plt.title("Cumulative Gas and Oil Production as a function of \n Pressure.",fontsize=20)
f.legend(loc = "upper left", bbox_to_anchor=(0.15,0.80))
plt.savefig("Cumulative Gas and Oil Production as a function of Pressure.jpg")
plt.show()

