import time
import multiprocessing as mp
import matplotlib.pyplot as plt
from test_data import read_number_test_data
from serial_quick_sort import serial_quick_sort


NUM_PROCESSES_LIST = [2,4,6,8,10,12]

def execute_quicksort_in_parallel(array, queue, id):
    result = serial_quick_sort(array)
    # save result to queue
    queue.put([id, result])
    queue.put({"id": id, "result": result})

if __name__ == '__main__':
    data = read_number_test_data()
    
    # SERIAL EXECUTION
    print("Starting serial quicksort execution.")
    serial_start_time = time.time()
    data_serial_sorted = serial_quick_sort(data)
    serial_total_time = time.time() - serial_start_time
    print("Quicksort serial execution time: " + str(round(serial_total_time, 4)))
    print("___________________________")

    # PARALLEL EXECUTION
    mp.set_start_method('spawn')

    execution_times = []
    print("Starting parallel quicksort execution.")
    
    for NUM_PROCESSES in NUM_PROCESSES_LIST:
        print("Starting parallel quicksort execution with " + str(NUM_PROCESSES) + " processes.")

        # start timer
        start_time = time.time()

        # list which will contain the pivot elements
        pivot_elements = []

        # create data chunks according to pivot elements
        # 2-dim list which will contain the list for each processes (e.g. [[list0],[list1],...])
        data_chunks = []
        # append empty array for elements which are smaller than the first pivot element
        data_chunks.append([])

        # append elements to pivot element list and empty lists to data chunks list
        for num in range(1, NUM_PROCESSES):
            pivot_elements.append(data[num])
            data_chunks.append([])
        
        # sort pivot elements
        pivot_elements = sorted(pivot_elements)
        
        # classifying the element into the various data chunks 
        # (e.g. data_chunks[0] <= pivot_elements[0] <= data_chunks[1] <= pivot_elements[1] <= data_chunks[2])
        for num_value in data:
            for i, pivot_value in enumerate(pivot_elements):
                if num_value <= pivot_value:
                    data_chunks[i].append(num_value)
                    break
                # add element to the last data_chunk, if the end of the pivot_elements list is reached
                if i + 1 == len(pivot_elements):
                    data_chunks[i+1].append(num_value)

        queue = mp.Queue()
        # start a process for each data_chunk with the data, queue and process ids as args
        processes = []
        for i, list in enumerate(data_chunks):
            process = mp.Process(target=execute_quicksort_in_parallel, args=(data_chunks[i], queue, i))
            process.start()
            processes.append(process)

        # get the results from the multiprocessing Queue and store them in an array
        queue_results = []
        for process in processes:
            queue_results.append(queue.get())

        # join the processes in the end
        for process in processes:
            process.join()

        # The results are not stored to the queue in the right order (e.g. 
        # it could be that the third process is finished before the first one)
        # Therefore, the final result has to be constructed by adding the result lists to the sorted_list in the right order
        # For that, the process id is used
        sorted_list = []
        for i in range(0, NUM_PROCESSES):
            # iterate over queue_results
            for result in queue_results:
                # if the process id matches the number of the process, add the result list to the result_list
                if result["id"] == i:
                    sorted_list = sorted_list + result["result"]

        end_time = time.time()

        print("Execution time using " + str(NUM_PROCESSES) + " processes: " + str(round(end_time-start_time, 4)))
        print("___________________________")
        execution_times.append(end_time-start_time)        

    print("Quicksort parallel execution successfully finished.")
        
    plt.plot(NUM_PROCESSES_LIST, execution_times)
    plt.ylabel('Execution Time in s')
    plt.xlabel('Number of Parallel Processes')
    plt.show()
    