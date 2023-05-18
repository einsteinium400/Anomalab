import multiprocessing
import uuid
import traceback

import multiprocessing
import uuid
import traceback


class JobQueueSingleton:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(JobQueueSingleton, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.job_queue = []
        self.manager = multiprocessing.Manager()
        self.status = self.manager.dict()
        self.lock = multiprocessing.Lock()

    def add_job(self, fn, *args, **kwargs):
        job_id = str(uuid.uuid4())
        job_process = JobProcess(job_id, fn, args, kwargs, self.status, self.lock)
        with self.lock:
            self.job_queue.append((job_id, job_process))
            self.status[job_id] = "queued"
        self.status[job_id] = "running"
        job_process.start()
        return job_id

    def get_status(self, job_id):
        return self.status.get(job_id, None)

    def stop_job(self, job_id):
        with self.lock:
            for i, (jid, process) in enumerate(self.job_queue):
                if jid == job_id:
                    process.terminate()
                    self.job_queue.pop(i)
                    self.status[job_id] = "stopped"
                    break


class JobProcess(multiprocessing.Process):
    def __init__(self, job_id, fn, args, kwargs, status, lock):
        super(JobProcess, self).__init__()
        self.job_id = job_id
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.status = status
        self.lock = lock

    def run(self):
        try:
            with self.lock:
                self.status[self.job_id] = "running"
            self.fn(*self.args, **self.kwargs)
            with self.lock:
                self.status[self.job_id] = "completed"
        except Exception as e:
            with self.lock:
                self.status[self.job_id] = "error"
                print(traceback.print_exc())
                print(f"Error in job {self.job_id}: {e}")
            self.status[self.job_id] = "completed"


## Run example with arguments
# import modelController

# job_queue = JobQueueSingleton()
# job_id = job_queue.add_job(modelController.CreateModel, data, 'MixedDistance')
# status = job_queue.get_status(job_id)