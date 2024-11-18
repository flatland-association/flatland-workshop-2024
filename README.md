# Flatland Workshop 2024

Shared codespace for [Flatland Workshop and Symposium 2024](https://flatland-association.org/events/flatland-workshop-and-symposium-2024).

## Topics of interest for the Flatland Workshop

* [Next Flatland Environment](next-flatland/README.md)
* [Complex schedules in Flatland using Netzgrafikeditor](complex-schedules-using-netzgrafikeditor/README.md)
* [Real-world infrastructures for Flatland](real-world-infrastructures/README.md)
* [Interactive user interface design for real-time simulations with Flatland](interactive-user-interface-design/README.md)
* [Human in the Loop and Flatland](human-in-the-loop/README.md)
* [Benchmarking scenarios](benchmarking-scenarios/README.md)
* [Flatland baselines](flatland-baselines/README.md)
* [Flatland next rail env generator](next-rail-env-generator/README.md)

## TL;DR;

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


### Troubleshooting
* `Launching Jupyter Notebook on localhost results in '[Errno 49] Can't assign requested address'` &rarr; https://stackoverflow.com/questions/60271829/launching-jupyter-notebook-on-localhost-results-in-errno-49-cant-assign-requ