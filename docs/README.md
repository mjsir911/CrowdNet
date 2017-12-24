# Crowd-Net

The wonderfully generic (hopefully)crowd-sourced neural network
(The crowd-sourced net has arisen in the form of p2p and is currently working on my lab!)
This is mostly a learning experience for me, many many more efficient alternatives exist out [there](https://github.com/tensorflow/tensorflow)
Tensorflow actually provides a really nice neural network representation [here](http://playground.tensorflow.org)


## Getting Started

If you want to experiment around, simply open up a python interpretive shell inside the [src](/src)

    import net
    network = net.Net(learning_rate, num_input, [hidden neurons], num_output)
    network.train([inputs], [outputs]) # must know number of input and output neurons in code
    # or
    network.mass_train([[inputs], [outputs]], iterations)
    # or
    network.function_train(func, iterations)

The network is dumb as rocks but it can work logic gates(100%) & 4 bit division(93%) pretty well!

### Prerequisities

_**[Python3](https://www.python.org/download/releases/3.0/)**_

virtualenv

    pip3 install virtualenv

### Installing

Installation is not particularly hard, due to the small nature of this project

To get a working development environment setup, simply git clone this repository into a directory of each choice

    git clone

next navigate to specified directory

    cd CrowdNet

You should see the contents of the repository's filesystem

Then run virtualenv to initialize a virtual environment in the folder ``venv``

    virtualenv venv

And turn on the virtual environment

    source venv/bin/activate

Finally, install the required modules

    pip3 install -r requirements.txt

### Note
To get out of a virtualenv:
    
    deactivate

## Running the tests

To run the automated test, navigate to the test directory: ``cd test`` and run the functions.py file

    python3 shallow.py

or

    ./shallow.py

## Deployment

Learning takes a bit of time(obviously)
Bigger neural networks take insane amounts of ram

### P2P module
Due to physical limitations of a single computer, I have developed a peer to peer cluster network that allows the neural network to distribute the processing power equally amongst all peers.

To initialize this, see documentation on the internet.py module.

## Built With

* [vim](http://www.vim.org/)
* lots of googling

## Contributing

Please read [CONTRIBUTING.md](/docs/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](/.tags).

## Authors

* **Marco Sirabella** - *Initial work* - [mjsir911](https://github.com/mjsir911)

See also the list of [contributors](/docs/CONTRIBUTORS.md) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](/docs/LICENSE.md) file for details

## Acknowledgments

* [Tensorflow](https://github.com/tensorflow) for inspiration
* [Mat Mazur](https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/) for help understanding

