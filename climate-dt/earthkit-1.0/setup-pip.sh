envname=earthkit-1.0-pip

# create venv (Python 3.10+)​
python3 -m venv $envname

# activate (macOS/Linux)​
source $envname/bin/activate

# install dependencies​
pip install -r requirements.txt

# register Jupyter kernel​
python3 -m ipykernel install --user --name=$envname