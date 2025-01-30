## Enabling Authentication in MongoDB

### 1. Create the user administrator

Change to the **admin** database:

```
use admin
```



You need to create a user with the [**userAdminAnyDatabase**](https://docs.mongodb.com/manual/reference/built-in-roles/#userAdminAnyDatabase) role, which grants the privilege to create other users on any existing database. The following example will create the **admin** user with password “**nothing**”:

```
> db.createUser(
  {
    user: "admin",
    pwd: "nothing",
    roles: [ { role: "root", db: "admin" } ]
  }
)
```

### 2. Enable authentication in mongod configuration file

update `mongod.cfg` which is in the `bin` sub-directory of mongodb's installation directory

```
security:
    authorization: "enabled"
```



then restart `mongod` service.



### 3. Installing python modules

`Python 3.11.4` version was used for development

```
pip install git+https://github.com/idoshr/flask-mongoengine.git@1.0.1
pip install -r requirements.txt
```

