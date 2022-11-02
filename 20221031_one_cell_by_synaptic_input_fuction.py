def one_cell(w_pos):
    start_scope()


    N_Excit=384
    N_Inhib=96
    weight_scaling_factor=5.33
    t_stimulus_start=100 * b2.ms
    t_stimulus_duration=9999 * b2.ms
    coherence_level=0.
    stimulus_update_interval=30 * b2.ms
    mu0_mean_stimulus_Hz=250.
    stimulus_std_Hz=20.
    N_extern=1000
    firing_rate_extern=9.8 * b2.Hz
    w_pos=1.9
    f_Subpop_size=0.25  # .15 in publication [1]                     
    max_sim_time=1000. * b2.ms 
    stop_condition_rate=None
                                    
    monitored_subset_size=512, 
    E_leak_excit = -70.0 * b2.mV

    print("simulating {} neurons. Start: {}".format(N_Excit + N_Inhib, time.ctime()))
    t_stimulus_end = t_stimulus_start + t_stimulus_duration

    N_Group_A = int(N_Excit * f_Subpop_size)  # size of the excitatory subpopulation sensitive to stimulus A
    N_Group_B = N_Group_A  # size of the excitatory subpopulation sensitive to stimulus B
    N_Group_Z = N_Excit - N_Group_A - N_Group_B  # (1-2f)Ne excitatory neurons do not respond to either stimulus.

    Cm_excit = 0.5 * b2.nF  # membrane capacitance of excitatory neurons
    G_leak_excit = 25.0 * b2.nS  # leak conductance
    E_leak_excit = -90.0 * b2.mV  # reversal potential
    v_spike_thr_excit = 50.0 * b2.mV  # spike condition
    v_reset_excit = -60.0 * b2.mV  # reset voltage after spike
    t_abs_refract_excit = 2. * b2.ms  # absolute refractory period

    # specify the inhibitory interneurons:
    # N_Inhib = 200
    Cm_inhib = 0.2 * b2.nF
    G_leak_inhib = 20.0 * b2.nS
    E_leak_inhib = -90.0 * b2.mV
    v_spike_thr_inhib = -50.0 * b2.mV
    v_reset_inhib = -60.0 * b2.mV
    t_abs_refract_inhib = 1.0 * b2.ms

    # specify the AMPA synapses
    E_AMPA = 0.0 * b2.mV
    tau_AMPA = 2.5 * b2.ms

    # specify the GABA synapses
    E_GABA = -70.0 * b2.mV
    tau_GABA = 5.0 * b2.ms

    # specify the NMDA synapses
    E_NMDA = 0.0 * b2.mV
    tau_NMDA_s = 100.0 * b2.ms
    tau_NMDA_x = 2. * b2.ms
    alpha_NMDA = 0.5 * b2.kHz

    # projections from the external population
    g_AMPA_extern2inhib = 1.62 * b2.nS
    g_AMPA_extern2excit = 2.1 * b2.nS

    # projectsions from the inhibitory populations
    g_GABA_inhib2inhib = weight_scaling_factor * 1.25 * b2.nS
    g_GABA_inhib2excit = weight_scaling_factor * 1.60 * b2.nS

    # projections from the excitatory population
    g_AMPA_excit2excit = weight_scaling_factor * 0.012 * b2.nS
    g_AMPA_excit2inhib = weight_scaling_factor * 0.015 * b2.nS
    g_NMDA_excit2excit = weight_scaling_factor * 0.040 * b2.nS
    g_NMDA_excit2inhib = weight_scaling_factor * 0.045 * b2.nS  # stronger projection to inhib.

    # weights and "adjusted" weights.
    w_neg = 1. - f_Subpop_size * (w_pos - 1.) / (1. - f_Subpop_size)
    # We use the same postsyn AMPA and NMDA conductances. Adjust the weights coming from different sources:
    w_ext2inhib = g_AMPA_extern2inhib / g_AMPA_excit2inhib
    w_ext2excit = g_AMPA_extern2excit / g_AMPA_excit2excit
    # other weights are 1
    # print("w_neg={}, w_ext2inhib={}, w_ext2excit={}".format(w_neg, w_ext2inhib, w_ext2excit))A
    # Define the inhibitory population



    excit_lif_dynamics = """
            s_NMDA_total : 1  # the post synaptic sum of s. compare with s_NMDA_presyn
            dv/dt = (
            - G_leak_excit * (v-E_leak_excit)
            - g_AMPA_excit2excit * s_AMPA * (v-E_AMPA)
            - g_GABA_inhib2excit * s_GABA * (v-E_GABA)
            - g_NMDA_excit2excit * s_NMDA_total * (v-E_NMDA)/(1.0+1.0*exp(-0.062*v/volt)/3.57)
            )/Cm_excit : volt (unless refractory)
            ds_AMPA/dt = -s_AMPA/tau_AMPA : 1
            ds_GABA/dt = -s_GABA/tau_GABA : 1
            ds_NMDA/dt = -s_NMDA/tau_NMDA_s + alpha_NMDA * x * (1-s_NMDA) : 1
            dx/dt = -x/tau_NMDA_x : 1
        """


    one_neuron = NeuronGroup(1, model=excit_lif_dynamics,
                            threshold="v>v_spike_thr_excit", reset="v=v_reset_excit",
                            refractory=t_abs_refract_excit, method="rk2")

    one_neuron.v = rnd.uniform(E_leak_excit / b2.mV, high=E_leak_excit / b2.mV + 5., size=one_neuron.N) * b2.mV




    # network parameters
    N_E = 1000
    gamma = 0.25
    N_I = round(gamma * N_E)
    N = N_E + N_I
    epsilon = 0.1
    C_E = epsilon * N_E
    C_ext = C_E

    # neuron parameters
    tau = 10 * ms
    theta = 1 * mV
    V_r = 0 * mV
    tau_rp = 2 * ms

    # synapse parameters
    J = 0.1 * mV
    D = 1.5 * ms
    nu_ext = 1 *Hz
    # external stimulus
    nu_thr = theta / (J * C_E * tau)

    defaultclock.dt = 0.1 * ms

    Poisson_NE = 1000
    g = 1


    # with and without NMDA 와 비교하기 
    exc_poisson_input = PoissonInput(
            target=one_neuron, target_var="s_AMPA", N=N_E, rate=1*nu_ext, weight= 1.0)       

    inh_poisson_input = PoissonInput(
            target=one_neuron, target_var="s_GABA", N=N_I, rate=1*nu_ext, weight= 1.0)


    #NDMA input 
    sNMDA_A_total = []

    @network_operation()
    def update_nmda_sum():
            sum_sNMDA_A = sum(one_neuron.s_NMDA)

            # note the _ at the end of s_NMDA_total_ disables unit checking
            one_neuron.s_NMDA_total_ = (w_pos * sum_sNMDA_A)  ## 자기 자신의 nmda input 만을 받는다. 
            sNMDA_A_total.append(sum_sNMDA_A)


    # set a self-recurrent synapse to introduce a delay when updating the intermediate
    # gating variable x

    syn_x_A2A = Synapses(one_neuron, one_neuron, on_pre="x += 1.", delay=0.5 * b2.ms)
    syn_x_A2A.connect(j="i")


    








