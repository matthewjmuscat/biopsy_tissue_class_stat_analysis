import pandas as pd
import scipy.stats as stats
import pingouin as pg
import os

def analyze_data(df, tissue_types, output_dir, output_filename):
    results = []

    for tissue in tissue_types:
        # Filter DataFrame for each tissue type
        filtered_df = df[(df['Simulated type'] == 'Real') & (df['Tissue class'] == tissue)]

        if len(filtered_df) > 1:
            # Perform Wilcoxon Signed-Rank Test on differences
            stat, p_value = stats.wilcoxon(filtered_df['Global Mean BE'], filtered_df['Global Mean BE optimal'])
            
            # Calculate Cohen's d for paired samples using pingouin
            cohen_d = pg.compute_effsize(filtered_df['Global Mean BE'], filtered_df['Global Mean BE optimal'], eftype='cohen', paired=True)
            
            # Calculate Common Language Effect Size using pingouin
            cles = pg.compute_effsize(filtered_df['Global Mean BE'], filtered_df['Global Mean BE optimal'], eftype='cles', paired=True)
            
            # Calculate mean difference
            mean_diff = filtered_df['Global Mean BE'].mean() - filtered_df['Global Mean BE optimal'].mean()

            results.append({
                'Tissue Type': tissue,
                'Wilcoxon Test Statistic': stat,
                'Wilcoxon P-Value': p_value,
                'Mean Difference': mean_diff,
                'Cohen\'s d': cohen_d,
                'Common Language Effect Size': cles
            })
        else:
            results.append({
                'Tissue Type': tissue,
                'Wilcoxon Test Statistic': 'N/A',
                'Wilcoxon P-Value': 'N/A',
                'Mean Difference': 'N/A',
                'Cohen\'s d': 'N/A',
                'Common Language Effect Size': 'N/A'
            })

    results_df = pd.DataFrame(results)
    full_path = os.path.join(output_dir, output_filename)
    results_df.to_csv(full_path, index=False)

    return results_df

# Example usage:
# Assuming df is your DataFrame loaded from a CSV or any other file.
# tissue_types = ['DIL', 'Periprostatic', 'Pros
