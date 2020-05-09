# Pratilipi-profession-space

##### Hosted on - https://pratilipi-professional-space.herokuapp.com/

------------


#### DB Model:
##### Table: `company_details`, `user_details`, `user_auth`
- `email` is the Primary key used in `user_details` and `user_auth` to indentify users. And also act as a relation(foreign key) between the two tables.
- `company_name` is used as primary key in `company_details`. And act as Foreign key between `user_details.company_name` column and `company_details.name` column.
- Sepaerate company tables are also present to keep track of live_user_count on company page.

------------
#### To Run in local :
Clone the repo and install the requirments file. And running the app.py should start the local server.

------------

#### Technologies Used: 
- Python
- Flask framework
- PostgreSql with SqlAlchemy wrapper.
