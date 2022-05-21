from ctm_python_client.core.bmc_control_m import CmJobFlow
from ctm_python_client.jobs.dummy import DummyJob
from ctm_python_client.jobs.command import CommandJob
from ctm_python_client.jobs.embedded_script import EmbeddedScriptJob
import sys 
sys.path.insert(0,"..")
from scripts.get_airflow_tasks import GetAirflowTasks
from ctm_python_client.session.session import Session

ctm_uri =  "https://3.140.33.249:8443/automation-api"
ctm_user =  "emuser"
ctm_pwd =  "empass"
hostname = "ip-172-31-40-130.us-east-2.compute.internal"
run_as = "controlm"

class SendDAGtoControlM: 
    
    @staticmethod
    def create_ctm_dag(dag_id):
        session = Session(endpoint=ctm_uri, username=ctm_user, password=ctm_pwd)
        # ctm_executor_bash_demo1
        t1_flow = CmJobFlow(application="CTM_Executor_Demo", sub_application = "ctm_executor_demo200", session=session)

        t1_flow.set_run_as(username="airflow",host="airflow")

        # Create Folder
        f1 = t1_flow.create_folder(name=dag_id)

        ctm_tasks = {}
        #(task_list, taskop_dict)
        dag_dict = GetAirflowTasks().process_tasks_response(dag_id)
        
        bash_cmd_dict = GetAirflowTasks().get_bash_commands(dag_id)
        
        # if task_cmd_dict:
        #     # op_type = {'1': None, '2': None}  -- print(all(op_type.values())) - Return False 
        #     # op_type = {'1': None, '2': 5}  -- print(all(op_type.values())) - Return True 
        #     if all(task_cmd_dict.values()):
        #         task_type = 'bash'
        #     else:
        #         task_type = 'dummy'
        # else:
        #     task_type = 'airflow'
        
        for task in dag_dict['tasks']:
            op_type = task['class_ref']['class_name']
            print(op_type)
            if op_type == 'DummyOperator':
                j1 = DummyJob(f1, task['task_id'])
            # elif op_type == 'BashOperator':
            #     print(bash_cmd_dict[task['task_id']])
            #     j1 = CommandJob(folder=f1, job_name=task['task_id'], command=bash_cmd_dict[task['task_id']], 
            #                     host=hostname, run_as=run_as)
            else:
                activate_env = 'source ~/airflowEnv/bin/activate\\n'
                deactivate_env = '\\ndeactivate'
                task_script = '{}airflow tasks test {} {} 2022-01-01{}'.format(activate_env, dag_id, task['task_id'], deactivate_env)
                j1 = EmbeddedScriptJob(folder=f1, job_name=task['task_id'], script=task_script, file_name = task['task_id'],
                                host=hostname, run_as=run_as)
                
            ctm_tasks[task['task_id']] = t1_flow.add_job( f1, j1)


        for task in dag_dict['tasks']:
            if len(task['downstream_task_ids']) > 0:
                for ds_task in task['downstream_task_ids']:
                    t1_flow.chain_jobs(f1,[ctm_tasks[task['task_id']],ctm_tasks[ds_task] ])
                
        # for task in task_list:
        #     task_op = taskop_dict[task]
            
        #     if task_op == 'DummyOperator':
        #         j1 = DummyJob(f1, task)
        #     # elif task_op == 'BashOperator':
        #     #     j1 = CommandJob(folder=f1, job_name=task, command=task_cmd_dict[task],
        #     #                   host=hostname, run_as=run_as)
        #     else:
        #         activate_env = 'source ~/airflowEnv/bin/activate\\n'
        #         deactivate_env = '\\ndeactivate'
        #         task_script = '{}airflow tasks test {} {} 2022-01-01{}'.format(activate_env, dag_id, task, deactivate_env)
        #         j1 = EmbeddedScriptJob(folder=f1, job_name=task, script=task_script, file_name = task,
        #                         host=hostname, run_as=run_as)
                
        #     ctm_tasks.append(t1_flow.add_job( f1, j1))
        
        # t1_flow.chain_jobs(f1, ctm_tasks)

        print(t1_flow.display_json())
        
        # from ctm_python_client.utils.displayDAG import DisplayDAG

        # DisplayDAG(t1_flow).display_graphviz()
        
        # #dot.render(directory='doctest-output').replace('\\', '/')
        
        deploy_result = t1_flow.deploy()
        print(deploy_result)
        
#SendDAGtoControlM.create_ctm_dag('ctm_weather_forecast')