#Crowd-Net

##Testing
right now all you need to do to test how it works is:

# Crowd-Net

The wonderfully generic (hopefully)crowd-sourced neural network
(the crowd sourced-ness is basically a pipe dream right now)
This is mostly a learning experience for me, many many more efficient alternatives exist out [there](https://github.com/tensorflow/tensorflow)
Tensorflow actually provides really nice neural network stuff [here](http://playground.tensorflow.org)


## Getting Started

If you want to experiment around, simply open up a python interpretive shell inside the (src)[../src]

    import net
    network = net.Net(learning_rate, [hidden neurons in 1 layer])
    network.train([inputs], [outputs]) # must know # of input and output neurons in code
    # or
    network.mass_train(iterations, [[inputs], [outputs]])

The network is dumb as rocks but it can work logic gates pretty well!

### Prerequisities

(Python3)[https://www.python.org/download/releases/3.0/]

### Installing

Installation is not particularly hard, due to the small nature of this project

To get a working development environment setup, simply git clone this repository into a directory of each choice

```
git clone
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* Dropwizard - Bla bla bla
* Maven - Maybe
* Atom - ergaerga

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc

