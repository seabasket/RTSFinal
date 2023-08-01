import pandas as pd
import numpy as np


class Task:
  def __init__(self, task_id, Ci, Ti):
    self.task_id = task_id
    self.Ci = Ci
    self.Ti = Ti
    self.last_executed = None
    self.remaining_time = Ci
    self.available = True

  def __str__(self):
    return str(f"Task {self.task_id}: Ci={self.Ci}, Ti={self.Ti}, last_executed = {self.last_executed}, remaining_time = {self.remaining_time}, available = {self.available}")


def read_tasks_from_csv(file_path):
  df = pd.read_csv(file_path)
  tasks = []
  for index, row in df.iterrows():
    tasks.append(Task(index + 1, row['Ci'], row['Ti']))
  return tasks  

def cyclic_schedule(tasks):
  Ti_list = []
  #create local copy of tasks
  l_tasks = tasks.copy()

  #create list of periods
  for task in l_tasks:
      Ti_list.append(task.Ti)

  min_cyc = np.gcd.reduce(Ti_list) # minor cycle
  maj_cyc = np.lcm.reduce(Ti_list) # major cycle

  # Create the cyclic executive schedule
  schedule = [None] * maj_cyc

  #sort tasks by frequency
  l_tasks.sort(key=lambda x: x.Ti)

  curr_time = 0
  time_remaining_in_min_cyc = min_cyc
  while curr_time < maj_cyc:
    for task in l_tasks:
      if (task.last_executed == None or curr_time - task.last_executed >= task.Ti) and (time_remaining_in_min_cyc >= task.Ci):
        task.last_executed = curr_time
        for _ in range(task.Ci):
          schedule[curr_time] = task.task_id
          curr_time += 1
          time_remaining_in_min_cyc -= 1
          if time_remaining_in_min_cyc == 0:
            time_remaining_in_min_cyc = min_cyc
    curr_time += 1
    time_remaining_in_min_cyc -= 1
    if time_remaining_in_min_cyc == 0:
      time_remaining_in_min_cyc = min_cyc
    
  for task in tasks:
    task.last_executed = None
  return schedule


def rms_schedule(tasks, total_time):
  schedule = []
  #local task list sorted by period (lowest to highest)
  l_tasks = sorted(tasks, key=lambda x: x.Ti)


  
  #iterate through each time slot
  for curtime in range(total_time):

    # set availability
    for task in l_tasks:
      if task.remaining_time > 0:
        task.available = True
      else: 
        task.available = False
      if curtime % task.Ti == 0:
        task.available = True
        task.remaining_time = task.Ci


    seltaskindex = len(l_tasks) - 1 #highest period task index to avoid undue selection
    #select task with shortest period that is also available
    for i in range(len(l_tasks)):
      if l_tasks[i].available and l_tasks[i].Ti < l_tasks[seltaskindex].Ti:
        seltaskindex = i

    #if all tasks are unavailable
    unavailcount = 0
    for task in l_tasks:
      if task.available is False:
        unavailcount += 1
    if unavailcount >= len(l_tasks):
      seltaskindex = None
    

    #assign taskid to schedule
    if seltaskindex is not None:
      schedule.append(l_tasks[seltaskindex].task_id)
      l_tasks[seltaskindex].remaining_time -= 1
      continue
    else:
      schedule.append(None)
      continue
    
  return schedule


fp = "/Users/sebastianrowe/Desktop/programming/Visual Studio Code/ucf/_EEE4475/tasksets/taskset1.csv"
tasks = read_tasks_from_csv(fp)


cyc_sch = cyclic_schedule(tasks)
for task in tasks:
  print(task.__str__())
rms_sch = rms_schedule(tasks, 250)
print(f"cyclic schedule is --> {cyc_sch}\n\n\n")
print(f"rms schedule is --> {rms_sch}")
