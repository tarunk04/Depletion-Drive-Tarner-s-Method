import numpy as np
import pandas as pd
from scipy.optimize import curve_fit  
from matplotlib import pyplot as plt
from matplotlib import ticker  
import pickle

from os import path


def valid_input(des, input_type = "single", skip = False, reason = "Input Requried"):
    user_input = ""
    while True and input_type=="single":
        try:
            user_input = input(des)
            user_input = float(user_input)
            break
        except:
            if skip != True and user_input=='':
                print(reason)
            elif skip == True and user_input=='':
                break
            else:
                print("Invalid Input. Text not allowed.")
    while True and input_type=="multi":
        try:
            user_input = input(des)
            user_input = np.float32(np.asarray(user_input.split(",")))
            break
        except:
            print("Invalid Input. Text not allowed.")
    return user_input

# Function to calculate Bg
def cal_Bg(Z , P):
    return (14.7*1*Z*(460+175))/(Pressure*1*520*5.615)

# Function to calculate Bt
def cal_Bt(Bo, Bg, Rsi, Rs):
    return Bo + (Rsi - Rs)* Bg

# Function to calculate Gmb
def cal_gmb(Np, Bt, Bti, Bg, Rss, CGppp):
    """
    Np   : Assumed Np/N ratio
    Bt   : Bt at Required Presure
    Bti  : Bt at Initial Pressure Reservoir Pressure
    Bg   : Bg at required Pressure
    Rss  : Initial GOR 
    CGppp: Cumulative Gas Production upto perivious pressure stage
    
    Return:
    Gmb : 
    """
    return (((Bt-Bti)- Np*(Bt - Rss*Bg))/ Bg ) - CGppp 

# Function to calculate So
def cal_so(Np, Bo, Boi, Swi):
#     print(Np," ",Bo," ",Boi," ",Swi)
    return (1- Np)*(Bo/Boi)*(1-Swi)

# Function to calculate Kg/Ko
def cal_kg_ko(So, *params):
    n =0
    r = np.zeros(So.shape)
    for param in params:
            r = r + param*np.power(So,n)
            n = n + 1
    return np.exp(r)

# Function to calculate R
def cal_R(kg_ko, vis_ratio, Bo, Bg, Rs):
    return kg_ko*vis_ratio*(Bo/Bg)+ Rs

# Function to calculate Ggor
def cal_Ggor(Np, Rp, R, CNppp):
    return 0.5 * (Rp + R) * (Np-CNppp)
    
# Function to calculate Gmb1 and Ggor1
def cal_trail(Np, Bo, Boi, Bt, Bti, Bg, Rs, Rss, Rp, vis_ratio, CGppp, CNppp, Swi, K_coeff, sth):
    Gmb = np.round(cal_gmb(Np , Bt, Bti, Bg, Rss, CGppp), 6)
    So = np.round(cal_so(Np, Bo, Boi, Swi), 6)
#     print(Np," ",Bo," ",Boi," ",So)
    if So < sth:
        K_ratio = np.round(cal_kg_ko(So*100, *K_coeff),6)
    else :
        K_ratio = np.asarray([0]) 
    R = np.round(cal_R(K_ratio, vis_ratio, Bo, Bg, Rs), 6)
    Ggor = np.round(cal_Ggor(Np, Rp, R, CNppp), 6)
    
    return Gmb, Ggor, Gmb-Ggor


#starting Np
# def solve_for_Np(Np_cal, Gp_cal, Rp_cal, Bo, Bg, Bt, Rs, vis_ratio, K_coeff, Swi = 0.15, delta = 0.01, index = 1, Np = 0.01, sth = 1):
#     Bti = Bt[0]
#     Boi = Bo[0]
#     Rss = Rs[0]
    
#     CGppp = np.sum(Gp_cal[:index])
#     CNppp = Np_cal[index-1]
    
#     Rp = Rp_cal[index-1]
    
# #     print(CGppp)
    
