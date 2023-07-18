import threading
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
        self.status = {}
        self.lock = threading.Lock()
    
    def add_job(self, fn, *args, **kwargs):
        job_id = str(uuid.uuid4())
        job_thread = threading.Thread(target=self._run_job, args=(job_id, fn, args, kwargs))
        with self.lock:
            self.job_queue.append((job_id, job_thread))
            self.status[job_id] = "queued"
        job_thread.start()
        return job_id
    
    def _run_job(self, job_id, fn, args, kwargs):
        try:
            with self.lock:
                self.status[job_id] = "running"
            fn(*args, **kwargs)
            with self.lock:
                self.status[job_id] = "completed"
        except Exception as e:
            with self.lock:
                self.status[job_id] = "error"
            self.status[job_id] = "completed"
    
    def get_status(self, job_id):
        return self.status.get(job_id, None)
    
    def stop_job(self, job_id):
        with self.lock:
            for i, (jid, thread) in enumerate(self.job_queue):
                if jid == job_id:
                    thread._stop()
                    self.job_queue.pop(i)
                    self.status[job_id] = "stopped"
                    break
    
## Run example with arguments
# import modelController

# job_queue = JobQueueSingleton()
# job_id = job_queue.add_job(modelController.CreateModel, data, 'MixedDistance')
# status = job_queue.get_status(job_id)