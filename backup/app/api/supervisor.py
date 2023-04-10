from typing import List
from loguru import logger

from app.api.producer import Producer
from app.api.watcher import Watcher

class Supervisor:

    def __init__(self, producers: List[Producer]) -> None:
        self._producers = producers

    def start_processes(self) -> None: 
        for producer in self._producers:
            producer.start()

    def monitor(self) -> None:
        while True:
            for producer in self._producers:
                if not producer.is_alive():
                    logger.info(f"Supervisor terminating Producer-{producer.id}")

                    new_producer = self._restart_process(producer)
                    self._producers.remove(producer)
                    self._producers.append(new_producer)
                    new_producer.start()

                    logger.info(f"Supervisor replaced Producer-{producer.id} with Producer-{new_producer.id}")

                    producer.terminate()
                    producer.join()

    
    def restart_process(self, process: Producer) -> Producer:
        path = process.watcher.path
        repo = process.watcher.backup_repo
        s3_service = process.watcher.s3_service
        actor_wait_time = process.watcher.actor_wait_time

        new_watcher = Watcher(path, repo, s3_service, actor_wait_time)
        new_producer = Producer(new_watcher)

        return new_producer
