from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
import random
from typing import Dict, List, Set, Any
from gen_env import (
    Agent,
    Arbiter,
    Effect,
    Agent,
    GenEnvSimulation,
    Relation,
    Resource,
    SystemState,
    Propagator,
)
import networkx as nx
import matplotlib.pyplot as plt


@dataclass()
class RailResource(Resource):
    id: int
    valid_routes: dict[Resource, list[Resource]]
    x: int
    y: int

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, RailResource):
            return self.id == other.id
        return False


@dataclass()
class MoveAction:
    agent: Agent
    destination: RailResource


class RailNetwork:
    def __init__(self):
        self.coordinates = [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (2, 1),
            (3, 1),
        ]
        self.resources = [
            RailResource(id=i, valid_routes={}, x=coord[0], y=coord[1])
            for i, coord in enumerate(self.coordinates)
        ]
        self.relations = []
        self._initialize_routes()
        self._initialize_relations()

    def _initialize_routes(self):
        """
             6 7
             - - 
           /     \ 
        - -  - -  - -
        0 1  2 3  4 5
        """
        # Define valid routes for straight line 0->1->2->3->4->5
        for i in range(1,4):
            self.resources[i].valid_routes[self.resources[i-1]] = [self.resources[i]]
            self.resources[i+1].valid_routes[self.resources[i+1]] = [self.resources[i]]
        
        self.resources[0].valid_routes[self.resources[1]] = [self.resources[1]]
        self.resources[0].valid_routes[self.resources[0]] = [self.resources[1]]
        self.resources[5].valid_routes[self.resources[4]] = [self.resources[4]]
        self.resources[5].valid_routes[self.resources[5]] = [self.resources[4]]

        # Define valid routes for straight line 6->7
        self.resources[6].valid_routes[self.resources[1]] = [self.resources[7]]
        self.resources[7].valid_routes[self.resources[4]] = [self.resources[6]]
        self.resources[6].valid_routes[self.resources[7]] = [self.resources[1]]
        self.resources[7].valid_routes[self.resources[6]] = [self.resources[4]]

        # Add switch connections
        # At resource 1 (connecting to 6)
        self.resources[1].valid_routes[self.resources[0]] = [self.resources[2], self.resources[6]]
        self.resources[1].valid_routes[self.resources[2]] = [self.resources[0]]
        self.resources[1].valid_routes[self.resources[6]] = [self.resources[0]]

        # At resource 4 (connecting to 7)
        self.resources[4].valid_routes[self.resources[5]] = [self.resources[3], self.resources[7]]
        self.resources[4].valid_routes[self.resources[3]] = [self.resources[5]]
        self.resources[4].valid_routes[self.resources[7]] = [self.resources[5]]

    def _initialize_relations(self):
        for resource in self.resources:
            for from_resource, to_resources in resource.valid_routes.items():
                for to_resource in to_resources:
                    relation = Relation(
                        from_entity=from_resource, to_entity=to_resource
                    )
                    self.relations.append(relation)

    def get_resources(self):
        return self.resources

    def get_relations(self):
        return self.relations

    def plot_network(self):
        G = nx.DiGraph()
        for resource in self.resources:
            G.add_node(resource.id, pos=(resource.x, resource.y))
            for dest in resource.valid_routes.get(resource, []):
                G.add_edge(resource.id, dest.id)

        pos = nx.get_node_attributes(G, "pos")
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=700,
            node_color="skyblue",
            font_size=10,
            font_weight="bold",
        )
        plt.show()


@dataclass
class RandomPolicy:
    def propose_next_position(
        self, current_position: RailResource, previous_position: RailResource
    ) -> RailResource:
        possible_resources = list(current_position.valid_routes[current_position])
        if previous_position in possible_resources:
            possible_resources.remove(previous_position)
        if not possible_resources:
            return None
        return random.choice(possible_resources)


@dataclass
class TrainAgent(Agent):
    id: int
    previous_position: RailResource

    def act(self):
        next_position = self.previous_position.valid_routes[self.previous_position][0]
        return MoveAction(self, next_position)


@dataclass()
class AddAndRemoveRelation(Effect):
    add_relation: Relation
    remove_relation: Relation


@dataclass()
class AddRelation(Effect):
    relation: Relation


@dataclass()
class RemoveRelation(Effect):
    relation: Relation


