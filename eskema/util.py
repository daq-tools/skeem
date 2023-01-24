from sqlformatter.sqlformatter import SQLFormatter


def jd(data):
    pass


def canonicalize_sql(sql: str) -> str:
    sql = sql.strip().replace("\t", "    ")
    return SQLFormatter(reindent=False, keyword_case="upper", identifier_case=None).format_query(sql)
