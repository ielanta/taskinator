# taskinator

Task management system<br />
Tested on Python 3.6.0

Task statuses: new, in progress, completed, archived...<br />
Task app: handling task logic<br />
Activity app: handling comment logic<br />

# Useful commands to run project on local
```python3 -m venv myvenv```<br />
```source myvenv/bin/activate```<br />
```pip install -r requirements.txt```<br />
```python manage.py migrate```<br />
```python manage.py createsuperuser```<br />
```python manage.py runserver```<br />

# Urls examples
`http://127.0.0.1:8000/tasks/` tasks list<br />
`http://127.0.0.1:8000/tasks/7/comments/` comments list per task<br />

# Coverage
```
Name                                             Stmts   Miss  Cover
--------------------------------------------------------------------
activity/__init__.py                                 0      0   100%
activity/admin.py                                    4      0   100%
activity/migrations/0001_initial.py                  8      0   100%
activity/migrations/0002_auto_20190619_1253.py       5      0   100%
activity/migrations/__init__.py                      0      0   100%
activity/models.py                                  12      1    92%
manage.py                                           13      6    54%
task/__init__.py                                     0      0   100%
task/admin.py                                        4      0   100%
task/migrations/0001_initial.py                      7      0   100%
task/migrations/0002_auto_20190619_1300.py           6      0   100%
task/migrations/__init__.py                          0      0   100%
task/models.py                                      20      1    95%
task/serializers.py                                 21     16    24%
task/tests.py                                       65     42    35%
task/urls.py                                         3      0   100%
task/views.py                                       13      6    54%
taskinator/__init__.py                               0      0   100%
taskinator/settings.py                              21      1    95%
taskinator/urls.py                                   3      0   100%
--------------------------------------------------------------------
TOTAL                                              205     73    64%
```
