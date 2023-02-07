import asyncio
from dataclasses import dataclass
from datetime import timedelta
from typing import Dict

import speedtest
from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker


@dataclass
class SpeedTestResult:
    download_speed: float
    upload_speed: float


s = speedtest.Speedtest()


@activity.defn
async def run_speed_test(input: SpeedTestResult):
    input.download_speed = round(s.download() / 1048576, 2)
    input.upload_speed = round(s.upload() / 1048576, 2)
    return {"download_speed": input.download_speed, "upload_speed": input.upload_speed}


@workflow.defn(sandboxed=False)
class SpeedTestWorkflow:
    @workflow.run
    async def run(self, input: SpeedTestResult) -> Dict[any, any]:
        

        result = await workflow.execute_activity(
            run_speed_test,
            SpeedTestResult(input.download_speed, input.upload_speed),
            start_to_close_timeout=timedelta(seconds=60),
   
        )
        print(f"Download speed: {result['download_speed']} Mbps")
        print(f"Upload speed: {result['upload_speed']} Mbps")
        print("Waiting 3 seconds before next test...")
        await asyncio.sleep(3)

        return SpeedTestResult(result["download_speed"], result["upload_speed"])


async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="task-queue",
        workflows=[SpeedTestWorkflow],
        activities=[run_speed_test],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
