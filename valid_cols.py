VALID_COLS = ['city', 'cluster 1 probability', 'num. neighborhoods', 'hpa_3yr_pred',
       'pop_est_25mile', 'pop_ch_25mile', 'mhv', 'md_retax',
       'pop_est_25mile_scaled', 'pop_ch_25mile_scaled', 'hpa_3yr_pred_scaled',
       'mhv_scaled', 'md_retax_scaled', 'state', 'region']

BETTER_COLS = ['city', 'cluster 1 probability', 'num. neighborhoods', 'predicted 3 year home price appreciation',
       '25 mi. population', '25 mi. population change', 'median home value', 'median real estate tax',
       'scaled 25 mi. population', 'scaled 25 mi. population change', 'scaled predicted 3 year home price appreciation',
       'scaled median home value', 'scaled median real estate tax', 'state', 'region']

COL_MAPPING = {new:old for old,new in zip(VALID_COLS, BETTER_COLS)}
