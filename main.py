class RoundRobin(object):
    def __init__(self):
        self.pass_ = None

    def process_data(self, no_of_processes):
        process_data = []
        temp_list = []
        final_list = []

        with open('round_robin.txt', 'r') as input_file:
            for i in range(50):
                data = input_file.readline()
                if not data == '':
                    temp_list.append(data.split(' '))

        for i in range(len(temp_list)):
            int_list = list(map(int, temp_list[i]))  # str to int
            final_list.append(int_list)  # [[1, 5, 5], [2, 9, 6], [3, 3, 7]]

        for i in range(no_of_processes):
            temporary = []
            process_id = final_list[i][0]
            arrival_time = final_list[i][1]
            burst_time = final_list[i][2]

            temporary.extend([process_id, arrival_time, burst_time, 0, burst_time])
            process_data.append(temporary)

        quantum_time = int(input("Time Quantum: "))
        RoundRobin.scheduling_process(self, process_data, quantum_time)

    def scheduling_process(self, process_data, time_slice):
        start_time = []
        exit_time = []
        executed_process = []
        ready_queue = []
        s_time = 0

        process_data.sort(key=lambda x: x[1])

        '''
        Sort processes according to the Arrival Time
        '''
        while 1:
            normal_queue = []
            temp = []
            for i in range(len(process_data)):
                if process_data[i][1] <= s_time and process_data[i][3] == 0:
                    present = 0
                    if len(ready_queue) != 0:
                        for k in range(len(ready_queue)):
                            if process_data[i][0] == ready_queue[k][0]:
                                present = 1
                    '''
                    The above if loop checks that the next process is not a part of ready_queue
                    '''
                    if present == 0:
                        temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                        ready_queue.append(temp)
                        temp = []
                    '''
                    The above if loop adds a process to the ready_queue only if it is not already present in it
                    '''
                    if len(ready_queue) != 0 and len(executed_process) != 0:
                        for k in range(len(ready_queue)):
                            if ready_queue[k][0] == executed_process[len(executed_process) - 1]:
                                ready_queue.insert((len(ready_queue) - 1), ready_queue.pop(k))
                    '''
                    The above if loop makes sure that the recently executed process is appended at the end of ready_queue
                    '''
                elif process_data[i][3] == 0:
                    temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                    normal_queue.append(temp)
                    temp = []
            if len(ready_queue) == 0 and len(normal_queue) == 0:
                break
            if len(ready_queue) != 0:
                if ready_queue[0][2] > time_slice:
                    '''If process has remaining burst time greater than the time slice, it will execute for a time 
                    period equal to time slice and then switch '''
                    start_time.append(s_time)
                    s_time = s_time + time_slice
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(ready_queue[0][0])
                    for j in range(len(process_data)):
                        if process_data[j][0] == ready_queue[0][0]:
                            break
                    process_data[j][2] = process_data[j][2] - time_slice
                    ready_queue.pop(0)
                elif ready_queue[0][2] <= time_slice:
                    '''If a process has a remaining burst time less than or equal to time slice, it will complete its 
                    execution '''
                    start_time.append(s_time)
                    s_time = s_time + ready_queue[0][2]
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(ready_queue[0][0])
                    for j in range(len(process_data)):
                        if process_data[j][0] == ready_queue[0][0]:
                            break
                    process_data[j][2] = 0
                    process_data[j][3] = 1
                    process_data[j].append(e_time)
                    ready_queue.pop(0)
            elif len(ready_queue) == 0:
                if s_time < normal_queue[0][1]:
                    s_time = normal_queue[0][1]
                if normal_queue[0][2] > time_slice:
                    '''If process has remaining burst time greater than the time slice, it will execute for a time 
                    period equal to time slice and then switch '''
                    start_time.append(s_time)
                    s_time = s_time + time_slice
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(normal_queue[0][0])
                    for j in range(len(process_data)):
                        if process_data[j][0] == normal_queue[0][0]:
                            break
                    process_data[j][2] = process_data[j][2] - time_slice
                elif normal_queue[0][2] <= time_slice:
                    '''If a process has a remaining burst time less than or equal to time slice, it will complete its 
                    execution '''
                    start_time.append(s_time)
                    s_time = s_time + normal_queue[0][2]
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(normal_queue[0][0])
                    for j in range(len(process_data)):
                        if process_data[j][0] == normal_queue[0][0]:
                            break
                    process_data[j][2] = 0
                    process_data[j][3] = 1
                    process_data[j].append(e_time)
        t_time = RoundRobin.calculate_turn_around_time(self, process_data)
        w_time = RoundRobin.calculate_waiting_time(self, process_data)
        RoundRobin.print_data(self, process_data, t_time, w_time)

    def calculate_turn_around_time(self, process_data):
        if self.pass_:
            pass

        total_turnaround_time = 0
        for i in range(len(process_data)):
            turnaround_time = process_data[i][5] - process_data[i][1]
            '''
            turnaround_time = completion_time - arrival_time
            '''
            total_turnaround_time = total_turnaround_time + turnaround_time
            process_data[i].append(turnaround_time)
        average_turnaround_time = total_turnaround_time / len(process_data)
        '''
        average_turnaround_time = total_turnaround_time / no_of_processes
        '''
        return average_turnaround_time

    def calculate_waiting_time(self, process_data):
        if self.pass_:
            pass

        total_waiting_time = 0
        for i in range(len(process_data)):
            waiting_time = process_data[i][6] - process_data[i][4]
            '''
            waiting_time = turnaround_time - burst_time
            '''
            total_waiting_time = total_waiting_time + waiting_time
            process_data[i].append(waiting_time)
        average_waiting_time = total_waiting_time / len(process_data)
        '''
        average_waiting_time = total_waiting_time / no_of_processes
        '''
        return average_waiting_time

    def print_data(self, process_data, average_turnaround_time, average_waiting_time):
        if self.pass_:
            pass

        process_data.sort(key=lambda x: x[0])

        for i in process_data:
            for j in range(5):
                i.pop(1)

        '''
        Sort processes according to the Process ID
        '''
        print("Process ID  Turnaround Time  Waiting Time")

        for i in range(len(process_data)):
            for j in range(len(process_data[i])):
                print(process_data[i][j], end="                ")
            print()

        print()
        print(f'Average Turnaround Time: {round(average_turnaround_time)}')
        print(f'Average Waiting Time: {round(average_waiting_time)}')


if __name__ == "__main__":
    number_of_processes = sum(1 for line in open('round_robin.txt'))
    RoundRobin().process_data(number_of_processes)
