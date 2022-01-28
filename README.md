# DegFairGNN

# Generalized Degree Fairness-Centric Graph Neural Networks
We provide the implementaion of DegFairGNN model.

The repository is organised as follows:
- data/: contains 3 benchmark datasets: squirrel, chameleon, emnlp
- models/: contains our model. 
- layers/: contains component layers for our model.  


## Requirements
To install required packages
- pip3 install -r requirements.txt

## Running experiments

To run chameleon:
- python3 main.py --dataset=chameleon --dim=32 --omega=1 --w_f=1e-3

To run squirrel:
- python3 main.py --dataset=squirrel --dim=32 --gpu=1 --omega=0.01 

To run emnlp:
- python3 main.py --dataset=emnlp --dim=16 --omega=0.001 --w_f=0.01 
