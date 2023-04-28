#!/usr/bin/env python3
"""Filtered Logger"""
from typing import List
import re
from mysql.connector import MySQLConnection
from os import getenv
from logging import (
    Formatter,
    getLogger,
    INFO,
    Logger,
    LogRecord,
    StreamHandler
)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], r: str, m: str, sep: str) -> str:
    """filters a string

    Args:
        fields (List[str]): _description_
        r (str): _description_
        m (str): _description_
        sep (str): _description_

    Returns:
        str: new line that the Personally identifiable information
            has being removed
    """
    for item in fields:
        m = re.sub("(?<={}=)[^{}]+".format(item, sep), r, m)
    return m


def get_logger() -> Logger:
    """Implement a get_logger function that takes no arguments
    and returns a logging.Logger object.

    The logger should be named "user_data" and only log up to
    logging.INFO level. It should not propagate messages to other
    loggers. It should have a StreamHandler with RedactingFormatter
    as formatter.

    Returns:
        Logger: _description_
    """
    logger = getLogger('user_data')
    logger.setLevel(INFO)
    logger.propagate = False
    logger.addHandler(StreamHandler().setFormatter(
        RedactingFormatter(PII_FIELDS)))
    return logger


def get_db() -> MySQLConnection:
    """returns a mysql connection

    Returns:
        MySQLConnection: mysql
    """
    return MySQLConnection(
        port=3306,
        host=getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=getenv("PERSONAL_DATA_DB_NAME", ""),
        user=getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=getenv("PERSONAL_DATA_DB_PASSWORD", "")
    )


class RedactingFormatter(Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: LogRecord) -> str:
        """Implement the format method to filter values in incoming
        log records using filter_datum. Values for fields in fields
        should be filtered.

        Args:
            record (LogRecord): _description_

        Returns:
            str: _description_
        """
        return filter_datum(
            self.fields,
            self.REDACTION,
            super(RedactingFormatter, self).format(record),
            self.SEPARATOR
        )


def main():
    """main function
    """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    cursor = get_db().cursor()
    cursor.execute(f"SELECT {fields} FROM users;")
    for r in cursor.fetchall():
        get_logger().handle(LogRecord(
            name="user_data", level=INFO, msg='{};'.format(
                '; '.join(list(map(
                    lambda x: '{}={}'.format(x[0], x[1]),
                    zip(fields.split(','), r),
                ))))))


if __name__ == "__main__":
    main()
