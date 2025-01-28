import pandas as pd 
import load_files
from pathlib import Path
import os 



def main():
    
    # Main output directory
    main_output_path = Path("/home/mjm/Documents/UBC/Research/biopsylocalization-new/Data/Output data/MC_sim_out- Date-Jan-14-2025 Time-14,25,24")  # Ensure the directory is a Path object
    
    ### Load Dataframes 

    # Set csv directory
    csv_directory = main_output_path.joinpath("Output CSVs")
    cohort_csvs_directory = csv_directory.joinpath("Cohort")

    # Cohort: Global dosimetry dataframe
    cohort_global_dosim_path = cohort_csvs_directory.joinpath("Cohort: Global dosimetry.csv")  # Ensure the directory is a Path object
    cohort_global_dosim_df = load_files.load_csv_as_dataframe(cohort_global_dosim_path)