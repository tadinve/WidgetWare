from os import stat
from ruamel.yaml import YAML
import great_expectations as ge
from pprint import pprint
from airflow.utils.log.logging_mixin import LoggingMixin

checkpoint_yaml_config = f"""
name: {{cp_name}}
config_version: 1.0
class_name: SimpleCheckpoint
run_name_template: "%Y%m%d-%H%M%S-my-run-name-template"
validations:
"""

validation_yaml_config = f"""
  - batch_request:
      datasource_name: {{ds_name}}
      data_connector_name: default_inferred_data_connector_name
      data_asset_name: {{da_name}}
      data_connector_query:
        index: -1
    expectation_suite_name: {{expectation_suite}}
"""

class GE_Checkpoints:
    
    @staticmethod
    def create_check_points(check_point_configs):
        yaml = YAML()
        context = ge.get_context()
        LoggingMixin().log.info('check_point_configs :: {}'.format(check_point_configs))
        for check_point_name in check_point_configs:
            data_source_dict = check_point_configs[check_point_name]
            valid_yaml = """"""
            for data_source in data_source_dict:
                for data_asset in data_source_dict[data_source]:
                    expectation_suite = '{}.warning'.format(data_asset)
                    valid_yaml = valid_yaml + validation_yaml_config.format(ds_name=data_source, da_name=data_asset, 
                                                                 expectation_suite=expectation_suite)
            yaml_config = checkpoint_yaml_config.format(cp_name=check_point_name) + valid_yaml
            context.add_checkpoint(**yaml.load(yaml_config))
            LoggingMixin().log.info('Done creating check_point file :: {}'.format(check_point_name))
            

    @staticmethod
    def create_check_point_config(sources_dict):
        check_point_configs = {}
        for data_source in sources_dict:
            rem_name = ''
            #exp_suite_list = []
            for data_asset in sources_dict[data_source]:
                if 'dbt' in data_asset:
                    if 'raw' in data_asset:
                        rem_name = 'raw_tables'
                    elif 'stg' in data_asset: 
                        rem_name = 'stg_tables'
                    else:
                        rem_name = 'transform_tables'
                else:
                    rem_name = 'csv_files'
                checkpoint_name = 'check_{}'.format(rem_name)
                #expectation_suite = '{}.warning'.format(data_asset)
                #exp_suite_list.append({data_asset: expectation_suite})
                if checkpoint_name in check_point_configs:
                    if data_source in check_point_configs[checkpoint_name]:
                        check_point_configs[checkpoint_name][data_source].append(data_asset)
                    # else:
                    #     check_point_configs[checkpoint_name][data_source] = [data_asset]
                else:
                    check_point_configs[checkpoint_name] = {data_source: [data_asset]}
        return check_point_configs
