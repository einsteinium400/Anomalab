import multiprocessing
from model.JobQueueSingleton import JobQueueSingleton


class JobController:
    def __init__(self):
        self.job_queue = JobQueueSingleton()
        self.jobs = []
        self.lock = multiprocessing.Lock()

    def add_job(self, fn, *args, **kwargs):
        job_id = self.job_queue.add_job(fn, *args, **kwargs)
        with self.lock:
            self.jobs.append(job_id)
        return job_id

    def get_job_status(self, job_id):
        return self.job_queue.get_status(job_id)

    def get_all_jobs(self):
        return self.jobs

    def get_running_jobs(self):
        with self.lock:
            return [job_id for job_id in self.jobs if self.get_job_status(job_id) == "running"]

    def get_queued_jobs(self):
        with self.lock:
            return [job_id for job_id in self.jobs if self.get_job_status(job_id) == "queued"]

    def get_error_jobs(self):
        with self.lock:
            return [job_id for job_id in self.jobs if self.get_job_status(job_id) == "error"]

    def get_completed_jobs(self):
        with self.lock:
            return [job_id for job_id in self.jobs if self.get_job_status(job_id) == "completed"]

    def clear_completed_jobs(self):
        with self.lock:
            completed_jobs = self.get_completed_jobs()
            for job_id in completed_jobs:
                self.jobs.remove(job_id)
                del self.job_queue.status[job_id]

    def stop_all_running_jobs(self):
        running_jobs = self.get_running_jobs()
        for job_id in running_jobs:
            print("Stopping job ", job_id)
            self.job_queue.stop_job(job_id)