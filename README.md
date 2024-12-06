### API Documents

##### Postman
We recommend to use Postman Application to call api endpoint [here](api.postman_collection.json)
![image](docs/img.png)


We have 3 tokens corresponding to 3 roles valid `until 12 a.m on Saturday December 2024`

- assistant_token:
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjVxcHBDaDlzaC1NYURNMnVObmhYQyJ9.eyJpc3MiOiJodHRwczovL2Rldi1td29od2UxN3A4anRocXVhLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzUxNzAxNmFkMjA5MTE4YzRiNDMyYzIiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAvYXBpIiwiaWF0IjoxNzMzNDk0MzM5LCJleHAiOjE3MzM1ODA3MzksImd0eSI6InBhc3N3b3JkIiwiYXpwIjoiMWNvaWhIdjEwdmNPUkhRRUpJWFVwcGxwVGxqSW01N3MiLCJwZXJtaXNzaW9ucyI6WyJyZWFkOmFjdG9yIiwicmVhZDptb3ZpZSJdfQ.APRPWWro5jO-V__31NFh_DyM_P-t8C6uzqpS9Jkwq_Kd1LLvePTpz5nL_gCirHdPUBC1uJIB-bFrRTHC4vl4ACrgPIuIC6VdIsI-suChECGOvWwB_fxNo7oXt6RogDRo5HpfZzkbVPfEiBzrpCnnqD0GotDCVRLa-GLf_RZz08U7qX4g8w7E2W9uaMyPID0JBir83gC8HsCvb3fbtDj5tDnu6-_7qC2IvxVzkGo-noP9anCNAU8R1F4R7G8qa3WphmfdDZ8NfdgJ1oxecpTqvj1GPMLCQvITQsDywxAmlmfWRrVy11fJAM3A7skblZYKIxVDT0YBtoCwYm0WD254-A
```

- director_token:
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjVxcHBDaDlzaC1NYURNMnVObmhYQyJ9.eyJpc3MiOiJodHRwczovL2Rldi1td29od2UxN3A4anRocXVhLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzUxNzAxNmFkMjA5MTE4YzRiNDMyYzIiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAvYXBpIiwiaWF0IjoxNzMzNDk0MzM5LCJleHAiOjE3MzM1ODA3MzksImd0eSI6InBhc3N3b3JkIiwiYXpwIjoiMWNvaWhIdjEwdmNPUkhRRUpJWFVwcGxwVGxqSW01N3MiLCJwZXJtaXNzaW9ucyI6WyJyZWFkOmFjdG9yIiwicmVhZDptb3ZpZSJdfQ.APRPWWro5jO-V__31NFh_DyM_P-t8C6uzqpS9Jkwq_Kd1LLvePTpz5nL_gCirHdPUBC1uJIB-bFrRTHC4vl4ACrgPIuIC6VdIsI-suChECGOvWwB_fxNo7oXt6RogDRo5HpfZzkbVPfEiBzrpCnnqD0GotDCVRLa-GLf_RZz08U7qX4g8w7E2W9uaMyPID0JBir83gC8HsCvb3fbtDj5tDnu6-_7qC2IvxVzkGo-noP9anCNAU8R1F4R7G8qa3WphmfdDZ8NfdgJ1oxecpTqvj1GPMLCQvITQsDywxAmlmfWRrVy11fJAM3A7skblZYKIxVDT0YBtoCwYm0WD254-A
```


- productor_token:
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjVxcHBDaDlzaC1NYURNMnVObmhYQyJ9.eyJpc3MiOiJodHRwczovL2Rldi1td29od2UxN3A4anRocXVhLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzUxNzA2OWFiNmJmZjVmNWIwYWVmNDEiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAvYXBpIiwiaWF0IjoxNzMzNDk0NDU3LCJleHAiOjE3MzM1ODA4NTcsImd0eSI6InBhc3N3b3JkIiwiYXpwIjoiMWNvaWhIdjEwdmNPUkhRRUpJWFVwcGxwVGxqSW01N3MiLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6YWN0b3IiLCJjcmVhdGU6bW92aWUiLCJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJyZWFkOmFjdG9yIiwicmVhZDptb3ZpZSIsInVwZGF0ZTphY3RvciIsInVwZGF0ZTptb3ZpZSJdfQ.P3sVe-lE3dPmOdsJLU2NoMtQfYEhelf7nOwy9ot5crlJBqKrOa-NZU-28Sy3Bo3ruOnt1L0CFOuqtVerNCsgKbFmcunEywH3H-P0-IMTtj2GP1gqPHTd5zFjCghy3d3rFQ0SL3ibCIgQHt8IkLCk7uszPx3-sd4rMh6MrG0Yx-m0MH-0F_s4am7j4d5E6Pnj7oX-6vnulHLme0tUlX16uuruIn4GyZHy_7Roao1lgbSiueu2VXS4U4wuKkHKLl5I1bxkkuTffoIfn0-RAzY18RpkKil9LzNZzoeLjuAGAdim_xnHclBUPfRLsDQRQjxdWytM98jx6h9iSoOY40wqXQ
```



### Install and Run application on local

#### Installing Dependencies

##### Python 3.12
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

##### Virtual Environment
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

##### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies

```
pipenv lock
pipenv requirements > requirements.txt
pip install -qr requirements.txt
```

##### Running the server
```commandline
python app.py
```

