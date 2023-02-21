import os
from vmtk import vmtkscripts
import numpy as np
import csv

folder_path = "C:/Users/Ajay Pediredla/Documents/ns"

# List all the files in the folder
files = os.listdir(folder_path)



# Function to calculate diameter reduction
def calculate_diameter_reduction(radii):
    normal_radius = np.max(radii)
    stenotic_radius = np.min(radii)
    diameter_reduction = (normal_radius - stenotic_radius) / normal_radius
    return diameter_reduction

# Function to calculate cross-sectional area reduction
def calculate_cross_sectional_area_reduction( radii):
    max_area = np.pi * (np.max(radii) / 2) ** 2
    area = np.pi * (np.min(radii) / 2) ** 2
    area_reduction = (max_area - area)/ max_area
    return area_reduction




with open('non_stenosis_data.csv',mode='w',newline='') as file:

# Loop through each file and read it
    writer=csv.writer(file)
    writer.writerow(['filename','type','radiusArray','Centerline_points','coefficent_of_variance'])
    for file in files:
    # Create the file path by concatenating the folder path with the file name
        file_path = os.path.join(folder_path, file)
        print(file_path)
        surfaceReader = vmtkscripts.vmtkSurfaceReader()
        surfaceReader.InputFileName = file_path
        surfaceReader.Execute()
        clNumpyAdaptor = vmtkscripts.vmtkCenterlinesToNumpy()
        clNumpyAdaptor.Centerlines = surfaceReader.Surface
        clNumpyAdaptor.Execute()
        numpyCenterlines = clNumpyAdaptor.ArrayDict

        RadiusArray = np.array(numpyCenterlines['PointData']['MaximumInscribedSphereRadius'])
        Centerlines_Points=np.array(numpyCenterlines['Points'])
        RadiusArraysize=len(RadiusArray)
        print("numberOfSpeheres: ",RadiusArraysize)


        mean_value=np.mean(RadiusArray)
        standard_deviation= np.std(RadiusArray)
        ration_of_cv=(standard_deviation/mean_value)*100
        # print("std: ",standard_deviation)
        # print("cv: ",ration_of_cv)

        # Relative Gradient
        # gradient = np.gradient(RadiusArray)
        # rel_gradient = gradient / mean_value
        # max_idx = np.argmax(rel_gradient)
        writer.writerow([file,'non_stenosis',RadiusArray,Centerlines_Points,ration_of_cv])
        # break


    
