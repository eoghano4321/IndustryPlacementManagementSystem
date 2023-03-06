# IndustryPlacementManagementSystem
Industry Placement Management System for CS4422 databases project built using flask on an oracle database

Boilerplate code can be found in week 8 of databases in CS4422 in Brightspace

To create make sure you add the title field to the placements.
Change your server settings in the main.py file as well.

# Installation Guide

<details><summary><b>Step 1 - Install Prerequisites</b></summary>
<p>
1. <a href = "https://dbeaver.io">DBeaver</a><br>
2. <a href = "https://www.docker.com/products/docker-desktop/">Docker</a><br>
3. <a href = "https://www.python.org/downloads/">Python</a>
</p>
</details>

<details><summary><b>Step 2 - Spin up the database in docker</b></summary>
<p>
Download the container from <a href = "https://hub.docker.com/r/gvenzl/oracle-xe">this link</a>.<br>
Initiate the docker instance using following command.<br>
docker run -d -p 1521:1521 -e ORACLE_PASSWORD=root gvenzl/oracle-xe
</p>
</details>

<details><summary><b>Step 3 - Connect to the database</b></summary>
<p>
Open DBeaver and establish a connection with the database using credentials of SYSTEM
</p>
</details>

<details><summary><b>Step 4 - Create the data</b></summary>
<p>
1. Create a new schema with name IPMS.<br>
2. Create a script and paste the following code to create the tables: <a href = "https://pastebin.com/H2xstxQd">link</a><br>
3. Create another script and paste the following code to insert template data: <a href = "https://pastebin.com/HtMcanns">link</a>
</p>
</details>

<details><summary><b>Step 5 - Install modules</b></summary>
<p>
1. Open command prompt<br>
2. Run the command 'pip install flask', and allow the module to install<br>
3. Run the command 'pip install oracle', and allow the module to install<br>
</p>
</details>

<details><summary><b>Step 6 - Launch the app</b></summary>
<p>
Open the repository folder in your preffered IDE, and run 'main.py'.<br>
Paste the follwing link in your browser: 'http://127.0.0.1:5000'
</p>
</details>
