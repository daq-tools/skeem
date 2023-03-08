from sqlformatter.sqlformatter import SQLFormatter


def sql_canonicalize(sql: str) -> str:
    """
    Compute canonical representation for SQL statement.
    """
    return sql_pretty(sql)


def sql_pretty(sql: str, reindent: bool = False) -> str:
    """
    Prettify SQL statement.
    """
    sql = sql.strip().replace("\t", "    ")
    return SQLFormatter(
        reindent=reindent, indent_width=2, keyword_case="upper", identifier_case=None, comma_first=False
    ).format_query(sql)
