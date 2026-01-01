def add_argmax_output_constraints(m, outputs, target_index):
    """
    Add constraints to check if output[target_index] is NOT the maximum.

    Args:
        m: Gurobi model
        outputs: list of output variables
        target_index: index that should be the argmax
    """
    for i in range(len(outputs)):
        if i != target_index:
            m.addConstr(outputs[target_index] >= outputs[i],
                        name=f"condition_target{target_index}_vs_{i}")
