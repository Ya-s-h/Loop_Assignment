from rq import SimpleWorker, Connection, Worker
from worker import conn

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(['default'], connection=conn)
        worker.work(with_scheduler=True)