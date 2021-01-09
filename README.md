# Smart-Mart / Grace Shopper
A single-page application for ordering smart home products. The app features a products view, individual product information, and OAuth support for users to sign into Google or Facebook. 

View Demo on [Heroku](https://smart-mart.herokuapp.com/)

Project [[link](https://github.com/yoursmarthome/smart-mart)] 

## Technologies
Reactjs, Postgres, DJango, Nodejs

## Installation
Clone this repository on to your local machine:

## Create databse in pstgres
Run `create_user_script.sql` to create database of nodejs

## Configuration
Download and install Node for your operating system. Node is available for Mac, Linux and Windows.

[Node Download Page](https://nodejs.org/en/download/)

NPM (Node Package Manager) is bundled with Node and allows for easy installation of the required dependencies. Dependencies can be installed all at once or one at a time.

### Install All Dependencies

`$ npm install`

_This command installs all of the required dependencies listed in the package.json file._



## Operating Instructions
Seed the DB:
` $ npm run seed `

## python requirements
`pip install -r requirements.txt`


## Start the express server:
In one terminal run the following command
` $ npm run start-dev `
View the Smart-Mart application:
` $ open http://localhost:8080 ` in your browser (**it will open the nodejs server along with react**)


## start the django server
In other terminal `cd server2` and `python manage.py runserver` and run `python manage.py migrate` 
Run `python manage.py dummy`

Run the `delete_user_script` file on postgres to delete the database of nodejs
#### Enjoy the app!
