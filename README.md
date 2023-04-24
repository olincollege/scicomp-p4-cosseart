# Cosserat Rod Simulation
This project contains a simple elastic rod simulation based on an implementation of the classical continuous-form Cosserat rod equations.

![Beam loading gif](https://im4.ezgif.com/tmp/ezgif-4-3587016f68.gif)

## Model

System Diagram | Model Equations
- | - 
![System diagram](https://media.discordapp.net/attachments/421939066930462723/1100061734506602637/image.png) | ![Model equations](https://media.discordapp.net/attachments/421939066930462723/1100061822423408772/image.png)

Our project implements the classical continuous-form Cosserat rod equations as taken from Equation 6 of Rucker and Webster's 2011 paper ["Statics and Dynamics of Continuum Robots with General Tendon Rouding and External Loading"](https://doi.org/10.1109/TRO.2011.2160469). These equations formulate the linear and angular force balances along the rod, which can then be solved for various loading scenarios as boundary value problems along the rod.

After our single rod model implementation is validated, a stretch goal will be to incorporate multiple rods that can be constrained together by various joint types. For this we will use the reaction-force based joint formulation of [Zhang, Chan, Parthasarthy, and Gazzola's 2019 paper "Modeling and Simulation of Complex Dynamic Musculoskeletal Architectures"](https://www.cosseratrods.org/publications/pubs/2019_NatComm.pdf). 

### Model implementation progress
- [x] Single cantilevered subject to point load
- [] Helical buckling for a rod that is compressed and twisted
- [] Fixed joints between two rods along thier length

## Validation
We first validate our single rod model implementation using the tests from [Gazzola et al's 2017 paper "Forward and Inverse Problems in the Mechanics of Soft Filaments"](https://mattia-lab.com/wp-content/uploads/2018/06/Gazzola_RSOS_2018.pdf). Then, if we have time, we will qualitatively and visually evaluate our joint implmentation.

### Model validation progress
- [] Single cantilevered subject to point load
- [] Helical buckling for a rod that is compressed and twisted
- [] Fixed joints between two rods along thier length

# Installation
## Dependencies
This project was developed on Python 3.8.10. The specific packages and their versions used for this project are listed in `requirements.txt`.

To install all dependencies, pip install from `requirements.txt` as such:
``` bash
$ python3 -m pip install -r requirements.txt
```

This project uses Streamlit to run the main app in an interactive format. Start the main Streamlit app with the following command:
```bash
$ streamlit run main.py
```

You should be off to the races!