import yaml
import subprocess
import os
import sys

base_config_path = 'config/qmt_v54q3.yaml'

# 1. Verify the base config exists before doing anything
if not os.path.exists(base_config_path):
    print(f"Error: Could not find {base_config_path}. Are you in the right directory?")
    sys.exit(1)

# 2. Load the original configuration
try:
    with open(base_config_path, 'r') as file:
        config = yaml.safe_load(file)
except yaml.YAMLError as exc:
    print(f"Error parsing YAML: {exc}")
    sys.exit(1)

# 3. Update the budget_time to 24 hours (86,400 seconds)
config['budget_time'] = 86400

# 4. Loop 5 times
for i in range(1, 6):
    run_folder = f"data/qmt_v54q3_run{i}"
    new_config_path = f"config/qmt_v54q3_run{i}.yaml"
    
    # Update the output directory for this specific run
    config['experiment_folder'] = run_folder
    
    # Write the modified configuration (sort_keys=False keeps your original YAML order)
    with open(new_config_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False, sort_keys=False)
    
    print(f"\n==============================")
    print(f"--- Starting Run {i}/5 ---")
    print(f"Config: {new_config_path} | Output: {run_folder}")
    print(f"==============================\n")
    
    # 5. Execute the QMT script with error catching
    try:
        subprocess.run(["python3", "-m", "lib.qmt", new_config_path], check=True)
        print(f"\n--- Run {i} completed successfully ---")
    except subprocess.CalledProcessError as e:
        print(f"\n--- Error: Run {i} crashed with exit code {e.returncode} ---")
        print("Moving on to the next run...")
        continue # Ensures the next 24-hour block still runs even if this one failed