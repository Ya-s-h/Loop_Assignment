## Restaurant Monitoring System

### Project Description
This project serves as a take-home interview that assesses the candidate's real-life problem-solving abilities, 
the capacity to build a system from the ground up,
and handle complex algorithmic challenges.

### Problem Statement   

Loop, a company that monitors several restaurants in the US, 
needs an efficient system to track whether a store is online or offline.
Each restaurant is expected to be online during its business hours,
but due to unforeseen circumstances, a store might go inactive for
a few hours. Restaurant owners are keen on obtaining a comprehensive report detailing
how often such incidents have occurred in the past. 

---
[For more Details Visit](https://loopxyz.notion.site/Take-home-interview-Store-Monitoring-12664a3c7fdf472883a41457f0c9347d)

### Setup

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/Ya-s-h/Loop_Assignment
    cd Loop_Assignment
    ```

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Server:**
    ```bash
    python main.py
    ```

4. **Access the API:**
    The server should be running at `http://127.0.0.1:5000/` or `http://localhost:5000/`.

---
### Challenges Faced During Parallel Execution

Despite employing different strategies to optimize parallel execution, challenges were encountered, and the following attempts were made:

1. **Performance Issues:**
    If parallel execution using ThreadPoolExecutor is causing performance issues, consider exploring other concurrency models like ProcessPoolExecutor or asynchronous programming with asyncio. In the attempt below, a ProcessPoolExecutor is used:

    ```python
    # Example code snippet
    with concurrent.futures.ProcessPoolExecutor() as pool:
        results = pool.map(your_function, your_data)
    ```

2. **Optimizing Parallel Tasks:**
    Despite efforts to optimize tasks running in parallel and avoid bottlenecks by adjusting the batch size, challenges persist:

    ```python
    # Example code snippet
    batch_size = 1000
    for batch in range(0, len(your_data), batch_size):
        process_batch(your_data[batch:batch + batch_size])
    ```

3. **Resource Limitations:**
    Checking for resource limitations is crucial, especially when running parallel tasks on a machine with limited resources. Adjusting the number of workers or processes based on available resources is essential:

    ```python
    # Example code snippet
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = pool.map(your_function, your_data)
    ```

Despite these attempts, challenges persisted in achieving the desired optimization for parallel execution. Further investigation and alternative strategies may be required to address these performance issues effectively.

---

### Generate Report Endpoint

To generate a report for a particular `store_id`, make a POST request to the `/trigger_report` endpoint. Include the `store_id` as a request body parameter.

#### Endpoint

- **URL:** `/trigger_report`
- **Method:** `POST`

#### Request Body

Provide the `store_id` as a parameter in the request body.

```json
{
  "store_id": 123456789
}