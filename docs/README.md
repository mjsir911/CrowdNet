#Crowd-Net

##Testing
right now all you need to do to test how it works is:

# Crowd-Net

The wonderfully generic (hopefully)crowd-sourced neural network
(the crowd sourced-ness is basically a pipe dream right now)
This is mostly a learning experience for me, many many more efficient alternatives exist out [there](https://github.com/tensorflow/tensorflow)
Tensorflow actually provides really nice neural network stuff [here](http://playground.tensorflow.org)


## Getting Started

If you want to experiment around, simply open up a python interpretive shell inside the [src](/src)

    import net
    network = net.Net(learning_rate, [hidden neurons in 1 layer])
    network.train([inputs], [outputs]) # must know number of input and output neurons in code
    # or
    network.mass_train(iterations, [[inputs], [outputs]])

The network is dumb as rocks but it can work logic gates pretty well!

### Prerequisities

[Python3](https://www.python.org/download/releases/3.0/)

### Installing

Installation is not particularly hard, due to the small nature of this project

To get a working development environment setup, simply git clone this repository into a directory of each choice

  git clone

next navigate to specified directory

    cd mydir

You should see the contents of the repository's filesystem

## Running the tests

To run the automated test, navigate to the test directory and run the threeXNOR.py file

    python3 threeXNOR.py

or

    ./threeXNOR.py

## Deployment

Learning takes a bit of time(obviously)
Bigger neural networks take insane amounts of ram

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
* [Mat Mazur](https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/) for understanding

