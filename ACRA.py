from fastapi import FastAPI, APIRouter, HTTPException, status, Request, Depends, Query,Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models.Token import Token
from models.ErrorMsg import ErrorMsg
from models.LoginCredential import LoginCredential
from models.ResultResponse import ResultResponse
from models.NumResponse import NumResponse
from models.Operation import Operation
from models.SquareRootData import SquareRootData
from models.OperationRecord import OperationRecord
from auth.AuthJWT import AuthJWT
from mathTool.RandomString import GetRandomString
from mathTool.Calculator import Calculator
from typing import List
from database.DataOps import DataOps

import os
from dotenv import load_dotenv
load_dotenv()



app = FastAPI(
    title="Arithmetic Calculator REST API",
    description="Web platform to provide a simple calculator functionality (addition, subtraction, multiplication, division, square root, and a random string generation)",
    version="0.1.0",
    openapi_tags=[{"name": "v1", "description": "Version 1 of the API"},]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN")],  # Origenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Métodos permitidos
    allow_headers=["*"],  # Cabeceras permitidas
)

v1_router = APIRouter()

def verify_token(request: Request):
   
    auth_header = request.headers.get("Authorization")
    print('Token Value: '+ str(auth_header))
    if auth_header is None or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = auth_header[len("Bearer "):]
    
    try:
        au = AuthJWT()
        username = au.validate(token)

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
        
    except Exception as e:
        raise  HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

@v1_router.post("/login", tags=["v1"], responses={
        200: {"model": Token},
        400: {"model": ErrorMsg, "description": "Invalid credentials or other bad request error"}
    })
async def login(user: LoginCredential):
    auth = AuthJWT()
    try:       
        return (auth.login(user))       
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content=ErrorMsg(detail= str(e)),
            headers={"Content-Type": "application/json"}
        )

@v1_router.post("/logout", tags=["v1"], responses={
        200: {"model": ResultResponse},
        400: {"model": ErrorMsg, "description": ""}
    })
async def logout(Authorization: str = Header(...)):
    auth = AuthJWT()
    token = Authorization.replace("Bearer", "")  # Elimina el prefijo "Bearer " si es necesario
    token = token.strip()
    try:          
        return ResultResponse(data=auth.logout(token))       
    except Exception as e:
       return JSONResponse(
            status_code=400,
            content=ErrorMsg(detail= str(e)),
            headers={"Content-Type": "application/json"}
        )

@v1_router.post("/validate_token", tags=["v1"], responses={
        200: {"model": ResultResponse},
        400: {"model": ErrorMsg, "description": ""}
    })
async def validate_token(Authorization: str = Header(...)):
    auth = AuthJWT()
    token = Authorization.replace("Bearer", "")  # Elimina el prefijo "Bearer " si es necesario
    token = token.strip()
    try:          
        return ResultResponse(data=auth.validate(token))       
    except Exception as e:
        return JSONResponse(
            status_code=400,
            #content={"detail": str(e)},
            content=(ErrorMsg(detail=str(e))).model_dump(),
            headers={"Content-Type": "application/json"}
        )


@v1_router.get("/random_string", tags=["v1"],
    
    description='For testing purposes, use Postman. There you can add the token generated from /login endpoint. Add the token in Header \'Authorization\'.',
    responses={
        200: {"model": ResultResponse},
        400: {"model": ErrorMsg}
    })
async def random_string(current_user: str = Depends(verify_token)):
    try:          
        ma = GetRandomString()  
        da = DataOps()
    
        da.SaveOperationRecord('random_string', current_user, ma, 100, ma)

        return ResultResponse(data=str(ma))       
    except Exception as e:
       return JSONResponse(
            status_code=400,
            #content=json.dump(ErrorMsg(detail= str(e))),
            content=(ErrorMsg(detail=str(e))).model_dump(),
            headers={"Content-Type": "application/json"}
        )

@v1_router.post("/addition", tags=["v1"],
    
    description='For testing purposes, use Postman. There you can add the token generated from /login endpoint. Add the token in Header \'Authorization\'.',
    responses={
        200: {"model": NumResponse},
        400: {"model": ErrorMsg}
    })
async def addition(data: Operation, current_user: str = Depends(verify_token)):
    try:          
        ca = Calculator(current_user)  
        return NumResponse(data=ca.Addition(data.num_a, data.num_b, data.operation))
    except Exception as e:
       return JSONResponse(
            status_code=400,
            content=(ErrorMsg(detail=str(e))).model_dump(),
            headers={"Content-Type": "application/json"}
        )
    
