# Human in the Loop and Flatland

# Problem
Assuming that Flatland exists with an AI-supported scheduling agent, we began to lay the foundation for the question of how we can make the Flatland data more accessible to people and how people can communicate with the AI-supported scheduling agent so that it knows the optimization goals, or how people can interact with the AI due proactive or reactive control the AI agents behavior. 

The interaction should be possible globally, or at the agent level. This means that on the one hand we want to communicate the global goals to the system or adapt them dynamically, but we also want to give each agent a strategy that differs from the global one. This means that different goals can be pursued at different levels or, depending on the importance of a move, which goals or priorities it should pursue.

We were particularly concerned with the question of how the information from Flatland can be made accessible to people so that they can get an overview very quickly and easily. In addition, we tried to create a first version in the first draft that would reduce the cognitive load on people. We were also inspired by the idea of ​​hypervision.

We also thought about how everything could be arranged. On the one hand, the system should make suggestions to the user as possible scenarios and, on the other hand, the user should be able to arrange a single move directly.
For this purpose, we built a UI prototype that visually represents the essential elements and explains the different views.

# Results 

<img width="640" alt="Interface 0 31" src="https://github.com/user-attachments/assets/61719a6f-650e-4c18-8868-7bb28ce7cc6f">
<img width="640" alt="Interface 0 32" src="https://github.com/user-attachments/assets/00c2708e-2dbd-4abf-bde7-7544e17fc13f">


# Next steps 
- Implement a simple Flatland Agent (such as e.g. [shortest_path_deadlock_avoidance_policy](https://github.com/aiAdrian/flatland_solver_policy/tree/main/policy/heuristic_policy/shortest_path_deadlock_avoidance_policy), ... ) and build the break through
- Enhance the AI ​​or introduce real AI (OR, ..., [MAPF](https://mapf.info/index.php/Main/News), ... MARL)
- Implement the proposed Design (build a prototyp) - it might can be integrated into an existing framework such as interactiveAI from SystemX
- Test with Human and find weaks and strongs
- Adapt the findings

# Source of inspiration

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



