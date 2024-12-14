def get_input():
    """
    Helper function to get input data from the user.
    """
    num_processes = int(input("Enter the number of processes: "))
    num_resources = int(input("Enter the number of resources: "))

    print("Enter the Allocation matrix:")
    allocation = [list(map(int, input(f"P{i}: ").split())) for i in range(num_processes)]

    print("Enter the Max Need matrix:")
    max_need = [list(map(int, input(f"P{i}: ").split())) for i in range(num_processes)]

    print("Enter the Available resources vector:")
    available = list(map(int, input().split()))

    return num_processes, num_resources, allocation, max_need, available