#     curr_Gmb, curr_Gogr, prev_diff= cal_trail(Np, Bo[index], Boi, Bt[index], Bti, Bg[index], Rs[index], Rss, Rp,
#                                                vis_ratio[index], CGppp, CNppp, Swi, K_coeff, sth)
# #     print(curr_Gmb, curr_Gogr)
#     sign_change = False
#     curr_diff = prev_diff
#     l_Np = Np
#     r_Np = Np
#     while abs(curr_diff) > 0.0001:
# #         print(curr_diff,"  ",Np)
#         if(sign_change == False):
#             if(curr_diff > 0):
#                 Np = Np + delta
#             else:
#                 Np = Np - delta
#         else:
#             Np = (l_Np + r_Np)*0.5 
#         curr_Gmb, curr_Gogr, curr_diff = cal_trail(Np, Bo[index], Boi, Bt[index], Bti, Bg[index], Rs[index], Rss, Rp,
#                                                vis_ratio[index], CGppp, CNppp, Swi, K_coeff, sth)
#         if(curr_diff * prev_diff < 0 ) :
#             sign_change = True
#         elif sign_change == False:
#             l_Np = Np
#             r_Np = Np
#         if(sign_change == True):
#             if(curr_diff > 0):
#                 l_Np = Np
#             elif(curr_diff < 0):
#                 r_Np = Np
#         prev_diff = curr_diff
        
#     return curr_Gmb , Np , (curr_Gmb/(Np-CNppp) * 2) - Rp_cal[index-1]


#Curve Fitting Function
def curve_fit_function(x, *params):
    n =0
    r = np.zeros(x.shape)
    for param in params:
            r = r + param*np.power(x,n)
            n = n + 1
    return r

def get_rpr_params(rp,sor,degree = 4):
#     print(rp)
#     print(sor)
#     print (degree)
    # Degree Of Polyinomial
    if rp[-1] < 1 :
            sor = sor *100
    data = [np.float64(sor),np.float64(rp)]
    # Initialisizing array with shape [1, degree]
    p = np.ones([1,degree])

    # Curve Fitting
    param, _ = curve_fit(curve_fit_function, data[0], np.log(data[1]), p0 = p) 
#     print(param)
    return param

def get_rpr(sor,params):
    return np.exp(curve_fit_function(sor, *params))

