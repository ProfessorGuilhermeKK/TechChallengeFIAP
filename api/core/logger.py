"""
Configuração de logging estruturado
"""
import contextvars
import logging
import sys
from pathlib import Path
from pythonjsonlogger import jsonlogger
from datetime import datetime


request_id_var = contextvars.ContextVar("request_id", default=None)
user_var = contextvars.ContextVar("user", default=None)

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Formatter JSON customizado"""
    
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        
        if not log_record.get('timestamp'):
            log_record['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
    

class ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        record.user = user_var.get()
        return True


def setup_logging(log_level: str = "INFO"):
    """
    Configura o sistema de logging
    
    Args:
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Criar diretório de logs se não existir
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configurar formato
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Remover handlers existentes
    root_logger.handlers.clear()
    
    # Console handler (formato simples)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_formatter = logging.Formatter(log_format)
    console_handler.setFormatter(console_formatter)
    console_handler.addFilter(ContextFilter())
    root_logger.addHandler(console_handler)
    
    # File handler (formato JSON)
    file_handler = logging.FileHandler(
        log_dir / f'api_{datetime.now().strftime("%Y%m%d")}.log', 
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    json_formatter = CustomJsonFormatter("%(timestamp)s %(level)s %(name)s %(message)s %(request_id)s %(user)s")

    file_handler.setFormatter(json_formatter)
    file_handler.addFilter(ContextFilter())
    root_logger.addHandler(file_handler)
    
    # Configurar loggers de terceiros
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    logging.info("Logging system configured")





