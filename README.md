# Flask REST-API
### Introduction
Flask REST-API is a backend REST-API implementation using Flask, SQLAlchemy, Flask-JWT-Extended, PostgreSQL etc.
### Project Support Features
* Users can signup and login to their accounts
* Public (non-authenticated) users can access the details of stores, items and tags on the platform
* Authenticated users in addition, can create or modify store, item, tag or link/unlink a store and tag.
### Installation Guide
* Clone this repository [here](https://github.com/karti358/flask-rest-api.git).
* The main branch is the most stable branch at any given time, ensure you're working from it.
* Ensure you create a virtual environment and activate the environment
* ## Create Virtual Environment
*     python -m venv venv
* ## Activate virtual environment
  ## Linux
      source ./venv/bin/activate
  ## Windows
      ./venv/Scripts/activate
* ## Run the following command to install all dependencies
      pip install -r requirements.txt
* ## Create a new .env in project root and paste following line in it. Fill the needed data.
      SECRET_KEY=<secret_key>
      DATABASE_URI=<database-uri>
### Usage
* ## Run the following command to start the application.
      flask run
  ## if the above do not work
      python app.py
* Connect to the API using Postman.
### API Endpoints
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |
| POST | /user/register | To sign up a new user account |
| POST | /user/login | To login an existing user account |
| POST | /user/logout | To logout an existing user account |
| POST | /user/refresh | To refresh an existing refresh token of user account |
| GET | /store | To retrieve details of all stores on the platform |
| POST | /store | To add a store on the platform |
| GET | /store/:store_id | To retrieve an existing store on platform with id |
| DELETE | /store/:store_id | To delete an existing store on platform with id |

| GET | /item | To retrieve details of a all items |
| POST | /item | To item to the platform |
| GET | /item/:item_id | To retrieve a single item by id |
| DELETE | /item/:item_id | To delete a single item by id |
| PUT | /item/:item_id | To modify a single item by id |

| GET | /store/:store_id/tag | To retrieve all tags of a store |
| POST | /store/:store_id/tag | To add a single tag to a store |

| POST | /item/:item_id/tag/:tag_id | To link a tag and an item |
| DELETE | /item/:item_id/tag/:tag_id | To unlink an already linked tag and item |

| GET | /item/:item_id | To delete a single cause |
| GET | /item/:item_id | To delete a single cause |
### Technologies Used
* [NodeJS](https://nodejs.org/) This is a cross-platform runtime environment built on Chrome's V8 JavaScript engine used in running JavaScript codes on the server. It allows for installation and managing of dependencies and communication with databases.
* [ExpressJS](https://www.expresjs.org/) This is a NodeJS web application framework.
* [MongoDB](https://www.mongodb.com/) This is a free open source NOSQL document database with scalability and flexibility. Data are stored in flexible JSON-like documents.
* [Mongoose ODM](https://mongoosejs.com/) This makes it easy to write MongoDB validation by providing a straight-forward, schema-based solution to model to application data.
### Authors
* [Black Developa](https://github.com/blackdevelopa)
* ![alt text](https://avatars0.githubusercontent.com/u/29962968?s=400&u=7753a408ed02e51f88a13a5d11014484bc4d80ee&v=4)
### License
This project is available for use under the MIT License.
