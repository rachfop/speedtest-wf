import asyncio

import matplotlib.pyplot as plt
from temporalio.client import Client

# Import the workflow from the previous code
from run_speed import SpeedTestResult, SpeedTestWorkflow


async def main(input: SpeedTestResult):
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")

    download_speed_list = []
    upload_speed_list = []
    iterations = 0

    for i in range(100):
        result = await client.execute_workflow(
            SpeedTestWorkflow.run,
            SpeedTestResult(input.download_speed, input.upload_speed),
            id="my-workflow-id",
            task_queue="task-queue",
        )

        download_speed_list.append(result["download_speed"])
        upload_speed_list.append(result["upload_speed"])
        iterations += 1

    await graph_results(download_speed_list, upload_speed_list)


async def graph_results(download_speed_list, upload_speed_list):
    # Plot the results using Matplotlib
    plt.plot(download_speed_list, label="download_speed")
    plt.plot(upload_speed_list, label="upload_speed")
    plt.legend()
    plt.xlabel("Iteration")
    plt.ylabel("Speed (Mbps)")
    plt.title("Internet Speed Test Results")
    plt.savefig(f"speed_test_results.png")
    plt.show()
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main(SpeedTestResult(0, 0)))
