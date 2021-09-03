// Open the command line and open the project directory
// run command : python manage.py makemigrations
// run command : python manage.py migrate
// run command : python manage.py runserver
// above command will run the project on your local system

// if you get errors (most probably about the pdf reader function which is convert_pdf_to_txt)
// go to the views.py inside the fileupload directory and on line number 78 you will see below code
//     pdfData = convert_pdf_to_txt(a)
// I hope everyone knows how to read pdf data from various libraries
// so maybe you can use pypdf or pypdf2 or pdfminer which im using just read all the data
// and put it inside the pdfData variable
// and try to run the code

// if you get error like there is no file like that
// go to the command line and run
// python manage.py create superuser
// then enter the name as an admin
// enter the password as an admin
// no need to fill other forms
// now you can go to the localhost:8000/admin
// and admin panel in django will pop up there you can login
// now you will be able to see the fileupload bottom left (not actually bottom left in the center probably)
// click on it then click on the sample
// then add the file which you want to read
// and go back to localhost:8000 and check if its running
// still giving errors call me
// hope you dont need to call you are smart guys!