def plot_rpr_curve(sor,params,compare=False,rp=[],save=False):
    # Defining Matplotlib Figure
    f = plt.figure(num=None, figsize=(9,12))
    
    sor_range = np.arange(sor.min()-2,sor.max()+2)
    rpr = get_rpr(sor_range,params)
    
    # Sub plot
    ax = f.add_subplot(111)
    
    if compare:
        # Plotting actual data
        plt.scatter(sor , rp , s = 50, marker= 'o' , label = 'Actual data')
        # Plotting calculated data
        plt.scatter(sor,   get_rpr(sor,params), s = 70, marker= 'x', label = 'Value calculated by equation') 

    plt.plot(sor_range,  rpr, c = 'g')

    # Semi-Log Plot
    plt.yscale("log")

    # Setting Plot Tick-values
    plt.yticks([0.01,0.001,0.01,0.1,1,10,100])
    plt.xticks(np.arange(sor.min()//10*10,101,10))

    # Tick-Parameters
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.tick_params(which='both', width=1,labelsize=14)
    ax.tick_params(which='major', length=6)
    ax.tick_params(which='minor', length=3, color='0.8')

    # Plot Title
    if compare:
        plt.title("Permeability Ratio Data\n (Actual vs Calculated)",{'fontsize':20})
    else:
        plt.title("Permeability Ratio Data",{'fontsize':20})

    # Plot Axes Labels
    axis_label = ["Oil Saturation (So) in persent(%)","Kg/Ko"]
    xl = plt.xlabel(axis_label[0],fontsize=16)
    yl = plt.ylabel(axis_label[1],fontsize=16)
    
    if compare:
        # Legend Location
        plt.legend(loc = "best")

    # Grid
    plt.grid(lw = 1, ls = '-', c = "0.7", which = 'major')
    plt.grid(lw = 1, ls = '-', c = "0.9", which = 'minor')
    
    #saving plot 
    if save:
            plt.savefig("KoKgRatioVsSaturtion_curve.png")
    # Showing Final Plot
    plt.show()

def save_reservoir_data(data, save_as = False):
    if  save_as == False:
        name = data["name"]
        if name == "" or name == None:
            name = input("Enter reservoir name:")
            if path.exists(name+".save"):
                if input("File already exists. Replace?(Y/n):") != "Y":
                    print("File not saved.")                    
                    return
    else:
        name = input("Enter reservoir name:")
        if path.exists(name+".save"):
            if input("File already exists. Replace?(Y/n):") != "Y":
                print("File not saved.")
                return
    data["name"] = name
    with open(name+".save",'wb') as file:
        pickle.dump(data,file)
        
def load_reservoir():
    name = input("Enter reservoir name:")
    with open(name+".save",'rb') as file:
        data = pickle.load(file)
    return data

def solve_for_Np(data, Swi = 0.15, delta = 0.01, index = 1, Np = 0.01, sth = 1):
    Np_cal = data["Np"]
    Gp_cal = data["Gp"]
    Rp_cal = data["gor"]
    Bo = data["Bo"]
    Bg = data["Bg"]
    Bt = data["Bt"]
    Rs = data["Rs"]
    vis_ratio = data["viscocity_ratio"]
    K_coeff = data["K_coeff"]
    
    
    Bti = Bt[0]
    Boi = Bo[0]
    Rss = Rs[0]
    
    CGppp = np.sum(Gp_cal[:index])
    CNppp = Np_cal[index-1]
    
    Rp = Rp_cal[index-1]
    
#     print(CGppp)
    
    curr_Gmb, curr_Gogr, prev_diff= cal_trail(Np, Bo[index], Boi, Bt[index], Bti, Bg[index], Rs[index], Rss, Rp,
                                               vis_ratio[index], CGppp, CNppp, Swi, K_coeff, sth)
#     print(curr_Gmb, curr_Gogr)
    sign_change = False
    curr_diff = prev_diff
    l_Np = Np
    r_Np = Np
    while abs(curr_diff) > 0.0001:
#         print(curr_diff,"  ",Np)
        if(sign_change == False):
            if(curr_diff > 0):
                Np = Np + delta
            else:
                Np = Np - delta
        else:
            Np = (l_Np + r_Np)*0.5 
        curr_Gmb, curr_Gogr, curr_diff = cal_trail(Np, Bo[index], Boi, Bt[index], Bti, Bg[index], Rs[index], Rss, Rp,
                                               vis_ratio[index], CGppp, CNppp, Swi, K_coeff, sth)
        if(curr_diff * prev_diff < 0 ) :
            sign_change = True
        elif sign_change == False:
            l_Np = Np
            r_Np = Np
        if(sign_change == True):
            if(curr_diff > 0):
                l_Np = Np
            elif(curr_diff < 0):
                r_Np = Np
        prev_diff = curr_diff
        
    data["Np"][index] = Np
    data["Gp"][index] = curr_Gmb
    data["gor"][index] = (curr_Gmb/(Np-CNppp) * 2) - Rp_cal[index-1]
    return data

def create_new_reservoir():    
    name = input("Enter Resorvior Name: ")
    oip = valid_input("Enter initial oil in place (STB): ", reason="Initial oil in place is required.")
    pi = valid_input("Enter initial reservoir pressure (psi): ", reason="Initial reservoir pressure is required.")
    pb = valid_input("Enter bubble point pressure (psi): ", reason="Bubble point pressure is required.")
    Sw = valid_input("Enter Connate-water saturation (%): ", reason="Connate-water saturation is required.")
    if pi>pb :
        Cw = valid_input("Enter compressibility of water (1/psi):",skip = True)
        Cf = valid_input("Enter compressbility of formation (1/psi):",skip = True)


    Pressure = valid_input("Enter Pressures psi (for calculation)\n(comma seperated and no space):",input_type="multi")
    Rs = valid_input("Enter Rs values  (scf/STB) \n(only for pressureabove or equal to bubble point pressure):",input_type="multi")
    Bo = valid_input("Enter Formation volume factor Bo (Bbbl/STB):",input_type="multi")
    vis_ratio = valid_input("Enter Oil/Gas viscocity ratio (1/psi):",input_type="multi")
    if input("Want to enter Z(gas Compressibilty): y/n(if n then you need to input Bg)" ) == "y":
        Z = valid_input("Enter gas Compressibilty factor (1/psi):",input_type="multi")
        Bg = Bg = cal_Bg(Z , Pressure[-1*Z.shape[0]:])
    else :
        Bg = valid_input("Enter Bg (1/psi):",input_type="multi")

    So = valid_input("Enter Water Saturation (%):",input_type="multi")
    rpr = valid_input("Enter Kg/Ko :",input_type="multi")
    sth = valid_input("Threshold sw (%): ", skip=True)/100
    # Creating raw_data
    raw = { 
        "data" : { 
            "oip" : oip,
            "pi" : pi,
            "pb" : pb,
            "pressure": Pressure,
            "Rs" : Rs,
            "Bo": Bo,
            "viscocity_ratio": vis_ratio,
            "Bg": Bg,
            "So": So,
            "rpr": rpr,
            "sth": sth,
            "Swi": Sw/100
                },
        "name" : name
    }
    if pi>pb:
        raw['data']['sw'] = Sw
        raw['data']['cw'] = Cw
        raw['data']['cf'] = Cf
    return raw