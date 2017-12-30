# Update
- This has been moved to a fork of the original project, please use the new repo [here](https://github.com/shaggyloris/Device-Monitor-Dashboard)

Simple Device Monitor
===

A python based web app to monitor tcp/icmp status to servers, network gear, or any other device that is pingable in a clean simple interface. It also supports MQTT listening to monitor if MQTT device transmit regularly.

Original design and concept by circa10a can be found [here](https://github.com/circa10a/Device-Monitor-Dashboard).

## Regular Setup
- Clone the git repository
- (recommended) setup a virtual environment with either python2.7 or 3.6
- Install dependencies
- Setup the database: `python manage.py setup`
- Run the web server `python manage.py runserver`
- Server will be available on [hostname]:8000

## Docker setup
- Clone the git repository
- Build the docker image: `docker build -t myrepo/simple-monitor .`
- Run the container: `docker run --name simple-monitor -p 8000:8000 myrepo/simple-monitor`
- Access the container at [hostname]:8000

## Managing the server:
- Failed devices will always be at the top. 
- The last time a device was seen is shown in the "Last Seen" column.
- To add, delete or edit a device, click the manage devices link and click the host tabs. 
- Click run report to ping all devices right now.
