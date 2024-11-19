# Next Graph-Based Observation

## Objectives

1. ✅ Verify tree obs is collapsed (not intermedate cells) &rarr; at cell level
2. 🔲 :black_square_button:Re-create - integrate Alberto's solution into Flatland core
    * pruned tree in-memory, list of features:

```text
Class for storing the node features

Each node information is composed of 14 features.

:param dist_own_target_encountered: if own target lies on the explored branch the current distance
                                    from the original agent in number of cells is stored.
:param dist_other_target_encountered: if another agents target is detected the distance in number of cells
                                    from the agents current location is stored
:param dist_other_agent_encountered: if another agent is detected the distance in number of cells
                                    from current agent position is stored.
:param dist_potential_conflict: Other agent predicts to pass along this cell at the same time as the agent,
                                we store the distance in number of cells from current agent position.
                                0 = No other agent reserve the same cell at similar time
:param idx_conflicting_agent: Idx of the agent creating the potential conflict.
:param cell_of_conflict: Tuple holding the coordinate of the expected conflict
:param dist_other_agent_to_conflict: Manhattan distance of the conflicting agent to the cell of conflict.
:param clashing_agent_has_alternative: Indicates whether the conflicting agent has or not an alternative.
                                        If not other possibilities then -> Certain conflict(?).
:param ca_expected_delay_for_alternative_path: Stores the lowest possible delay following the 2nd shortest path.
:param conflict_on_junction_with_multiple_path: Indicates whether the conflict will take place on a junction and
                                                the selected train has a free path to follow.
                                                Hence, not going to be blocked nor dead.
:param expected_delay_for_2nd_best_path: Indicates the delay for resolving the conflict on the junction
:param dist_unusable_switch: if a not usable switch (for agent) is detected we store the distance.
:param unusable_switch_usable_for_ca: Indicates whether the unusable switch can be used by the conflicting agent.
:param unusable_switch_delay_for_ca: Indicates the expected delay for the conflicting agent to use the switch.
:param dist_to_next_branch: the distance in number of cells to the next branching  (current node)
:param dist_min_to_target: minimum distance from node to the agent's target given the direction of the agent
                            if this path is chosen
:param num_agents_same_direction: number of agents present same direction
:param num_agents_opposite_direction: number of agents present other direction than myself
                                      (so potential conflict)
:param num_agents_malfunctioning: number of time steps the observed agent remains blocked
:param speed_min_fractional: slowest observed speed of an agent in same direction. (1 if no agent is observed)
:param num_agents_ready_to_depart: number of agents ready to depart but no yet active on the node.
:param idx_deadlock_trains:  idx of deadlocked trains.
:param childs: childs node that can be reached from the parent.

Missing/padding nodes are filled in with -inf (truncated).
Missing values in present node are filled in with +inf (truncated).
```

![Graph Observation](GraphObs.png)

3. 🔲 What feature can we add to augment the information to conflict in Alberto's solution?
    * n-shortest: weighted
    * further ideas?

## Next steps

* Training environment to test out improvements? In Flatland or de-centralized?
* Tree-LSTM