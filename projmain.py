from generate_visuals import visualizeConcentration
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
from predictor import predictIce
from process_data import processData
import os
from report_gen import htmlReportGenerator
from hyperparams_src import modelOptimization

# get current directory
cwd = os.getcwd()

# load in dataset as xarray
print("Getting data...")  # message to terminal
ds = xr.open_dataset(r'C:\Users\Caitlin\Downloads\MODEL.ICE.HAD187001-198110.OI198111-202203.nc.gz')  # open saved data
icearray = ds.SEAICE  # get data as array
df = icearray.to_dataframe('concentration').reset_index()  # convert to dataframe

# instantiate processData class to process dataframe
df_processed = processData(df)

# call select_year function to get data for desired years
data1 = df_processed.select_year(1980, 3)
data2 = df_processed.select_year(2021, 3)

# call visualizeConcentration class to make images of data1 and data2
# this will return map of earliest and map of most recent for comparison purposes
fig1980 = visualizeConcentration(data1, 1, 1980)  # visualize latest data
plt1 = fig1980.draw_fig()  # get figures
plt.figure().clear()
fig2021 = visualizeConcentration(data2, 2, 2021)  # visualize oldest data
plt2 = fig2021.draw_fig()

img = str(cwd) + r"\figure1.png"  # get path to saved image
img2 = str(cwd) + r"\figure2.png"

plt.figure().clear()
avg_df = processData(df)
avgs = avg_df.get_averages()  # get average concentration of each year
img_avg = visualizeConcentration(avgs,1,'avg')
imgg = img_avg.trend_fig()

img3 = str(cwd) + r"\averages.png"
plt.figure().clear()
# zip lats and longs into list of coordinate pairs
coords = list(zip(df['lat'], df['lon']))
# for runtime purposes, take every n entry (will interpolate between)
reduced_coords = coords[0::3]

# prepare to run model at all coordinate points
mass_pred = df_processed.mass_prediction()

# get all unique coordinate pairs and reduce to every n entry
list_of_c = list(mass_pred['coords'].unique())
reduced_list = list_of_c[0::3]

# create empty lists to hold coordinates and predictions
coord_list = []
prediction_list = []

# loop through list and get prediction at each coordinate pair
for i in reduced_list:
    temp_df = mass_pred[mass_pred['coords'] == i]
    ice = predictIce(temp_df)
    conc, fit_df = ice.predict_concentration()
    coord_list.append(i)
    prediction_list.append(conc)

# convert results to dataframe for easier handling
lats, lons = list(zip(*coord_list))
lats = list(lats)
lons = list(lons)
df_mass = pd.DataFrame(list(zip(lats,lons,prediction_list)))
df_mass.columns = ['lat','lon','concentration']

df_mass.to_csv("Predicted_Values.csv")
df_mass.to_hdf("Predicted_Values.hdf5", key='df_mass')

optimizer = modelOptimization(fit_df,mass_pred)

# use results to get final heatmap of predicted values
pred_img = visualizeConcentration(df_mass,3,2023)
predicted_img = pred_img.draw_fig()

img4 = str(cwd) + r"\figure3.png"  # get path to saved image

# instantiate report object
report = htmlReportGenerator(img, img2, img3, df_mass, img4)

# generate html report
report.make_report()