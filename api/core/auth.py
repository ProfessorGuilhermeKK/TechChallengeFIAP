from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from api.core.config import get_settings
from api.core.logger import user_var
import logging
import uuid

from api.domain.auth.schemas import TokenData, User, UserInDB

try:
    from passlib.context import CryptContext
    USE_PASSLIB = True
except ImportError:
    USE_PASSLIB = False

try:
    import bcrypt
    USE_BCRYPT_DIRECT = True
except ImportError:
    USE_BCRYPT_DIRECT = False
    bcrypt = None

logger = logging.getLogger(__name__)

settings = get_settings()

if USE_PASSLIB:
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        logger.info("Passlib inicializado com sucesso")
    except Exception as e:
        logger.warning(f"Erro ao inicializar passlib: {e}. Usando bcrypt diretamente.")
        USE_PASSLIB = False
        pwd_context = None
else:
    pwd_context = None

if not USE_PASSLIB and not USE_BCRYPT_DIRECT:
    raise RuntimeError(
        "Erro: bcrypt não está disponível. "
        "Execute: pip install bcrypt passlib[bcrypt]"
    )
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"/api/{settings.api_version}/auth/login",
    scheme_name="OAuth2PasswordBearer"
)


def _parse_users_from_env() -> dict:
    users_db = {}
    
    try:
        users_string = settings.auth_users
        if not users_string:
            logger.warning("AUTH_USERS não configurado, usando usuários padrão")
            return _get_default_users()
        
        for user_entry in users_string.split(','):
            user_entry = user_entry.strip()
            if not user_entry:
                continue
            
            try:
                parts = user_entry.split(':')
                if len(parts) < 4:
                    logger.warning(f"Formato inválido para usuário: {user_entry}")
                    continue
                
                username, password, full_name, email = parts[0], parts[1], parts[2], parts[3]
                
                hashed_password = get_password_hash(password)
                
                users_db[username] = {
                    "username": username,
                    "full_name": full_name,
                    "email": email,
                    "hashed_password": hashed_password,
                    "disabled": False,
                }
                
                logger.info(f"Usuário '{username}' carregado das variáveis de ambiente")
                
            except Exception as e:
                logger.error(f"Erro ao processar usuário '{user_entry}': {e}")
                continue
        
        if not users_db:
            logger.warning("Nenhum usuário válido encontrado, usando usuários padrão")
            return _get_default_users()
        
        return users_db
        
    except Exception as e:
        logger.error(f"Erro ao carregar usuários das variáveis de ambiente: {e}")
        return _get_default_users()


def _get_default_users() -> dict:
    logger.warning("⚠️ Usando usuários padrão - NÃO RECOMENDADO EM PRODUÇÃO!")
    return {
        "admin": {
            "username": "admin",
            "full_name": "Admin User",
            "email": "admin@booksapi.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            "disabled": False,
        },
        "testuser": {
            "username": "testuser",
            "full_name": "Test User",
            "email": "test@booksapi.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            "disabled": False,
        }
    }


fake_users_db = _parse_users_from_env()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            truncated = password_bytes[:72].decode('utf-8', errors='ignore')
            plain_password = truncated
        
        if USE_PASSLIB and pwd_context:
            try:
                return pwd_context.verify(plain_password, hashed_password)
            except Exception as e:
                logger.warning(f"Passlib falhou, tentando bcrypt diretamente: {e}")
                if USE_BCRYPT_DIRECT and bcrypt:
                    return bcrypt.checkpw(
                        plain_password.encode('utf-8'),
                        hashed_password.encode('utf-8')
                    )
                return False
        
        elif USE_BCRYPT_DIRECT and bcrypt:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        else:
            logger.error("Nenhum método de verificação de senha disponível")
            return False
    except ValueError as e:
        logger.warning(f"Erro ao verificar senha (senha muito longa?): {e}")
        return False
    except Exception as e:
        logger.error(f"Erro ao verificar senha: {e}")
        return False


def get_password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password = password_bytes[:72].decode('utf-8', errors='ignore')
    
    if USE_PASSLIB and pwd_context:
        return pwd_context.hash(password)
    elif USE_BCRYPT_DIRECT and bcrypt:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    else:
        raise RuntimeError("Nenhum método de hash de senha disponível")


def get_user(username: str) -> Optional[UserInDB]:
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)
    return None


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire, 
                      "type": "access",
                      "iat": datetime.utcnow(),
                      "jti": str(uuid.uuid4()),
                      })
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    return encoded_jwt


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(days=settings.refresh_token_expire_days)
    )

    # claims adicionais úteis
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4()),
        "type": "refresh",
    })

    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_token(token)
        token_type = payload.get("type")
        if token_type != "access":
            raise credentials_exception
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        logger.error(f"JWT Error: {e}")
        raise credentials_exception
    
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception

    user_var.set(user.username)

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user





