# Demo Instructions

## Building the Docker image:

To be able to use the demo, do the following to have a working docker image.  This command will be ran in the demo directory to build the Groundr Docker image using the provided Dockerfile.

    docker build scripts -t groundr

If you would like to test the Docker image, the following command can be run, replacing all instances of 5000 with whatever port you want the Docker image to use.

    docker run -p 5000:5000 -it groundr /root/start.sh 0.0.0.0 5000

## Launching the demo:

Launch demo.py in this folder, giving it an IP and port to host on if needed:

    python demo.py <ip> <port>

The defaults are IP 0.0.0.0 and port 80, which you can connect to by either entering localhost into your browser, or the IP of the server.