class RailState(SystemState[Agent, Relation, RailResource]):
    def __init__(
        self,
        agents_starting_resources: list[Resource],
    ):
        rail_network = RailNetwork()
        self.agents = [TrainAgent(id=i) for i in range(len(agents_starting_resources))]
        self.relations = rail_network.get_relations()
        self.resources = rail_network.get_resources()
        self.relations.extend(
            [
                Relation(agent, resource)
                for agent, resource in zip(self.agents, agents_starting_resources)
            ]
        )

    def pull_actions(self):
        """Pull actions from all agents"""
        actions = []
        for agent in self.agents:
            actions.append(agent.act())
        return actions

    def actions_to_effects(self, actions: list[MoveAction]) -> list[Effect]:
        effects = []
        for action in actions:
            effects.append(
                AddAndRemoveRelation(
                    remove_relation=Relation(
                        action.agent, action.agent.previous_position
                    ),
                    add_relation=Relation(action.agent, action.destination),
                )
            )
        return effects

    def actionsToEffects(self, actions) -> List[Effect]:
        """Convert agent actions to effects"""
        effects = []
        for action in actions:
            if action is not None:  # Skip if agent has no valid move
                if isinstance(action, AddAndRemoveRelation):
                    effects.append(action)
        return effects

    def relations_by_entity(self) -> Dict[Any, int]:
        """Count relations per entity"""
        counts = defaultdict(int)
        for relation in self.relations:
            counts[relation.to_entity] += 0
        return counts

    def add_entity(self, entity: Agent):
        self.agents.append(entity)

    def add_relation(self, from_entity: Agent, to_entity: Agent):
        self.relations.append(Relation(from_entity, to_entity))

    def remove_relation(self, from_entity: Agent, to_entity: Agent):
        self.relations.remove(Relation(from_entity, to_entity))

    def add_resource(self, resource: RailResource):
        self.resources.append(resource)


@dataclass()
class RailArbiter(Arbiter):
    rail_state: RailState

    def check_rules(self, effects: list[Effect]) -> list[Effect]:
        valid_effects: list[Effect] = []
        for effect in effects:
            if isinstance(effect, AddAndRemoveRelation):
                agent = effect.add_relation.from_entity
                resource_to_add = effect.add_relation.to_entity
                resource_to_remove = effect.remove_relation.to_entity

                # occupation check
                valid_occupation = (
                    self.rail_state.relations_by_entity()[resource_to_add] == 0
                )
                if not valid_occupation:
                    print("agent {} stopped at occupied resource".format(agent.id))
                    continue

                # transition check
                valid_transition = (
                    resource_to_add.id
                    in resource_to_remove.valid_routes[agent.previous_position]
                )
                if valid_transition:
                    valid_effects.extend(
                        [
                            AddRelation(effect.add_relation),
                            RemoveRelation(effect.remove_relation),
                        ]
                    )
                print("agent {} stopped at invalid transition {} -> {}".format(agent.id, agent.previous_position.id,agent.current_position.id))

        return valid_effects


@dataclass
class RailPropagator(Propagator):
    rail_state: RailState

    def propagate(self, effects: List[Effect]) -> Dict[Agent, bool]:
        """
        Propagates effects by:
        - Validating effect types
        - Updating agent positions
        - Updating rail state relations
        - Tracking completion status
        """
        dones = {}

        for effect in effects:
            if isinstance(effect, AddAndRemoveRelation):
                agent = effect.add_relation.from_entity
                next_position = effect.add_relation.to_entity
                current_position = effect.remove_relation.to_entity

                # Update agent's position
                agent.previous_position = current_position
                agent.current_position = next_position

                # Update relations in rail state
                self.rail_state.remove_relation(agent, current_position)
                self.rail_state.add_relation(agent, next_position)

                # Track if agent has completed its objective
                dones[agent] = False  # Could be updated based on objectives

        return dones


# Example usage
if __name__ == "__main__":
    rail_network = RailNetwork()
    initial_position = [rail_network.resources[0], rail_network.resources[5]]

    # Create agents with random policy
    agents = [
        TrainAgent(
            id=i,
            current_position=initial_position[i],
            previous_position=initial_position[i],
            policy=RandomPolicy()
        ) for i in range(2)
    ]

    # Setup simulation components
    rail_state = RailState(
        agents=agents,
        relations=rail_network.relations,
        resources=rail_network.resources,
    )
    rail_arbiter = RailArbiter(rail_state=rail_state)
    rail_propagator = RailPropagator(rail_state=rail_state)

    # Create and run simulation
    simulation = GenEnvSimulation(
        propagator=rail_propagator, state=rail_state, arbiter=rail_arbiter
    )

    simulation.run()
