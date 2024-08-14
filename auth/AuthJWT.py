from jose import JWTError, jwt, ExpiredSignatureError
from typing import Optional, Dict
from datetime import datetime, timedelta
import os
from models.LoginCredential import LoginCredential
from models.Token import Token
from database.DataOps import DataOps


from dotenv import load_dotenv
load_dotenv()


class AuthJWT:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("EXPIRATION_TIME"))

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=3600)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def login(self, user: LoginCredential):
        try:

            util = DataOps()
             
            _user = util.ValidateUser(user.username, user.password)
            if _user:
                access_token_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = self.create_access_token(
                    data={"sub": user.username}, expires_delta=access_token_expires
                )

                util.SaveToken(user.username, access_token)

                return {"access_token": access_token, "token_type": "bearer"}
            else:
                raise Exception('There is not user \''+str(user.username)+'\'')
        except Exception as e:
            raise Exception('Error generating Token: ' + str(e))

    def logout(self, access_token):
        try:
            util = DataOps()
            return util.RevokeToken(access_token)
        except Exception as e:
            raise Exception('Error revoking Token: ' + str(e))

    def validate_access_token(self, token: str):
       
        try:
           
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if not username:
                raise Exception("Token invalid: missing username.")     

            return username                   
        except ExpiredSignatureError:        
            raise Exception("Token expired.")    
        except JWTError as e:
            raise Exception(e)

    def validate(self, token):
        try:
            util = DataOps()
            token_valid = util.ValidateToken(token)
            
            if token_valid:
                
                return self.validate_access_token(token_valid)
            else:
                raise Exception('Token not found in database or revoked.')
        except Exception as e:
             raise Exception('Error validating Access: ' + str(e))

    