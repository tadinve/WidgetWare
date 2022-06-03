import datetime

import pandas as pd

import great_expectations as ge
import great_expectations.jupyter_ux
from great_expectations.core.batch import BatchRequest
from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler
from great_expectations.checkpoint import SimpleCheckpoint
from great_expectations.exceptions import DataContextError


class GE_Suites:
    
    def create_suite_files(datasource_name, data_asset_name):
        context = ge.data_context.DataContext()

        expectation_suite_name = '{}.warning'.format(data_asset_name)
        
        context.create_expectation_suite(
            expectation_suite_name, overwrite_existing=True 
        )
        batch_request = {'datasource_name': datasource_name, 
                         'data_connector_name': 'default_inferred_data_connector_name', 
                         'data_asset_name': data_asset_name, 'limit': 1000}

        #expectation_suite_name = "raw_customers.csv.warning"

        validator = context.get_validator(
            batch_request=BatchRequest(**batch_request),
            expectation_suite_name=expectation_suite_name
        )
        column_names = [f'"{column_name}"' for column_name in validator.columns()]
        print(f"Columns: {', '.join(column_names)}.")
        validator.head(n_rows=5, fetch_all=False)

        ignored_columns = []
        profiler = UserConfigurableProfiler(
            profile_dataset=validator,
            excluded_expectations=None,
            ignored_columns=ignored_columns,
            not_null_only=False,
            primary_or_compound_key=False,
            semantic_types_dict=None,
            table_expectations_only=False,
            value_set_threshold="MANY",
        )
        profiler.build_suite()
        
        # print(validator.get_expectation_suite(discard_failed_expectations=False))
        validator.save_expectation_suite(discard_failed_expectations=False)

# suite_dict = {
#     'pandas_datasource': ['raw_customers.csv', 'raw_orders.csv', 'raw_payments.csv'],
#     'postgres_datasource': ['dbt.customers', 'dbt.orders', 'dbt.raw_customers', 
#                             'dbt.raw_orders', 'dbt.raw_payments', 'dbt.stg_customers', 
#                             'dbt.stg_orders', 'dbt.stg_payments']
# }
# sources_dict = {}
# for datasource_name in ge.get_context().list_datasources():
#     data_asset_names_dict = ge.get_context().get_available_data_asset_names(datasource_name['name'])
#     sources_dict[datasource_name['name']] = data_asset_names_dict[datasource_name['name']]['default_inferred_data_connector_name']    
    
# for data_source in sources_dict:
#     for data_asset in sources_dict[data_source]:
#         GE_Suites.create_suite_files(datasource_name=data_source, data_asset_name=data_asset)
