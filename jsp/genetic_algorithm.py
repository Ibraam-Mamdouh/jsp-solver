import random
import math
from typing import List, Tuple, Dict, Optional

from jsp.models import Operation, Job, JSPInstance
from jsp.schedule import ScheduledOperation, Schedule
from jsp.validation import is_valid

# def load_orlib_benchmark(filepath:str)->list[list[tuple[int,int]]]:
#     if not os.path.exists(filepath):
#         raise FileNotFoundError(f"File not found: {filepath}")
#     with open(filepath, 'r',encoding="utf-8") as f:
#          lines=[line.strip() for line in f if line.strip() and not line.strip().startswith(("#","+"))] 
#     header=lines[0].split()
#     num_jobs=int(header[0])
#     num_machines=int(header[1])

#     problem_data=[]

#     for line in lines[1:num_jobs+1]:
#         numbers=list(map(int,line.split()))
#         job_ops=[]
#         for i in range(0,len(numbers),2):
#             machine_id=numbers[i]
#             processing_time=numbers[i+1]
#             job_ops.append((machine_id,processing_time))
#         problem_data.append(job_ops)
#     return problem_data

class Chromosome:
    def __init__(self,genes:list[int],instance:JSPInstance):
        self.genes:List[int]=genes
        self.instance:JSPInstance=instance
        self.schedule:Optional[Schedule]=None
        self.makespan:int=0
        self.fitness:float=0.0

    def decode(self)->Schedule:
        n_jobs=self.instance.n_jobs
        n_machines=self.instance.n_machines
        job_available_time=[0]*n_jobs
        machine_available_time=[0]*n_machines
        job_op_step=[0]*n_jobs

        scheduled_ops: List[ScheduledOperation]=[]

        for job_id in self.genes:
            op_idx=job_op_step[job_id]
            operation:Operation=self.instance.get_operation(job_id,op_idx)

            mach=operation.machine
            dur=operation.duration

            start_time=max(job_available_time[job_id],machine_available_time[mach])
            end_time=start_time+dur
            scheduled_ops.append(
                ScheduledOperation(
                    job_id=job_id,
                    op_index=op_idx,
                    machine=mach,
                    start=start_time,
                    end=end_time
                )
            )  

            job_available_time[job_id]=end_time
            machine_available_time[mach]=end_time
            job_op_step[job_id]+=1

        self.schedule = Schedule(operations=scheduled_ops)
        return self.schedule        

    def evaluate(self) -> float:
        if self.schedule is None:
            self.decode()
        self.makespan = self.schedule.makespan
        self.fitness = 1000.0 / self.makespan
        return self.fitness

    def clone(self) -> "Chromosome":
            new_ind = Chromosome(genes=list(self.genes), instance=self.instance)
            new_ind.schedule = self.schedule
            new_ind.makespan = self.makespan
            new_ind.fitness = self.fitness
            return new_ind

def generate_random_chromosome(instance:JSPInstance)->Chromosome:
     genes=[]
     for job in instance.jobs:
         genes.extend([job.job_id]*job.n_operations)
     random.shuffle(genes)

     ind=Chromosome(genes=genes,instance=instance)
     ind.evaluate()
     return ind

def generate_spt_chromosome(instance:JSPInstance)->Chromosome:
     remaining_ops={job.job_id: list(job.operations) for job in instance.jobs}
     genes=[]
     while any(remaining_ops.values()):
        candidates=[(j_id,ops[0].duration) for j_id,ops in remaining_ops.items() if ops]
        best_job_id=min(candidates,key=lambda x:x[1])[0]
        genes.append(best_job_id)
        remaining_ops[best_job_id].pop(0)
     ind=Chromosome(genes=genes,instance=instance)
     ind.evaluate()
     return ind   

    
def create_initial_population(instance:JSPInstance,pop_size:int=50,include_spt:bool=True)->list[Chromosome]:
    population:list[Chromosome]=[]
    if include_spt:
        population.append(generate_spt_chromosome(instance))

    while len(population)<pop_size:
        population.append(generate_random_chromosome(instance))
    return population        
