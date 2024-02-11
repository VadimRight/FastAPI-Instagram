from fastapi.security import OAuth2PasswordBearer

# oauth instance declaration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
