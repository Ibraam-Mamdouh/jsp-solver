from jsp.models import Operation, Job, JSPInstance

def load_instance(path: str, name: str) -> JSPInstance:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found {path}")
    
    instance_idx = -1

    for i, line in enumerate(lines):
        parts = line.strip().split()
        if len(parts) == 2 and parts[0].lower() == "instance" and parts[1] == name:
            instance_idx = i
            break
    if instance_idx == -1:
        raise ValueError(f"Instance '{name}' not found in the file.")

    idx = instance_idx + 1
    n_jobs, n_machines = None, None

    while idx < len(lines):
        tokens = lines[idx].strip().split()
        if len(tokens) == 2 and all(token.isdigit() for token in tokens):
            n_jobs = int(tokens[0])
            n_machines = int(tokens[1])
            break
        idx += 1
    if n_jobs is None or n_machines is None:
        raise ValueError(f"Could not find dimensions (n_jobs, n_machines) for instance '{name}'.")
    
    jobs = []
    for job_id in range(n_jobs):
        idx += 1
        if idx >= len(lines):
            raise ValueError(f"Unexpected end of file while reading jobs for instance '{name}'.")
        
        tokens = lines[idx].strip().split()
        if not tokens:
            raise ValueError(f"Unexpected empty line while reading jobs in instance '{name}' at line {idx + 1}.")
        
        ints = [int(token) for token in tokens]

        if len(ints) % 2 != 0:
            raise ValueError(f"Malformed data in instance '{name}': Job line has odd number of tokens ({len(ints)}).")

        operations = []
        for i in range(0, len(ints), 2):
            machine = ints[i]
            duration = ints[i + 1]
            operations.append(Operation(machine=machine, duration=duration))

        jobs.append(Job(job_id=job_id, operations=operations))

    return JSPInstance(
        name=name,
        n_jobs=n_jobs,
        n_machines=n_machines,
        jobs=jobs
    )