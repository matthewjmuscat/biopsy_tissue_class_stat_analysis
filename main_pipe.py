import pandas as pd 
import load_files
from pathlib import Path
import os 
import statistical_tests_1_quick_and_dirty

def main():
    
    # Main output (files, input) directory
    main_output_path = Path("/home/mjm/Documents/UBC/Research/biopsylocalization-new/Data/Output data/MC_sim_out- Date-Jan-14-2025 Time-14,25,24")  # Ensure the directory is a Path object
    


    ### Load Dataframes 

    # Set csv directory
    csv_directory = main_output_path.joinpath("Output CSVs")
    cohort_csvs_directory = csv_directory.joinpath("Cohort")

    # Cohort: Global dosimetry dataframe
    cohort_global_sum_to_one_tissue_path = cohort_csvs_directory.joinpath("Cohort: global sum-to-one mc results_custom.csv")  # Ensure the directory is a Path object
    cohort_global_sum_to_one_tissue_df = load_files.load_csv_as_dataframe(cohort_global_sum_to_one_tissue_path)




    ## Create output directory
    # Output directory 
    output_dir = Path(__file__).parents[0].joinpath("output_data")
    os.makedirs(output_dir, exist_ok=True)

    statistical_tests_1_dir = output_dir.joinpath("statistical_tests_0")
    os.makedirs(statistical_tests_1_dir, exist_ok=True)

    output_filename = 'stats_test_1.csv'
    tissue_types = ["DIL", 'Prostatic', 'Periprostatic', 'Urethral', 'Rectal']
    _ = statistical_tests_1_quick_and_dirty.analyze_data(cohort_global_sum_to_one_tissue_df, tissue_types, statistical_tests_1_dir, output_filename)

    

if __name__ == "__main__":
    main()