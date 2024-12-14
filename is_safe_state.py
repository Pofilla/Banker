def is_safe_state(available, allocation, max_need, num_processes, num_resources):
    """
    Check if the system is in a safe state after resource allocation.
    """
    work = available[:]
    finish = [False] * num_processes
    safe_sequence = []

    while len(safe_sequence) < num_processes:
        found_process = False
        for p in range(num_processes):
            if not finish[p]:
                if all(max_need[p][r] - allocation[p][r] <= work[r] for r in range(num_resources)):
                    # This process can execute safely
                    for r in range(num_resources):
                        work[r] += allocation[p][r]
                    finish[p] = True
                    safe_sequence.append(p)
                    found_process = True
                    break

        if not found_process:
            return False, []  # Not safe state

    return True, safe_sequence