from django.shortcuts import render
from django.http import HttpResponse


welcome = '''

=====================================================================================================
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

    <title>Welcome</title>
  </head>
  <body>
    <h1>WELCOME TO MY SERVER</h1>
  </body>
</html>
=====================================================================================================


'''

http_404 = '''

=====================================================================================================
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

    <title>404</title>
  </head>
  <body>
    <h1>URL NOT FOUND ON THIS SERVER</h1>
  </body>
</html>
=====================================================================================================


'''
def home_page(request):
    return HttpResponse(welcome)

def error_four_zero_four(request, exception):
    return HttpResponse(http_404)