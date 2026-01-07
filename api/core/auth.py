"""
Sistema de autenticação JWT
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from api.core.config import get_settings
import logging

from api.domain.auth.schemas import TokenData, User, UserInDB

# Tentar importar passlib, mas usar bcrypt diretamente como fallback
try:
    from passlib.context import CryptContext
    USE_PASSLIB = True
except ImportError:
    USE_PASSLIB = False

# Tentar importar bcrypt diretamente
try:
    import bcrypt
    USE_BCRYPT_DIRECT = True
except ImportError:
    USE_BCRYPT_DIRECT = False
    bcrypt = None

logger = logging.getLogger(__name__)

# Configurações
settings = get_settings()

# Configurar bcrypt - usar passlib se disponível, senão usar bcrypt diretamente
# Isso contorna o problema de incompatibilidade entre passlib e bcrypt
if USE_PASSLIB:
    try:
        # Inicialização lazy - não forçar inicialização do backend
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
# OAuth2PasswordBearer para Swagger UI - não precisa de client_id/client_secret
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"/api/{settings.api_version}/auth/login",
    scheme_name="OAuth2PasswordBearer"
)

# Banco de dados fake de usuários (em produção, usar banco de dados real)
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@booksapi.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
        "disabled": False,
    },
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@booksapi.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
        "disabled": False,
    }
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta"""
    try:
        # Truncar senha para evitar erro do bcrypt (limite de 72 bytes)
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            truncated = password_bytes[:72].decode('utf-8', errors='ignore')
            plain_password = truncated
        
        # Usar passlib se disponível, senão usar bcrypt diretamente
        if USE_PASSLIB and pwd_context:
            try:
                return pwd_context.verify(plain_password, hashed_password)
            except Exception as e:
                # Se passlib falhar, tentar bcrypt diretamente
                logger.warning(f"Passlib falhou, tentando bcrypt diretamente: {e}")
                if USE_BCRYPT_DIRECT and bcrypt:
                    return bcrypt.checkpw(
                        plain_password.encode('utf-8'),
                        hashed_password.encode('utf-8')
                    )
                return False
        
        elif USE_BCRYPT_DIRECT and bcrypt:
            # Usar bcrypt diretamente (contorna problema do passlib)
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
    """Gera hash da senha"""
    # Truncar senha se necessário
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password = password_bytes[:72].decode('utf-8', errors='ignore')
    
    if USE_PASSLIB and pwd_context:
        return pwd_context.hash(password)
    elif USE_BCRYPT_DIRECT and bcrypt:
        # Usar bcrypt diretamente
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    else:
        raise RuntimeError("Nenhum método de hash de senha disponível")


def get_user(username: str) -> Optional[UserInDB]:
    """Busca usuário no banco de dados"""
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)
    return None


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """Autentica usuário"""
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria token JWT de acesso
    
    Args:
        data: Dados a serem codificados no token
        expires_delta: Tempo de expiração
        
    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Obtém usuário atual a partir do token JWT
    
    Args:
        token: Token JWT
        
    Returns:
        Usuário autenticado
        
    Raises:
        HTTPException: Se o token for inválido
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
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
    
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Verifica se o usuário atual está ativo
    
    Args:
        current_user: Usuário atual
        
    Returns:
        Usuário ativo
        
    Raises:
        HTTPException: Se o usuário estiver desabilitado
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user





