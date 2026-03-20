@REM ploomber build --env--var 'pm_2.5' --env--year 2023 --env--period '1ME' --env--agg_type 'mean' --env--dist_matrix_type 'cosine' --env--clusters 'silhouette' --env--method 'ward'

ploomber build --env--var 'pm_2.5' --env--period 'D' --env--agg_type 'mean' --env--dist_matrix_type 'cosine' --env--clusters 'silhouette' --env--method 'ward' -e pipeline1.yaml
