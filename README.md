Super fast color transfer between images
==============
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jqueguiner/color_transfer.git/jupyter?filepath=example.ipynb)


The <code>color_transfer</code> package is an OpenCV and Python implementation based (loosely) on [*Color Transfer between Images*](http://www.thegooch.org/Publications/PDFs/ColorTransfer.pdf) [Reinhard et al., 2001] The algorithm itself is extremely efficient (much faster than histogram based methods), requiring only the mean and standard deviation of pixel intensities for each channel in the L\*a\*b\* color space.

For more information, along with a detailed code review, [take a look at this post on my blog](http://www.pyimagesearch.com/2014/06/30/super-fast-color-transfer-images/).

# Requirements
- OpenCV
- NumPy

#Install
To install, make sure you have installed NumPy and compiled OpenCV with Python bindings enabled.

From there, there easiest way to install is via pip:

<code>$ pip install color_transfer</code>

# Examples
Below are some examples showing how to run the <code>example.py</code> demo and the associated color transfers between images.

<code>$ python example.py --source images/autumn.jpg --target images/fallingwater.jpg</code>
![Autumn and Fallingwater screenshot](docs/images/autumn_fallingwater.png?raw=true)

<code>$ python example.py --source images/woods.jpg --target images/storm.jpg</code>
![Woods and Storm screenshot](docs/images/woods_storm.png?raw=true)

<code>$ python example.py --source images/ocean_sunset.jpg --target images/ocean_day.jpg</code>
![Sunset and Ocean screenshot](docs/images/sunset_ocean.png?raw=true)


# Docker for Notebook

You can build and run the docker using the following process:

## Cloning
```console
git clone https://github.com/jrosebr1/color_transfer.git color_transfer
```

## Building Docker
```console
cd color_transfer && docker build -t color_transfer -f Dockerfile .
```

## Running Docker
```console
echo "http://$(curl ifconfig.io):8888" && docker run --env NOTEBOOK_PASSWORD="pass123" -p 8888:8888 -it color_transfer
```

# Docker for API

You can build and run the docker using the following process:

## Cloning
```console
git clone https://github.com/jrosebr1/color_transfer.git color_transfer
```

## Building Docker
```console
cd color_transfer && docker build -t color_transfer_api -f Dockerfile-api .
```

## Running Docker
```console
echo "http://$(curl ifconfig.io):5000" && docker run -p 5000:5000 -d color_transfer_api
```

## Calling the API for image processing
```console
curl -X POST "http://MY_SUPER_API_IP:5000/process" -H "accept: image/png" -H "Content-Type: application/json" -d '{"source_url":"https://i.ibb.co/q9cYCzK/source.jpg", "target_url": "https://i.ibb.co/HB4bNVy/target.jpg"} --output my_super_transfered_image.png
```
