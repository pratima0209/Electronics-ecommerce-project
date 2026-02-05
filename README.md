# Electronics-ecommerce-project
Django e-commerce Electronics project with frontend

# Project Description

<p>Technologies used : Python, Django, SMTP, HTML, CSS, Bootstrap.
Added Product Cart, Dummy Payment System, Grand Total Calculations, OTP through email and verification.
User Account section is provided for the email, phone and address updation. Also to contact the customer service through email and Customer Order History and its details are provided.
</p><br>

<h3>Product Categories</h3>
<p>Electronics ecommerce project contains 4 categories:</p>
<ul>
  <li>Mobile</li>
  <li>Speaker</li>
  <li>TV's</li>
  <li>Laptops</li>
  
</ul><br>

<h3>Adding More products and categories</h3>
<h5>Migrations</h5>
<p>Run the migration command: <b>pyhthon manage.py makemigrations</b> and then <b>python manage.py migrate</b> to create a database.</p>
<p>Creating a super user using command: <b>python manage.py createsuperuser</b> it would ask for the credentials, create it using valid credentials and login to django administrator with this link <b>http://127.0.0.1:8000/admin</b>.
 After login we can add more required products.
</p>

<h3>Credentials need to be added</h3>
<p>To run the OTP functionality and receiving OTP through email, it need to be added with the email which has been 2-factor authenticated on the google and need get a password by google, after adding this credentials in the views.py file and settings.py file, OTP functionality through email will run.</p>
