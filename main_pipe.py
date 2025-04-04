import pandas as pd 
import load_files
from pathlib import Path
import os 
import statistical_tests_1_quick_and_dirty
import shape_and_radiomic_features
import misc_funcs
import biopsy_information
import uncertainties_analysis



def main():
    
    # Main output (files, input) directory
    # This one is 10k 10k containment and dosim, 11 patients, 2 fractions each,  pt 181 MR as well (ran with errors in final figures)
    #main_output_path = Path("/home/matthew-muscat/Documents/UBC/Research/Data/Output data/MC_sim_out- Date-Apr-01-2025 Time-15,04,17")  # Ensure the directory is a Path object
    # This one is 10k containment and 10 (very low) dosim for speed, 11 patients, 2 fractions each,  pt 181 MR as well (ran with no errors in final figures)
    #main_output_path = Path("/home/matthew-muscat/Documents/UBC/Research/Data/Output data/MC_sim_out- Date-Apr-02-2025 Time-03,44,41")
    # This one is 10k containment and 10 (very low) dosim for speed, all vitesse patients! 
    main_output_path = Path("/home/matthew-muscat/Documents/UBC/Research/Data/Output data/MC_sim_out- Date-Apr-02-2025 Time-19,38,15")

    



    ### Load Dataframes 

    # Set csv directory
    csv_directory = main_output_path.joinpath("Output CSVs")
    cohort_csvs_directory = csv_directory.joinpath("Cohort")






    # Cohort 3d radiomic features all oar and dil structures
    cohort_3d_radiomic_features_all_oar_dil_path = cohort_csvs_directory.joinpath("Cohort: 3D radiomic features all OAR and DIL structures.csv")  # Ensure the directory is a Path object
    cohort_3d_radiomic_features_all_oar_dil_df = load_files.load_csv_as_dataframe(cohort_3d_radiomic_features_all_oar_dil_path)  # Load the CSV file into a DataFrame
    """ NOTE: The columns of the dataframe are:
    cohort_3d_radiomic_features_all_oar_dil_df.columns =
    Index(['Patient ID', 'Structure ID', 'Structure type', 'Structure refnum',
       'Volume', 'Surface area', 'Surface area to volume ratio', 'Sphericity',
       'Compactness 1', 'Compactness 2', 'Spherical disproportion',
       'Maximum 3D diameter', 'PCA major', 'PCA minor', 'PCA least',
       'PCA eigenvector major', 'PCA eigenvector minor',
       'PCA eigenvector least', 'Major axis (equivalent ellipse)',
       'Minor axis (equivalent ellipse)', 'Least axis (equivalent ellipse)',
       'Elongation', 'Flatness', 'L/R dimension at centroid',
       'A/P dimension at centroid', 'S/I dimension at centroid',
       'S/I arclength', 'DIL centroid (X, prostate frame)',
       'DIL centroid (Y, prostate frame)', 'DIL centroid (Z, prostate frame)',
       'DIL centroid distance (prostate frame)', 'DIL prostate sextant (LR)',
       'DIL prostate sextant (AP)', 'DIL prostate sextant (SI)'],
      dtype='object')
    """
    
    
    
    # biopsy basic spatial features
    cohort_biopsy_basic_spatial_features_path = cohort_csvs_directory.joinpath("Cohort: Biopsy basic spatial features dataframe.csv")  # Ensure the directory is a Path object
    cohort_biopsy_basic_spatial_features_df = load_files.load_csv_as_dataframe(cohort_biopsy_basic_spatial_features_path)  # Load the CSV file into a DataFrame
    """ NOTE: The columns of the dataframe are:
    cohort_biopsy_basic_spatial_features_df.columns =
    Index(['Patient ID', 'Bx ID', 'Simulated bool', 'Simulated type',
       'Struct type', 'Bx refnum', 'Bx index', 'Length (mm)', 'Volume (mm3)',
       'Voxel side length (mm)', 'Relative DIL ID', 'Relative DIL index',
       'BX to DIL centroid (X)', 'BX to DIL centroid (Y)',
       'BX to DIL centroid (Z)', 'BX to DIL centroid distance',
       'NN surface-surface distance', 'Relative prostate ID',
       'Relative prostate index', 'Bx position in prostate LR',
       'Bx position in prostate AP', 'Bx position in prostate SI'],
      dtype='object')
      """


    # Cohort: Global sum-to-one mc results
    cohort_global_sum_to_one_tissue_path = cohort_csvs_directory.joinpath("Cohort: global sum-to-one mc results.csv")  # Ensure the directory is a Path object
    cohort_global_sum_to_one_tissue_df = load_files.load_csv_as_dataframe(cohort_global_sum_to_one_tissue_path)

    # Cohort sum-to-one mc results
    cohort_sum_to_one_mc_results_path = cohort_csvs_directory.joinpath("Cohort: sum-to-one mc results.csv")  # Ensure the directory is a Path object
    cohort_sum_to_one_mc_results_df = load_files.load_csv_as_dataframe(cohort_sum_to_one_mc_results_path)  # Load the CSV file into a DataFrame

    # Cohort tissue class - distances global
    cohort_tissue_class_distances_global_path = cohort_csvs_directory.joinpath("Cohort: Tissue class - distances global results.csv")  # Ensure the directory is a Path object
    # this is a multiindex dataframe
    cohort_tissue_class_distances_global_df = load_files.load_multiindex_csv(cohort_tissue_class_distances_global_path, header_rows=[0, 1])  # Load the CSV file into a DataFrame




    # Load uncertainties csv
    #uncertainties_path = main_output_path.joinpath("uncertainties_file_auto_generated Date-Apr-02-2025 Time-03,45,24.csv")  # Ensure the directory is a Path object

    # Assuming main_output_path is already a Path object
    # Adjust the pattern as needed if the prefix should be "uncertainities"
    csv_files = list(main_output_path.glob("uncertainties*.csv"))
    if csv_files:
        # grab the first one 
        uncertainties_path = csv_files[0]
        uncertainties_df = load_files.load_csv_as_dataframe(uncertainties_path)
    else:
        raise FileNotFoundError("No uncertainties CSV file found in the directory.")

    




    # load all containment and distances results csvs
    mc_sim_results_path = csv_directory.joinpath("MC simulation")  # Ensure the directory is a Path object
    all_paths_containment_and_distances = load_files.find_csv_files(mc_sim_results_path, ['containment and distances (light) results.parquet'])
    # Load and concatenate all containment and distances results csvs
    # Loop through all the paths and load the csv files
    all_containment_and_distances_dfs_list = []
    for path in all_paths_containment_and_distances:
        # Load the csv file into a dataframe
        df = load_files.load_parquet_as_dataframe(path)
        # Append the dataframe to the list
        all_containment_and_distances_dfs_list.append(df)
    # Concatenate all the dataframes into one dataframe
    all_containment_and_distances_df = pd.concat(all_containment_and_distances_dfs_list, ignore_index=True)
    del all_containment_and_distances_dfs_list
    # Print the shape of the dataframe
    print(f"Shape of all containment and distances dataframe: {all_containment_and_distances_df.shape}")
    # Print the columns of the dataframe
    print(f"Columns of all containment and distances dataframe: {all_containment_and_distances_df.columns}")
    # Print the first 5 rows of the dataframe
    print(f"First 5 rows of all containment and distances dataframe: {all_containment_and_distances_df.head()}")
    # Print the last 5 rows of the dataframe
    print(f"Last 5 rows of all containment and distances dataframe: {all_containment_and_distances_df.tail()}")












    ########### LOADING COMPLETE









    ## Create output directory
    # Output directory 
    output_dir = Path(__file__).parents[0].joinpath("output_data")
    os.makedirs(output_dir, exist_ok=True)


    ### Get unqiue patient IDs
    # Get ALL unique patient IDs from the cohort_3d_radiomic_features_all_oar_dil_df DataFrame
    unique_patient_ids_all = cohort_biopsy_basic_spatial_features_df['Patient ID'].unique().tolist()
    # Print the unique patient IDs
    print("Unique Patient IDs (ALL):")
    print(unique_patient_ids_all)
    # Print the number of unique patient IDs
    print(f"Number of unique patient IDs ALL: {len(unique_patient_ids_all)}")


    # Get unique patient IDs, however the patient IDs actually include the patient ID (F#) where F# indicates the fraction but its actually the same patient, so I want to take only F1, if F1 isnt present for a particular ID then I want to take F2
    # Get the unique patient IDs from the cohort_3d_radiomic_features_all_oar_dil_df DataFrame
    unique_patient_ids_f1_prioritized = misc_funcs.get_unique_patient_ids_fraction_prioritize(cohort_biopsy_basic_spatial_features_df,patient_id_col='Patient ID', priority_fraction='F1')
    # Print the unique patient IDs
    print("Unique Patient IDs (F1) prioritized:")
    print(unique_patient_ids_f1_prioritized)
    # Print the number of unique patient IDs
    print(f"Number of unique patient IDs (F1) prioritized: {len(unique_patient_ids_f1_prioritized)}")

    ### Get unique patient IDs for F1
    # Get the unique patient IDs from the cohort_3d_radiomic_features_all_oar_dil_df DataFrame
    unique_patient_ids_f1 = misc_funcs.get_unique_patient_ids_fraction_specific(cohort_biopsy_basic_spatial_features_df, patient_id_col='Patient ID',fraction='F1')
    # Print the unique patient IDs
    print("Unique Patient IDs (F1) ONLY:")
    print(unique_patient_ids_f1)
    # Print the number of unique patient IDs
    print(f"Number of unique patient IDs F1 ONLY: {len(unique_patient_ids_f1)}")

    ### Get unique patient IDs for F2
    # Get the unique patient IDs from the cohort_3d_radiomic_features_all_oar_dil_df DataFrame
    unique_patient_ids_f2 = misc_funcs.get_unique_patient_ids_fraction_specific(cohort_biopsy_basic_spatial_features_df, patient_id_col='Patient ID',fraction='F2')
    # Print the unique patient IDs
    print("Unique Patient IDs (F2) only:")
    print(unique_patient_ids_f2)
    # Print the number of unique patient IDs
    print(f"Number of unique patient IDs F2 ONLY: {len(unique_patient_ids_f2)}")








    ### Uncertainties analysis (START)
    # Create output directory for uncertainties analysis
    uncertainties_analysis_dir = output_dir.joinpath("uncertainties_analysis")
    os.makedirs(uncertainties_analysis_dir, exist_ok=True)
    # Output filename
    output_filename = 'uncertainties_analysis_statistics_all_patients.csv'
    # Get uncertainties analysis statistics
    uncertainties_analysis_statistics_df = uncertainties_analysis.compute_statistics_by_structure_type(uncertainties_df,
                                                                                           columns=['mu (X)', 'mu (Y)', 'mu (Z)', 'sigma (X)', 'sigma (Y)', 'sigma (Z)', 'Dilations mu (XY)', 'Dilations mu (Z)', 'Dilations sigma (XY)', 'Dilations sigma (Z)', 'Rotations mu (X)', 'Rotations mu (Y)', 'Rotations mu (Z)', 'Rotations sigma (X)', 'Rotations sigma (Y)', 'Rotations sigma (Z)'], 
                                                                                           patient_uids=unique_patient_ids_all)
    # Save the statistics to a CSV file
    uncertainties_analysis_statistics_df.to_csv(uncertainties_analysis_dir.joinpath(output_filename), index=True)
    # Print the statistics
    print(uncertainties_analysis_statistics_df)
    ### Uncertainties analysis (END)









    ### Radiomic features analysis (START)
    # Create output directory for radiomic features
    radiomic_features_dir = output_dir.joinpath("radiomic_features")
    os.makedirs(radiomic_features_dir, exist_ok=True)
    # Output filename
    output_filename = 'radiomic_features_statistics_all_patients.csv'
    # Get radiomic statistics
    radiomic_statistics_df = shape_and_radiomic_features.get_radiomic_statistics(cohort_3d_radiomic_features_all_oar_dil_df, 
                                                                                 patient_id= unique_patient_ids_f1_prioritized, 
                                                                                 exclude_columns=['Patient ID', 'Structure ID', 'Structure type', 'Structure refnum','PCA eigenvector major', 'PCA eigenvector minor',	'PCA eigenvector least', 'DIL centroid (X, prostate frame)', 'DIL centroid (Y, prostate frame)', 'DIL centroid (Z, prostate frame)', 'DIL centroid distance (prostate frame)', 'DIL prostate sextant (LR)', 'DIL prostate sextant (AP)', 'DIL prostate sextant (SI)'])

    # Save the statistics to a CSV file
    radiomic_statistics_df.to_csv(radiomic_features_dir.joinpath(output_filename), index=True)
    # Print the statistics
    print(radiomic_statistics_df)
    ### Radiomic features analysis (END)















    ### Find DIL double sextant percentages (START)
    # Create output directory for DIL information
    dil_information_dir = output_dir.joinpath("dil_information")
    os.makedirs(dil_information_dir, exist_ok=True)
    # Output filename
    output_filename = 'dil_double_sextant_percentages_all_patients.csv'
    # Get DIL double sextant percentages
    dil_double_sextant_percentages_df = shape_and_radiomic_features.find_dil_double_sextant_percentages(cohort_3d_radiomic_features_all_oar_dil_df, patient_id=unique_patient_ids_f1_prioritized)
    # Save the statistics to a CSV file
    dil_double_sextant_percentages_df.to_csv(dil_information_dir.joinpath(output_filename), index=True)
    # Print the statistics
    print(dil_double_sextant_percentages_df)
    ### Find DIL double sextant percentages (END)















    ### Find structure counts (START)
    # Create output directory for DIL information
    radiomic_features_dir = output_dir.joinpath("radiomic_features")
    os.makedirs(radiomic_features_dir, exist_ok=True)
    # Output filename
    output_filename = 'structure_counts_all_patients.csv'
    # Get structure counts
    structure_counts_df, structure_counts_statistics_df = shape_and_radiomic_features.calculate_structure_counts_and_stats(cohort_3d_radiomic_features_all_oar_dil_df, patient_id=unique_patient_ids_f1_prioritized, structure_types=None)
    # Save the statistics to a CSV file
    structure_counts_df.to_csv(radiomic_features_dir.joinpath(output_filename), index=True)
    # Print the statistics
    print(structure_counts_df)
    # Save the statistics to a CSV file
    output_filename = 'structure_counts_statistics_all_patients.csv'
    # Save the statistics to a CSV file
    structure_counts_statistics_df.to_csv(radiomic_features_dir.joinpath(output_filename), index=True)
    # Print the statistics
    print(structure_counts_statistics_df)
    ### Find structure counts (END)












    ### Biopsy information analysis (START)
    # Create output directory for biopsy information
    biopsy_information_dir = output_dir.joinpath("biopsy_information")
    os.makedirs(biopsy_information_dir, exist_ok=True)
    # Output filename
    output_filename = 'biopsy_information_statistics_all_patients.csv'
    # Get biopsy information statistics
    biopsy_information_statistics_df = biopsy_information.get_filtered_statistics(cohort_biopsy_basic_spatial_features_df, 
                                                                                 columns=['Length (mm)', 
                                                                                          'Volume (mm3)', 
                                                                                          'Voxel side length (mm)',  
                                                                                          'BX to DIL centroid (X)', 
                                                                                          'BX to DIL centroid (Y)',
                                                                                          'BX to DIL centroid (Z)', 
                                                                                          'BX to DIL centroid distance', 
                                                                                          'NN surface-surface distance'], 
                                                                                 patient_id=unique_patient_ids_all,
                                                                                 simulated_type='Real')

    # Save the statistics to a CSV file
    biopsy_information_statistics_df.to_csv(biopsy_information_dir.joinpath(output_filename), index=True)
    # Print the statistics
    print(biopsy_information_statistics_df)
    ### Biopsy information analysis (END)

















    ### Find biopsy double sextant percentages (START)
    # Create output directory for biopsy information
    biopsy_information_dir = output_dir.joinpath("biopsy_information")
    os.makedirs(biopsy_information_dir, exist_ok=True)
    # Output filename
    output_filename = 'biopsy_double_sextant_percentages_all_patients.csv'
    # Get biopsy double sextant percentages
    biopsy_double_sextant_percentages_df = biopsy_information.find_biopsy_double_sextant_percentages(cohort_biopsy_basic_spatial_features_df, 
                                                                                                     patient_id=unique_patient_ids_all,
                                                                                                     simulated_type='Real')
    # Save the statistics to a CSV file
    biopsy_double_sextant_percentages_df.to_csv(biopsy_information_dir.joinpath(output_filename), index=True)
    # Print the statistics
    print(biopsy_double_sextant_percentages_df)
    ### Find biopsy double sextant percentages (END)







    ### Find distances statistics (START)










    statistical_tests_1_dir = output_dir.joinpath("statistical_tests_0")
    os.makedirs(statistical_tests_1_dir, exist_ok=True)

    output_filename = 'stats_test_1.csv'
    tissue_types = ["DIL", 'Prostatic', 'Periprostatic', 'Urethral', 'Rectal']
    _ = statistical_tests_1_quick_and_dirty.analyze_data(cohort_global_sum_to_one_tissue_df, tissue_types, statistical_tests_1_dir, output_filename)

    

if __name__ == "__main__":
    main()