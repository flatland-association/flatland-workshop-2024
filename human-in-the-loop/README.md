# Human in the Loop and Flatland

## Team 
- [Michaela Hildebrandt](https://michaelahildebrandt.com/)
- [Adrian Egli](https://www.linkedin.com/in/adrian-egli-733a9544/)
- [Daniel Boos](https://www.linkedin.com/in/boosdaniel)



### Results: AI Assistant System for Human Dispatchers in Railway Operations
[Flatland Train Dispatcher Interface 20241206.pdf](https://github.com/user-attachments/files/18090579/Flatland.Train.Dispatcher.Interface.20241206.pdf)

[Flatland Train Dispatcher Interface 20250514.pdf](https://github.com/user-attachments/files/20865149/Flatland.Train.Dispatcher.Interface.20250514.pdf)


---



## What we did
We dealt with the question of how the information from Flatland can be made accessible to humans dispachters so that they can quickly get an overview of what is happening in the simulated world (Flatland). Additionally, we tried to create a (conceptual) prototype with the goal to identify the key components for visualisation (explaination) and for interaction (exploration, human-ai-cooperation). 

We also thought about how everything could be arranged in the frontend (user interface). On the one hand, the system should present possible scenarios as suggestions to the user, and on the other hand, the user should be able to communicate the goals to the system (globally or locally, i.e., it must also be possible to influence or control the optimization goals for a very specific, individual train directly or indirectly).

For this purpose, we created a UI prototype that visually represents the essential elements and explains the different views.

## Solution idea

### Prerequisites
To prototypically implement the ideas found in the field of user interaction, user interface, and human-machine interaction, some basic prerequisites must be met:

- A simulation environment exists that allows disposition decisions (actions) to be made and which are then applied or implemented by the system, and the temporal course (including the impact of the actions) can be simulated through simulation.
- A disposition method exists that can make suggestions or directly execute a chain of actions with the simulation.
- A disposition method exists that can be controlled by optimization goals, which are currently of importance, e.g., minimizing train delays.
- A disposition method exists that can be interactively controlled by settings, determining which actions can be taken, including changing routes, stopping vehicles (agents waiting, etc.).

### Assumptions
Assuming that Simulationsoftware (Flatland) exists with an AI-supported planning agent, we began laying the foundation for the question of how we can make Flatland data more accessible to humans and how humans can communicate with the AI-supported planning agent so that it knows the optimization goals or how humans can influence the behavior of the AI agents through proactive or reactive control.

### Goals

- **User should be able to control the dispatching goals globally (for all agents) or locally for one single agent (override global setting).**
  The interaction should be possible globally or at the agent level. This means that, on the one hand, we want to communicate the global goals to the system or dynamically adjust them, but also give each agent a strategy 
  that differs from the global one. This means that different goals can be pursued at different levels or, depending on the importance of a train, which goals or priorities should be pursued for a specific train.

### Requirements

- **User should be able to select one single agent and choose dispatching action for this single train separately.**

- **User should be able to pre-simulate computer generated (AI generated) scenarios.**
  The user can choose one scenario (suggestion) which contains at least one dispatching action up to many, which will be done in a given order and at a clearly defined time from now to the near future.
  The user should be able to override an action in the scenario, thus the user should see the actions in a temporally ordered list where each action will be very clearly visualized and defined.

- **The system should have the option to switch from full information visualisation and automatically filtered information where only relevant information is visualized (displayed).**
  This means that when the system runs in full information visualization mode, the user gets maximum details displayed. When the system runs in automatic filtering mode, the visualization/displaying of the information is 
  selective, and the system will only show what is relevant to the current ongoing decision (support).

- **The system should be able to notify the user when some unexpected events occurs.**
- **The system should provide a map like flatland rendering/visualisation which is realted to the ["Streckenspiegel"](https://fahrweg.dbnetze.com/resource/blob/1359516/86b02d132898b0532d085671bc11578a/kundenpraesentation_leidis_nk_basisversion-data.pdf)**
- **The system should have [graphic timetable / time-distance-visualisation](https://github.com/SchweizerischeBundesbahnen/netzgrafik-editor-frontend/blob/main/documentation/Graphic_Timetable.md) . User should be able to select a certain "Path/route"**

- **The system should provide the option to switch automatic dispatching on. When enabled, no user-defined action can be taken. The user can only control the dispatching result through the goals.**
- **The system should provide the option to switch off the dispatching suggestions and/or the notification panel**
  


## Results 

PowerPoint Version
[Flatland Train Dispatcher Interface 20241206.pptx](https://github.com/user-attachments/files/18090580/Flatland.Train.Dispatcher.Interface.20241206.pptx)

PDF Version
[Flatland Train Dispatcher Interface 20241206.pdf](https://github.com/user-attachments/files/18090579/Flatland.Train.Dispatcher.Interface.20241206.pdf)


### View: Example 1 

<img width="640" alt="Interface 0 31" src="https://github.com/user-attachments/assets/92cad4f3-6404-44af-8edc-9b45dfa1a598">

### View: Example 2
<img width="640" alt="Interface 0 32" src="https://github.com/user-attachments/assets/00c2708e-2dbd-4abf-bde7-7544e17fc13f">


[Preview in Figma](https://embed.figma.com/proto/2ozvNPInECnQwQOpdHw3L4/Flatland-Dispatcher-Interface?node-id=58-27041&node-type=frame&scaling=contain&content-scaling=fixed&page-id=5%3A2&embed-host=share)


## Next steps 

The ideas of this work have to be 
verified through a functional software which needs to be developed first. The focus is not necessarily on the quality of disposition, nor on the accurate representation of a real railway operation or a railway operation simulation, but rather on the question of how a user interface and a user interaction model between railway (simulation) with AI (disposition algorithmics from the field of OR, heuristics, Multi-Agent Path Finding (MAPF), or Multi-Agent Reinforcement Learning (MARL)) and human interactions can be implemented.


- Implement a simple Flatland Agent (such as e.g. [shortest_path_deadlock_avoidance_policy](https://github.com/aiAdrian/flatland_solver_policy/tree/main/policy/heuristic_policy/shortest_path_deadlock_avoidance_policy), ... ) and build the break through
- Enhance the AI ​​or introduce real AI (OR, ..., [MAPF](https://mapf.info/index.php/Main/News), ... MARL)
- Implement the proposed Design (build a prototyp) - it might can be integrated into an existing framework such as interactiveAI from SystemX
- Test with Human and find weaks and strongs
- Adapt the findings

## Source of inspiration

Rousseau, T., Amokrane, K., Meddeb, M., Renoir, N. , Brunat, M. , Fort, M. , Schott, L. , Mahler, S. , Berthou, H. (2024, April) 
[Cooperation between a human traffic manager and an AI assistant for an improved railway infrastructure resilience.](https://hal.science/hal-04547672/)
In Transport Research Arena (TRA2024).

Richta H.N.
[Automatische Dispositionsassistenz auf Grundlage Produktionsmodell Betrieb ADA-PMB für mehr Pünktlichkeit](https://www.gdsd.statistik.uni-muenchen.de/2023_neu/presentations_speaker/deutsche_bahn_gdsd23.pdf)
German Data Science Days 2023

Marot, A., Rozier, A., Dussartre, M., Crochepierre, L., & Donnot, B. (2022). 
[Towards an AI assistant for power grid operators.](https://www.researchgate.net/publication/363763107_Towards_an_AI_Assistant_for_Power_Grid_Operators)
In HHAI2022: Augmenting Human Intellect (pp. 79-95). IOS Press.

Ammar N. Abbas, Chidera W. Amazu, Joseph Mietkiewicz, Houda Briwa, Andres Alonzo Perez, Gabriele Baldissone, Micaela Demichela, Georgios G. Chasparis, John D. Kelleher, Maria Chiara Leva
[Analyzing Operator States and the Impact of AI-Enhanced Decision Support in Control Rooms: A Human-in-the-Loop Specialized Reinforcement Learning Framework for Intervention Strategies](https://arxiv.org/abs/2402.13219)

Florian Mischek, Nysret Musliu
[Preference Explanation and Decision Support for Multi-Objective Real-World Test Laboratory Scheduling](https://openreview.net/pdf?id=1u95DvUJjE)
ICAPS 2024 Conference

#### Editor (Tracklayout/Topology) - Source of inspiration 
---

![image](https://github.com/user-attachments/assets/c4fdd006-88c5-46c3-bca4-f01543108994)


[iTrain Simulator](https://www.berros.eu/de/itrain/) ![image](https://github.com/user-attachments/assets/8b8c7156-1ebd-48b9-9652-d728b708b6cc)

[Inspiration: iTrain (iCar) Editor](https://www.berros.eu/de/itrain/screenshots.php) ![image](https://github.com/user-attachments/assets/f48af25e-1a17-4d7b-9bd8-1198553a6c98)

[Preference Explanation and Decision Support for Multi-Objective Real-World Test Laboratory Scheduling](https://openreview.net/pdf?id=1u95DvUJjE)
![image](https://github.com/user-attachments/assets/fe41dae7-c395-4ae5-aafc-b960391396cf)




