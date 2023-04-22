import threading
import uuid

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
        with self.lock:
            self.status[job_id] = "running"
        fn(*args, **kwargs)
        with self.lock:
            self.status[job_id] = "completed"
    
    def get_status(self, job_id):
        return self.status.get(job_id, None)