# strw-ra-scripts

This is the README document for strw-ra-scripts, a collection of scripts used for the 2026 **_Radio Astronomy_** lecture hosted at [**Leiden Observatory**](https://local.strw.leidenuniv.nl/).

**Dated:** 2026-September-16

## index

WIP

## preparations

We start with creating and activating a `conda` environment with `python` version 3.14:

```sh
cd strw-ra-scripts
conda create -n strw-ra-py314 python=3.14
conda activate strw-ra-py314
```

For the other packages, we install via `conda-forge` channels:

```sh
conda install -c conda-forge numpy scipy astropy matplotlib tqdm healpy aplpy python-casacore cython pyfftw numba h5py
```

An exception occurs with `lofarantpos`, this can then be installed via `pip`:

```sh
pip install lofarantpos
```

At this time, we can list the packages installed with `conda` into a `env.yml` file via:

```sh
conda env export > env.yml
```

And, alternatively, top level packages handled by `conda` can be listed via:

```sh
conda env export --from-history > env.yml
```

We write the `pip` installed packages into `env.yml` afterwards. This can be done through `fish` shell via:

```sh
{
    conda env export --from-history | grep -v "^prefix:";
    echo "  - pip:";
    pip list --format=freeze | sed 's/^/      - /';
} > env.yml
```

This `env.yml` file is useful for recreating an identical environment via:

```sh
conda create -f env.yml -n name-for-new-env
```

## global packages

Some packages are better off being system-wide for preference:

```sh
sudo pacman -S gnuradio gnuradio-osmosdr gnuradio-companion hackrf jupyterlab
```

## notebooks

We install and enable `git-lfs`. On Arch-based systems, we can install system-wide via:

```sh
sudo pacman -S git-lfs
git lfs install
```

The notebooks associated can now be cloned via:

```sh
git clone https://github.com/brentjens/radio-astronomy-by-notebooks.git
```

We optionally unlink this remote with:

```sh
rm -rf ./radio-astronomy-by-notebooks/.git/
```

We then optionally add this notebook directory to ignore with a `.gitignore` file:

```sh
cd strw-ra-scripts
echo "radio-astronomy-by-notebooks/" >> .gitignore
```

## tree

```sh
.
├── data
├── env.yml
├── fig
├── flowchart
├── LICENSE
├── radio-astronomy-by-notebooks
├── README.md
└── scripts
```
