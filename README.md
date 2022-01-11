# bikeprogram

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/Ampheris/pattern-bikeprogram/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/Ampheris/pattern-bikeprogram/?branch=main)

A simulation of the real world. Users and bikes will be simulated

## How to start the program with docker

<pre>
docker-compose up -d server
docker-compose up -d frontend
docker-compose run bikeprogram
</pre>
When bikeprogam starts
<pre>
    The program will ask for port used default in docker-compose is 8000
    Next part is the url of the backend, which can be left blank and it'll use the standard option which should be correct. 
</pre>
