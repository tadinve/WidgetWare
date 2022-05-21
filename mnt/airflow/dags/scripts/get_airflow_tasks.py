import requests
from requests.auth import HTTPBasicAuth
from graphlib2 import TopologicalSorter        
import re
class GetAirflowTasks:
    
    session = None
    auth = None
    host_name = None
    
    def __init__(self):
        self.host_name = 'http://localhost:8080'
        self.auth = HTTPBasicAuth('airflow', 'airflow')
        
        

    def _get_tasks_for_dag(self, dag_id):
        """Get Tasks for a given Airflow DAG

        Args:
            dag_name (str): DAG ID

        Returns:
            string: JSON Object with tasks associated to the DAG
        """
        output = None
        try:
            res = requests.get(self.host_name + '/api/v1/dags/'+dag_id+'/tasks', auth = self.auth)
            output = res.json()
        except Exception as e:
            print("Exception while fetching _get_tasks_for_dag() %s", e)
        return output
    
    
    def process_tasks_response(self, dag):
        """Get the tasks order from the DAG

        Args:
            dag (str): DAG ID

        Returns:
            list: List of task id's in the sequential order from the dag
        """
        
        output = self._get_tasks_for_dag(dag_id=dag)
        # dt = {}
        # taskop_dict = {}
        # for obj in output['tasks']:
        #     taskop_dict[obj['task_id']] = obj['class_ref']['class_name']
        #     dt[obj['task_id']] = obj['downstream_task_ids']
        
        # ts = TopologicalSorter(dt)
        # final_dag_order = list(ts.static_order())
        # final_dag_order.reverse()
        # return (final_dag_order, taskop_dict)
        return output
    
    
    def _get_dag_path_info(self, dag_id):
        """Get DAG Basic Info

        Args:
            dag_name (str): DAG ID

        Returns:
            string: JSON Object with tasks associated to the DAG
        """
        output = None
        try:
            res = requests.get(self.host_name + '/api/v1/dags/'+dag_id+'', auth = self.auth)
            output = res.json()          
        except Exception as e:
            print("Exception while fetching _get_dag_path_info() %s", e)
        return output
            
    
    def _get_dag_source_code(self, file_token):
        """Get DAG Source Code

        Args:
            dag_name (str): DAG ID
            file_token (str): File Token

        Returns:
            string: JSON Object with tasks associated to the DAG
        """
        output = None
        try:
            res = requests.get(self.host_name + '/api/v1/dagSources/' +file_token, auth = self.auth)
            output = res.text            
        except Exception as e:
            print("Exception while fetching _get_dag_source_code() %s", e)
        return output   
    
    def get_bash_commands(self, dag_id):
        """Get Task and the corresponding task commands

        Args:
            dag_id (string): DAG ID
        """
        try:
            dag_info = self._get_dag_path_info(dag_id)
            file_token = dag_info['file_token']
            source_code = self._get_dag_source_code(file_token)
            # #print(source_code)
            # if 'BashOperator' in source_code:
            #     op_type = 'BashOperator'
            # elif 'DummyOperator' in source_code:
            #     op_type = 'DummyOperator'
            # else:
            #     op_type = None
            
            tasks_dict = {}
                
            match = re.findall(r'(?<=BashOperator\()[^\)]*', source_code, re.MULTILINE)
            #print(match)
            for x in match:
                task_id_x = re.findall(r'(?<=task_id\s\=\s")[^\",]*', x)
                #print(task_id_x)
                task_id_x = task_id_x[0]
                task_cmd_x = re.findall(r'(?<=\=")[^\"]*', x)
                task_cmd_x = task_cmd_x[0].strip()
                #print(task_cmd_x)
                tasks_dict[task_id_x] = task_cmd_x
                
            #print(tasks_dict)
        except Exception as e:
            print("Exception while fetching get_task_commands %s", e)
        return tasks_dict 
        

# Usage 
# dag_order = GetAirflowTasks().process_tasks_response(dag='forex_data_pipeline')
# print(dag_order)
#print(GetAirflowTasks().get_task_commands(dag_id='ctm_multi_etl'))