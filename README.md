## Flask Gateway
---
### Setup Virtual Environment
Install virtualenv.
```
pip install virtualenv
```

Create virtual environment.
```
source .venv/Scripts/activate
```
---
### Dependencies
Python package dependencies are contained in the requirements.txt. Run the installation within virtual environment.
```
pip install -r requirements.txt
```
---
### gRPC Stubs
Ensure the protobuf IDL are located in the protos folder. Run the following command to generate the client and server stubs in the grpclib folder.
```
python -m grpc_tools.protoc -Imain_app/grpclib=./main_app/protos --python_out=. --grpc_python_out=. --proto_path=./main_app/protos ./main_app/protos/useraccount.proto
```
Note:
python_out and grpc_python_out path arugments are relative to the path defined in the argument

---
### WSGI
Run the following the following command on windows.
```
waitress-serve --host localhost --port 8000 --call app:create_app
```