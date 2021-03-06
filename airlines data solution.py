

import pandas as pd
Airlines = pd.read_csv("Airlines.csv") #read csv file
month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'] #created the list of months

import numpy as np
p = Airlines["Month"][0] # p variable starts with 0 index 
p[0:3] # creating as quarterly of month
Airlines['months']= 0 #creating extra column name as months

for i in range(96):  #159 as per data avability
    p= Airlines["Month"][i] #i = 159
    Airlines['months'][i]= p[0:3]  #[0:3] slicing for the name of the months as 'Jan'
    
month_dummies = pd.DataFrame(pd.get_dummies(Airlines['months']))   # get_dummies is used to convert categorical variable into dummy variable.  String to append DataFrame column names 
Airlines1 = pd.concat([Airlines,month_dummies],axis = 1) #amtrak1 = amtrak + month_dummies just the concatination

Airlines1["t"] = np.arange(1,97)  # creating a column for t
Airlines1["t_squared"] = Airlines1["t"]*Airlines1["t"] # creating a column for t square
Airlines1.columns

Airlines1["log_Passenger"] = np.log(Airlines1["Passengers"]) # creating a column for log value of ridership
Airlines.rename(columns={"Passengers": 'Passengers'}, inplace=True) # you can rename the column name by using this rename funtion
Airlines.Passengers.plot() #plotting the graph

#Amtrak1.log_Rider.plot()

Train = Airlines1.head(90)
Test = Airlines1.tail(6)

# to change the index value in pandas data frame 
# Test.set_index(np.arange(1,13))



####################### L I N E A R ##########################
import statsmodels.formula.api as smf 

linear_model = smf.ols('Passengers~t',data=Train).fit()
pred_linear =  pd.Series(linear_model.predict(pd.DataFrame(Test['t'])))
rmse_linear = np.sqrt(np.mean((np.array(Test['Passengers'])-np.array(pred_linear))**2))
rmse_linear




##################### Exponential ##############################

Exp = smf.ols('log_Passenger~t',data=Train).fit()
pred_Exp = pd.Series(Exp.predict(pd.DataFrame(Test['t'])))
rmse_Exp = np.sqrt(np.mean((np.array(Test['Passengers'])-np.array(np.exp(pred_Exp)))**2))
rmse_Exp




#################### Quadratic ###############################

Quad = smf.ols('Passengers~t+t_squared',data=Train).fit()
pred_Quad = pd.Series(Quad.predict(Test[["t","t_squared"]]))
rmse_Quad = np.sqrt(np.mean((np.array(Test['Passengers'])-np.array(pred_Quad))**2))
rmse_Quad


################### Additive seasonality ########################

add_sea = smf.ols('Passengers~Jan+Feb+Mar+Apr+May+Jun+Jul+Aug+Sep+Oct+Nov',data=Train).fit()
pred_add_sea = pd.Series(add_sea.predict(Test[['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov']]))
rmse_add_sea = np.sqrt(np.mean((np.array(Test['Passengers'])-np.array(pred_add_sea))**2))
rmse_add_sea



################## Additive Seasonality Quadratic ############################

add_sea_Quad = smf.ols('Passengers~t+t_squared+Jan+Feb+Mar+Apr+May+Jun+Jul+Aug+Sep+Oct+Nov',data=Train).fit()
pred_add_sea_quad = pd.Series(add_sea_Quad.predict(Test[['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','t','t_squared']]))
rmse_add_sea_quad = np.sqrt(np.mean((np.array(Test['Passengers'])-np.array(pred_add_sea_quad))**2))
rmse_add_sea_quad 

################## Multiplicative Seasonality ##################

Mul_sea = smf.ols('log_Passenger~Jan+Feb+Mar+Apr+May+Jun+Jul+Aug+Sep+Oct+Nov',data = Train).fit()
pred_Mult_sea = pd.Series(Mul_sea.predict(Test))
rmse_Mult_sea = np.sqrt(np.mean((np.array(Test['Passengers'])-np.array(np.exp(pred_Mult_sea)))**2))
rmse_Mult_sea

##################Multiplicative Additive Seasonality ###########

Mul_Add_sea = smf.ols('log_Passenger~t+Jan+Feb+Mar+Apr+May+Jun+Jul+Aug+Sep+Oct+Nov',data = Train).fit()
pred_Mult_add_sea = pd.Series(Mul_Add_sea.predict(Test))
rmse_Mult_add_sea = np.sqrt(np.mean((np.array(Test['Passengers'])-np.array(np.exp(pred_Mult_add_sea)))**2))
rmse_Mult_add_sea 



################## Testing #######################################

data = {"MODEL":pd.Series(["rmse_linear","rmse_Exp","rmse_Quad","rmse_add_sea","rmse_add_sea_quad","rmse_Mult_sea","rmse_Mult_add_sea"]),"RMSE_Values":pd.Series([rmse_linear,rmse_Exp,rmse_Quad,rmse_add_sea,rmse_add_sea_quad,rmse_Mult_sea,rmse_Mult_add_sea])}
table_rmse=pd.DataFrame(data)
table_rmse
# so rmse_add_sea_quad has the least value among the models prepared so far


 



# Predicting new values 

predict_data = pd.read_csv("Predict_new.csv")
model_full = smf.ols('Passengers~t+t_squared+Jan+Feb+Mar+Apr+May+Jun+Jul+Aug+Sep+Oct+Nov',data=Airlines1).fit()

pred_new  = pd.Series(add_sea_Quad.predict(predict_data))
pred_new
predict_data["forecasted_Passengers"] = pd.Series(pred_new)
