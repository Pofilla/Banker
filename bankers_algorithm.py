from is_safe_state import is_safe_state

def process_request(process, request, available, allocation, max_need, num_resources):
    """
    Handle resource requests for a specific process.
    """
    if all(request[r] <= max_need[process][r] - allocation[process][r] for r in range(num_resources)) and \
       all(request[r] <= available[r] for r in range(num_resources)):
        # Temporarily allocate resources
        for r in range(num_resources):
            available[r] -= request[r]
            allocation[process][r] += request[r]

        # Check safe state after allocation
        safe, sequence = is_safe_state(available, allocation, max_need, len(allocation), num_resources)
        if safe:
            return True, sequence
        else:
            # Rollback the allocation
            for r in range(num_resources):
                available[r] += request[r]
                allocation[process][r] -= request[r]
            return False, "System would enter unsafe state."
    else:
        return False, "Request exceeds maximum need or available resources."