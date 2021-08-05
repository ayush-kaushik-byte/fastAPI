from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from repository import schemas
import JWTtoken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")
print(oauth2_scheme)

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(data, JWTtoken.SECRET_KEY, algorithms=[JWTtoken.ALGORITHM])
        name: str = payload.get("sub")
        id: int = payload.get("id")
        print(name)
        if name is None:
            raise credentials_exception
        token_data = schemas.TokenData(name=name, id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data
