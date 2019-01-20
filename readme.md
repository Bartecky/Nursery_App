**Nursery App**
<hr>
The project allows you to manage nursery, it's for parents and staff.
Parent has the option of registering a child and caregivers (f.e. able to pick up child from nursery)<br>
Staff has several options, can add/modify/delete groups, extra activities, diets for children, teachers.<br>
Important thing for staff is easy recruitment panel - children list, sorted by status (verified, on waiting list, in nursery)
<hr>

**Start project**


Clone repository, create your own virtualenv and activate it.<br>
In terminal:<br>
`virtualenv -p python3 <your-dir-name>`<br>
next:<br>
`source <your-dir-name>/bin/activate`<br>
install requirements from project:<br>
`pip install requirements.txt`



Running:<br>
You need postgresql and db called 'nurseryapp'<br>
_Apply migrations:_<br>
`python manage.py migrate`<br>
and run project:<br>
`python manage.py runserver`

IMPORTANT:
You have to create super user by:
`python manage.py createsuperuser` and login into this account to see staff features in project.
<hr>

**Screens**


Parent view<br>
<img src="src/images/parent-view-1.png" height=400>

Parent view2<br>
<img src="src/images/parent-view-2.png" height=400>

Child detail<br>
<img src="src/images/child-detail.png" height=400>

Children list<br>
<img src="src/images/children-list.png" height=400>

Teacher detail<br>
<img src="src/images/teacher-detail.png" height=400>

Management<br>
<img src="src/images/management.png" height=400>
