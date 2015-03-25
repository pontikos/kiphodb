# Kinase-Phosphatase database

Group project undertaken at Imperial College in 2009 on the MSci Bioinformatics program.

## Instructions

1) Create the database and the appropriate user:
```
CREATE DATABASE kiphodb CHARACTER SET utf8;
CREATE USER 'dbproject'@'localhost' IDENTIFIED BY '312032';
GRANT ALL PRIVILEGES on kiphodb.* to 'dbproject'@'localhost';
```

2) Change configuration of apache:

```
LoadModule python_module /usr/lib/httpd/modules/mod_python.so
<Location "/">
    SetHandler python-program
    PythonHandler django.core.handlers.modpython
    SetEnv DJANGO_SETTINGS_MODULE dbproject.settings
    PythonOption django.root /dbproject
    PythonDebug On
    PythonPath "['/home/workspace/'] + sys.path"
</Location>
```

3) Create the project

```
mkdir /home/workspace
chown chris /home/workspace
chgrp users /home/workspace
cd /home/workspace
django-admin.py startproject dbproject
```


4) Set the server up
```
ddclient
/etc/rc.d/mysqld start
export PYTHON_EGG_CACHE="/tmp/.python-eggs"
/etc/rc.d/httpd start
svnserve -d
```
