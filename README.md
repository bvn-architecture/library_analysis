# BVN Library analysis

Prompted by a discussion of how diverse the BVN library is, this is a quick attempt to answer that question.

The `analysis.py` file does a somewhat odd job of loading, cleaning and taking a brief look at the data. There's still a _lot_ left to do.

![A graph showing how many books there are for each subject](plots/subjects.png)

A graph showing how many books there are for each subject. Note: each book can have many subjects.

## How to get started with this repo

Once you've cloned this repo, from inside the repo folder, run these commands:   (You should be able to just paste it in as a block.)

```
python -m venv --copies lib-env
lib-env\\Scripts\\activate.bat
echo 🚪
python -m pip install --upgrade pip
python -m pip install pip-tools
pip-compile requirements.in
echo 🚀
pip install -r requirements.txt
git init,
echo 🍟🍟🍟
```

Then jump into analysis.py and go sick. 

