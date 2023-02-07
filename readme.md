# Speedtest Workflow


## Run the program

```bash
python3 run_speed.py
python3 run_workflow.py
```

## Terminate

```
temporal workflow terminate --workflow-id="my-workflow-id"
```

## Post

```
curl -X POST http://localhost:5000/ -H "Content-Type: application/json" -d '{"download_speed":0.0, "upload_speed":0.0}'
```
## Get

```
curl -X GET http://localhost:5000/speedtest
```