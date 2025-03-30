#!/bin/bash
echo "Starting evaluate_instance.py..."
# python -m swebench_docker.evaluate_instance

# We are current in another directory, but we have to add the path to the python path
# So that the module can be found
export PYTHONPATH=$PYTHONPATH:/swebench_docker
# Run the evaluate_instance.py script with the provided arguments
python -m swebench_docker.evaluate_instance
