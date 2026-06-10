envname=earthkit-1.0-conda
conda create -n $envname -c conda-forge -y python=3.10
conda env update -n $envname -f environment.yml

# load conda's shell functions so `conda activate` works in a script
eval "$(conda shell.bash hook)"
conda activate $envname

# register Jupyter kernel
python3 -m ipykernel install --user --name=$envname
