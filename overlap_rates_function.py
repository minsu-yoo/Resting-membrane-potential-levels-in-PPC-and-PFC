

def overlap_rates(data, start, end, trial_num):
    time = data[0]['time']

    for i in range(trial_num):
        
        plt.plot(time[start:end], data[i]['pop_rate_a'][start:end], 'c', alpha = 0.3, linewidth= 3)
        #plt.plot(time[start:end], data[median_index]['pop_rate_a'][start:end], 'k', alpha = 1, linewidth= 1)
        #plt.plot(time, rate_mean, 'b-', label='mean_1', linewidth=0.8)

        
    plt.ylabel('Firing rate (Spikes/s)')
    plt.xlabel('time (ms)')
    plt.show()

    
    
def traces_by_trials(i):
    print(data_keys[i])    
    data_for_traces = (data[data_keys[i]])
    overlap_rates(data_for_traces, 0, 2500, 10)



