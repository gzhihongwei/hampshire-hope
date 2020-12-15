# Intructions to Run `heatmap.ipynb`
## Downloading Jupyter and Prerequisites

1. Install `python` for your platform, ideally version `> 3.x`. The link for downloading `python` is [here](https://www.python.org/downloads/).
2. Make sure that `python` and `pip` are on your system path. You can check this by running `python --version` and `pip --version` in your terminal. If they are both on your system path, then there will be no errors and the version numbers of the programs will be printed.
3. To install Jupyter Notebook, run `pip install notebook` in your terminal. You should be seeing progress bars of the install.
4. In order to see if Jupyter Notebook was successfully installed, run `jupyter notebook` in your terminal. If successful, the terminal will prompt you to copy a link like `http://localhost:8888/?token=SESSION_TOKEN` into your browser or will automatically open a new tab. If this doesn't happen, redo step 3.

## Installing `gmaps`

1. Enable `ipywidgets` widgets extension by running `jupyter nbextension enable --py --sys-prefix widgetsnbextension` in your terminal
2. Then, install `gmaps` by running the command `pip install gmaps` in your terminal.
3. Finally, load the extension into Jupyter with `jupyter nbextension enable --py --sys-prefix gmaps`. 

## Enabling Google's APIs

In order to query from the Distance Matrix API and to generate a heatmap, you must have a valid project on [Google Cloud Platform](https://console.cloud.google.com/home/). In order to create a project, navigate to the dropdown next to "Google Cloud Platform" on the top navigation bar. Afterwards, click on the three lines on the top navigation bar to reveal the sidebar. From here, click on "APIs & Services". There should be a blue "+" sign saying to "ENABLE APIS AND SERVICES". Click on that and search up "Distance Matrix" and "Maps JavaScript". Enable these two APIs, otherwise you will encounter errors when trying to run the notebook.

Navigate to the `google` directory using the `cd` command in your terminal. After navigating there, run `jupyter notebook` and you should be able to navigate to `heatmap.ipynb` from there. That should be everything. If something is not working, email <georgewei369@yahoo.com> (or just slack).