import great_expectations as ge
from great_expectations.cli.datasource import sanitize_yaml_and_save_datasource



ds_pandas_yaml = f"""
name: {{data_source}}
class_name: Datasource
execution_engine:
  class_name: PandasExecutionEngine
data_connectors:
  default_inferred_data_connector_name:
    class_name: InferredAssetFilesystemDataConnector
    base_directory: {{data_dir}}
    default_regex:
      group_names:
        - data_asset_name
      pattern: (.*)
  default_runtime_data_connector_name:
    class_name: RuntimeDataConnector
    batch_identifiers:
      - default_identifier_name
"""

# connection_string: postgresql+psycopg2://{{username}}:{{password}}@{{host}}:{{port}}/{{database}}  
postgres_yaml = f"""
name: {{datasource}}
class_name: Datasource
execution_engine:
  class_name: SqlAlchemyExecutionEngine
  credentials:
    host: {{host}}
    port: '{{port}}'
    username: {{username}}
    password: {{password}}
    database: {{database}}
    schema_name: {{schema_name}}
    drivername: postgresql
data_connectors:
  default_runtime_data_connector_name:
    class_name: RuntimeDataConnector
    batch_identifiers:
      - default_identifier_name
  default_inferred_data_connector_name:
    class_name: InferredAssetSqlDataConnector
    include_schema_name: True"""

class GE_Data_Sources:
    
    @staticmethod
    def create_file_data_source(datasource= "pandas_datasource"):
        
        context = ge.get_context()

        datasource_name = datasource
        context.test_yaml_config(yaml_config=ds_pandas_yaml.format(datasource_name))

        sanitize_yaml_and_save_datasource(context, ds_pandas_yaml.format(datasource_name), overwrite_existing=True)
        res = context.list_datasources()
        print(res)
    
    @staticmethod
    def create_postgres_data_source(datasource= "postgres_datasource", args_json={}):
        
        context = ge.get_context()

        datasource_name = datasource
        
        yaml_config = postgres_yaml.format(datasource=datasource_name, host=args_json['host'], port=args_json['port'], \
            username=args_json['username'], password=args_json['password'], database=args_json['database'], schema_name=args_json['schema_name'])
        
        
        # context.test_yaml_config(yaml_config=postgres_yaml.format(datasource=datasource_name, host=args_json['host'], port=args_json['port'], 
        #                                                           username=args_json['username'], password=args_json['password'], 
        #                                                           database=args_json['database'], schema_name=args_json['schema_name']))

        sanitize_yaml_and_save_datasource(context, yaml_config, overwrite_existing=True)
        res = context.list_datasources()
        print(res)
    
    @staticmethod
    def create_data_source(datasource= "postgres_datasource", data_dir=None, args_json={}):
        
        context = ge.get_context()

        datasource_name = datasource
        
        if args_json:
          yaml_config = postgres_yaml.format(datasource=datasource_name, host=args_json['host'], port=args_json['port'], \
              username=args_json['username'], password=args_json['password'], database=args_json['database'], schema_name=args_json['schema_name'])
        else:
          yaml_config = ds_pandas_yaml.format(data_source=datasource_name, data_dir=data_dir)  
                        
        sanitize_yaml_and_save_datasource(context, yaml_config, overwrite_existing=True)
        res = context.list_datasources()
        print(res)


# args_json = {
#     'host': 'postgres-dbt',
#     'port': 5432,
#     'username': 'dbtuser',
#     'password': 'pssd',
#     'database': 'dbtdb', 
#     'schema_name': 'dbt'
# }
# GE_Data_Sources.create_postgres_data_source(args_json=args_json)