@v1_router.post("/subtraction", tags=["v1"],
    
    description='For testing purposes, use Postman. There you can add the token generated from /login endpoint. Add the token in Header \'Authorization\'.',
    responses={
        200: {"model": NumResponse},
        400: {"model": ErrorMsg}
    })
async def subtraction(data: Operation, current_user: str = Depends(verify_token)):
    try:          
        ca = Calculator(current_user)     
        return NumResponse(data=ca.Subtraction(data.num_a, data.num_b, data.operation))
    except Exception as e:
       return JSONResponse(
            status_code=400,
            content=(ErrorMsg(detail=str(e))).model_dump(),
            headers={"Content-Type": "application/json"}
        )
    
@v1_router.post("/multiplication", tags=["v1"],
    
    description='For testing purposes, use Postman. There you can add the token generated from /login endpoint. Add the token in Header \'Authorization\'.',
    responses={
        200: {"model": NumResponse},
        400: {"model": ErrorMsg}
    })
async def multiplication(data: Operation, current_user: str = Depends(verify_token)):
    try:          
        ca = Calculator(current_user)     
        return NumResponse(data=ca.Multiplication(data.num_a, data.num_b, data.operation))
    except Exception as e:
       return JSONResponse(
            status_code=400,
            content=(ErrorMsg(detail=str(e))).model_dump(),
            headers={"Content-Type": "application/json"}
        )
    
@v1_router.post("/division", tags=["v1"],
    
    description='For testing purposes, use Postman. There you can add the token generated from /login endpoint. Add the token in Header \'Authorization\'.',
    responses={
        200: {"model": NumResponse},
        400: {"model": ErrorMsg}
    })
async def division(data: Operation, current_user: str = Depends(verify_token)):
    try:          
        ca = Calculator(current_user)     
        return NumResponse(data=ca.Division(data.num_a, data.num_b, data.operation))
    except Exception as e:
       return JSONResponse(
            status_code=400,
            content=(ErrorMsg(detail=str(e))).model_dump(),
            headers={"Content-Type": "application/json"}
        )
    
@v1_router.post("/square_root", tags=["v1"],
    
    description='For testing purposes, use Postman. There you can add the token generated from /login endpoint. Add the token in Header \'Authorization\'.',
    responses={
        200: {"model": NumResponse},
        400: {"model": ErrorMsg}
    })
async def square_root(data: SquareRootData, current_user: str = Depends(verify_token)):
    try:          
        
        ca = Calculator(current_user)     
        return NumResponse(data=ca.SquareRoot(data.number,'square_root'))
    except Exception as e:
      return JSONResponse(
            status_code=400,
            content=(ErrorMsg(detail=str(e))).model_dump(),
            headers={"Content-Type": "application/json"}
        )


@v1_router.get("/record/", #response_model=List[OperationRecord],
    tags=["v1"],   
    description='For testing purposes, use Postman. There you can add the token generated from /login endpoint. Add the token in Header \'Authorization\'.',
    responses={
        200: {"model": List[OperationRecord]},
        400: {"model": ErrorMsg}
    })
async def record(
    page: int = Query(1, description="Número de página"),
    per_page: int = Query(10, description="Número de registros por página"),
    sort_by: str = Query('date', description="Campo por el cual ordenar"),
    sort_order: str = Query('asc', description="Orden de la ordenación, ascendente o descendente"),
    search: str = Query('', description="Cadena de búsqueda"),
    current_user: str = Depends(verify_token)
): #current_user: str = Depends(verify_token)
    try:       
        da = DataOps()
        return da.OperationRecords(current_user,
                                   page=page, 
                                   per_page=per_page, 
                                   sort_by=sort_by, 
                                   sort_order=sort_order,
                                   search=search
                                   )
    except Exception as e:
        return str(e)

@v1_router.delete("/record/{id}", tags=["v1"],    
    description='For testing purposes, use Postman. There you can add the token generated from /login endpoint. Add the token in Header \'Authorization\'.',
    responses={
        200: {"model": ResultResponse},
        400: {"model": ErrorMsg}
    })
async def softdelete(id: int ,current_user: str = Depends(verify_token)):
    try:  
             
        da = DataOps()
        return ResultResponse(data= da.SoftDelete(current_user,id)  )  
    except Exception as e:
       return JSONResponse(
            status_code=400,
            content=(ErrorMsg(detail=str(e))).model_dump(),
            headers={"Content-Type": "application/json"}
        )

app.include_router(v1_router, prefix="/v1")
 