import threading
from model.JobQueueSingleton import JobQueueSingleton

class JobController:
    def __init__(self):
        self.job_queue = JobQueueSingleton()
        self.jobs = []
        self.lock = threading.Lock()
    
    def add_job(self, fn, *args, **kwargs):
        try:
            job_id = self.job_queue.add_job(fn, *args, **kwargs)
            with self.lock:
                self.jobs.append(job_id)
            return job_id
        except Exception as e:
            raise Exception(f"Error adding job") 
            
    def get_job_status(self, job_id):
        try:
            return self.job_queue.get_status(job_id)
        except Exception as e:
            raise Exception(f"Error getting job status")
         
    def get_all_jobs(self):
        try:
            return self.jobs
        except Exception as e:
            raise Exception(f"Error getting all jobs") 
        
    def get_running_jobs(self):
        try:
            with self.lock:
                return [job_id for job_id in self.jobs if self.get_job_status(job_id) == "running"]
        except Exception as e:
            raise Exception(f"Error getting running jobs") 
        
    def get_queued_jobs(self):
        try:    
            with self.lock:
                return [job_id for job_id in self.jobs if self.get_job_status(job_id) == "queued"]
        except Exception as e:
            raise Exception(f"Error getting queued jobs") 
        
    def get_error_jobs(self):
        try:
            with self.lock:
                return [job_id for job_id in self.jobs if self.get_job_status(job_id) == "error"]
        except Exception as e:
            raise Exception(f"Error getting errored jobs") 
    def get_completed_jobs(self):
        try:
            with self.lock:
                return [job_id for job_id in self.jobs if self.get_job_status(job_id) == "completed"]
        except Exception as e:
            raise Exception(f"Error getting completed jobs") 
        
    def clear_completed_jobs(self):
        try:
            with self.lock:
                completed_jobs = self.get_completed_jobs()
                for job_id in completed_jobs:
                    self.jobs.remove(job_id)
                    del self.job_queue.status[job_id]
        except Exception as e:
            raise Exception(f"Error cleaning jobs") 
    def stop_all_running_jobs(self):
        try:
            running_jobs = self.get_running_jobs()
        except :
            raise Exception(f"Errot getting all jobs") 
        try:
            for job_id in running_jobs:
                self.job_queue.stop_job(job_id)
        except Exception as e:
            raise Exception(f"Error closing job {job_id}") 