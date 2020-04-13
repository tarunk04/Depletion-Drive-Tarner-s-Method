# Depletion Drive Tarner's Method
The purpose of this program is to calculate the future performance of a depletion drive reservoir using `Tarner's method`. Tarner's Method uses the iterative approach to calculate future performance. To achieve the high-speed calculation, Numerical Method is used.

# Algorithm Flow Diagram

![Flow chat](Flow%20Chart.jpg)

# Requirments
* Python 3.6 or higher
* NumPy
* Pandas
* Matplotlib

# To get started

* Clone this repository:  
```console
git clone https://github.com/tarunk04/Depletion-Drive-Tarner-s-Method.git
```
  or click `Download ZIP` in the right panel of repository and extract it.
* Go App folder 
* Run `app.py`.
* Follow the instruction.
* It will solve and save the plots and save calculated data as `reservoir.csv`.

# Permeability Ratio Curve

The relative permeability data is required by the program in the instantaneous GOR equation, and that can be done interpolation of the values. There are several different techniques. A common technique is a least-square fit, sometimes also called a curve fit. 
Curve fitting can be used to fit the So and Kg/Ko data and generate an equivalent function for calculation of Kg/Ko for the required value of So. 
Using this, So and the equation formed using curve fitting (Kg.Ko vs. So Plot.ipynb) can be used to calculate Kg/Ko.

<img src="https://render.githubusercontent.com/render/math?math=\frac{K_g}{K_o} = e^{F(S_o)}">

**where**

<img src="https://render.githubusercontent.com/render/math?math={F(S_o)} = A %2B BS_o %2B CS_o^2 %2B ... %2B NS_o^n"> where n is the Degree of  polynomial

**where**
A, B, C, .., N is computed using curve fitting.

![sample](KoKgRatioVsSaturtion_curve.png) 

# Preformance
Tabulation of calculated data is saved in `reservoir.csv` and plot generated is also saved in the working directory.
Example plots and table:
![table1](Table1.png)
![plot1](https://github.com/tarunk04/Depletion-Drive-Tarner-s-Method/blob/master/Pressure%20and%20producing%20GOR%20as%20a%20function%20of%20OOIP%20recovered.png?raw=true)
![plot2](https://github.com/tarunk04/Depletion-Drive-Tarner-s-Method/blob/master/Cumulative%20Gas%20and%20Oil%20Production%20as%20a%20function%20of%20Pressure.jpg)


# Example Notebook
Two examples have been included in the repository for understanding the working of the program. Go to the example folder to check or click the links below.

* [Example 1](https://github.com/tarunk04/Depletion-Drive-Tarner-s-Method/blob/master/Examples/Tarner's%20Method%20Example%201.ipynb)
* [Example 2](https://github.com/tarunk04/Depletion-Drive-Tarner-s-Method/blob/master/Examples/Tarner's%20Method%20Example%202.ipynb)

# About the Project
This project is developed by **Tarun Kumar** of **IIT (ISM), Dhanbad** under the supervision of **Prof. Rajeev Upadhyay, Department of Petroleum Engineering, IIT (ISM) Dhanbad**.
