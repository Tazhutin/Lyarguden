import psycopg2
from loguru import logger

logger.add("Logs//Database_Logs//DB_Error_Logs.log" , format = "{time} {file} {level} {name} {line} {message}", level="ERROR", rotation="100 MB", compression="zip")
logger.add("Logs//Database_logs//DB_Debug_Logs.log", format="{time} {file} {level} {name} {line} {message}", level="DEBUG", rotation="100 MB", compression="zip")



