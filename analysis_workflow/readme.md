Data Aggregation Overview

Required Libraries:
- ploomber
- pandas
- matplotlib
- numpy
- scipy
- seaborn
- scikit-learn

Parameters:
- var (str): The type of variable to aggregate (options: pm_2.5, pm_10.0, atm_preassure, temperature, humidity).
- year (int): The year from which the data was collected.
- period (str): The date range for aggregation (e.g., 1h, 1D, 1W, 1ME).
- agg_type (str): The type of aggregation that is going to be made (min, mean, max).
- start_date (str): The start date in the format 'MM/DD/YYYY'.
- end_date (str): The end date in the format 'MM/DD/YYYY'.
- dist_matrix_type (str): The type of distance matrix wanted, by default it uses Euclidean (euclidean, cosine, cityblock).
- method (str): The type of clustering algorithm to be used, by default it uses Ward (ward, single, complete, average, centroid, median, weighted).
- clusters (str or int): Defines how to determine the number of clusters, by default it uses Silhouette (elbow, silhouette, or an integer in the range 1 to 20).

Running the Aggregation in the Terminal:
- Use the command 'ploomber build' to run the aggregation process with the default parameters specified in env.yaml.
- To override the default values, provide custom parameters using the ploomber build command with the appropriate flags.

Example:
1. Aggregating data for PM 2.5 for the year 2023 with a monthly period. Additionally specifying to calculate distance matrix with Cosine distance, to determine the number of clusters by silhouette and to use ward type of clustering algorithm:
> ploomber build --env--var 'pm_2.5' --env--year 2023 --env--period '1ME' --env--agg_type 'mean' --env--dist_matrix_type 'cosine' --env--clusters 'silhouette' --env--method 'ward' 

2. Aggregating data for PM 2.5 for a specific range period with a weekly period: Additionally specifying to calculate distance matrix with Euclidean distance, to determine the number of clusters by elbow and to use single type of clustering algorithm:
> ploomber build --env--var 'pm_2.5' --env--start_date '1/1/2023' --env--end_date '4/1/2023' --env--period '1ME' --env--agg_type 'mean' --env--dist_matrix_type 'euclidean' --env--clusters 'elbow' --env--method 'ward' 