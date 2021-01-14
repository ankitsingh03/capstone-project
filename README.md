# Smart-Mart / Grace Shopper
A single-page application for ordering smart home products. The app features a products view, individual product information, and OAuth support for users to sign into Google or Facebook. 

Source Demo on [Heroku](https://smart-mart.herokuapp.com/)
Source Project [[link](https://github.com/yoursmarthome/smart-mart)] 

## Technologies
Django, Reactjs, Postgres, 

## Installation
Clone this repository on to your local machine:

## Configuration
Download and install npm.
`sudo apt install npm`

## Create databse in postgres
Run `sudo -u postgres psql -f create_user_script.sql` to create database of Django.

NPM (Node Package Manager) is bundled with Node and allows for easy installation of the required dependencies. Dependencies can be installed all at once or one at a time.

### Install All Dependencies

`$ npm install`

_This command installs all of the required dependencies listed in the package.json file._

## Python requirements
`pip install -r requirements.txt`

## Python migrate
Move to server2 and run `python manage.py migrate`.

## Seed DB
To seed dummy data in database `python manage.py dummy`

## Run server
To run the server `python manage.py runserver`

View the Smart-Mart application:
` $ open http://localhost:8000 ` in your browser (**it will open the django server along with react**)

Run the `sudo -u postgres psql -f delete_user_script` file on postgres to delete the database of postgres
#### Enjoy the app!
