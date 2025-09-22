from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError
from .results import Result




ALGORITHM="HS256"

class JWTHandler:
    def __init__(self, access_secret_key: str,refresh_secret_key: str):
        if not access_secret_key and refresh_secret_key:
            raise ValueError("secret_key is required")
        self.access_secret_key=access_secret_key
        self.refresh_secret_key=refresh_secret_key

    
    def create_access_token(self,access_token_claims:dict,expire_delta: timedelta=timedelta(minutes=1)):
        exp= datetime.now(tz=timezone.utc)+ expire_delta
        access_token_claims.update({"exp":int(exp.timestamp())})

        return jwt.encode(claims=access_token_claims, key=self.access_secret_key, algorithm=ALGORITHM)

    
    def create_refresh_token(self,refresh_token_claims:dict ,expire_delta: timedelta=timedelta(minutes=5)):
        exp= datetime.now(tz=timezone.utc)+ expire_delta
        refresh_token_claims.update({"exp":int(exp.timestamp())})

        return jwt.encode(claims=refresh_token_claims, key=self.refresh_secret_key, algorithm=ALGORITHM,)
        
    

    def verify_access_token(self, token: str, access: bool = False, refresh: bool = False):
        if access:
            secret_key = self.access_secret_key
        elif refresh:
            secret_key = self.refresh_secret_key
        else:
            return Result.error(message="set access=True or refresh=True")
        try:
            payload = jwt.decode(token, key=secret_key, algorithms=[ALGORITHM])
            return {"payload": payload, "verified": True}
        except ExpiredSignatureError:
            raise 
        except JWTClaimsError:
            raise
        except JWTError:
            raise






# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# class JWTHandler:
#     def __init__(
#         self,
#         secret_key: str,           # required
#         algorithm: str = "HS256",
#         expire_minutes: int = 60
#     ):
#         if not secret_key:
#             raise ValueError("secret_key is required")
#         self.SECRET_KEY = secret_key
#         self.ALGORITHM = algorithm
#         self.ACCESS_TOKEN_EXPIRE_MINUTES = expire_minutes

#     # Create JWT token
#     def create_jwt(self, payload: dict, expires_delta: int = None) -> str:
#         to_encode = payload.copy()
#         expire_minutes = expires_delta if expires_delta is not None else self.ACCESS_TOKEN_EXPIRE_MINUTES
#         expire = datetime.now(tz=timezone.utc) + timedelta(minutes=expire_minutes)
#         to_encode.update({"exp": expire})
#         token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
#         return token

#     # Verify JWT token
#     def verify_jwt(self, token: str) -> dict:
#         try:
#             payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
#             return payload
#         except JWTError:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid or expired token"
#             )

#     # FastAPI dependency
#     def get_current_payload(self, token: str = Depends(oauth2_scheme)) -> dict:
#         return self.verify_jwt(token)
