# Flatland Workshop 2024

Shared codespace for [Flatland Workshop and Symposium 2024](https://flatland-association.org/events/flatland-workshop-and-symposium-2024).

## Topics of interest for the Flatland Workshop

* [Next Flatland Environment](next-flatland/README.md)
* [Human in the Loop and Flatland](human-in-the-loop/README.md)
* [Enhancements to Tree Observation](next-graph-based-observation/README.md)
* [Real-World Scenarios in FLATLAND](real-world-scenarios/README.md)

### Backlog
* [Complex schedules in Flatland using Netzgrafikeditor](_backlog/complex-schedules-using-netzgrafikeditor/README.md)
* [Real-world infrastructures for Flatland](_backlog/real-world-infrastructures/README.md)
* [Interactive user interface design for real-time simulations with Flatland](_backlog/interactive-user-interface-design/README.md)
* [Benchmarking scenarios](_backlog/benchmarking-scenarios/README.md)
* [Flatland baselines](_backlog/flatland-baselines/README.md)
* [Flatland next rail env generator](_backlog/next-rail-env-generator/README.md)


## Publications - What was done before

An overview: 
- [Research results using Flatland](https://github.com/aiAdrian/flatland_railway_extension/blob/master/publications/flatland_research.MD)
- [Youtube: Video recordings of lectures/talks](https://github.com/aiAdrian/flatland_railway_extension/blob/master/publications/youtube_flatland.MD)


Very interesting with potentially big impact on Flatland 4.0: 
-  Ricardo Gama, Daniel Fuertes, Carlos R. del-Blanco, Hugo L. Fernandes -
 [**Multi-Agent Environments for  Vehicle Routing Problems**](
 https://arxiv.org/abs/2411.14411) -
 arXiv:2411.14411 -  :boom: 21 Nov 2024



## TL;DR;

Use local setup (preferred) or, alternatively, Colab approach.

### Local Setup

Pre-requisite: [Install Miniconda](https://docs.anaconda.com/miniconda/miniconda-install/) (or use any XXXconda).

```shell
conda create -n flatland python=3.10.0
conda activate flatland


git clone https://github.com/flatland-association/flatland-rl.git
cd flatland-rl
python -m pip install -r requirements.txt -r requirements-dev.txt

export PYTHONPATH=.
jupyter notebook

# open browser http://127.0.0.1:8888/notebooks/notebooks/flatland_animate.ipynb
```

#### Troubleshooting

* `Launching Jupyter Notebook on localhost results in '[Errno 49] Can't assign requested address'`
  &rarr; https://stackoverflow.com/questions/60271829/launching-jupyter-notebook-on-localhost-results-in-errno-49-cant-assign-requ

### Colab

Alternatively, use the provided [simple_flatland_rl.ipynb on Colab](https://colab.research.google.com/drive/1qtwB4xyX4njmtMDScEBm-iIH5VyYpuWG?usp=sharing)
