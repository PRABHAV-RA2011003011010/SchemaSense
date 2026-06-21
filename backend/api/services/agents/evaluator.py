import logging

logger = logging.getLogger(__name__)

def evaluate_sql(sql: str) -> bool:
    """
    Validate SQL before execution.
    Returns True if safe, False if unsafe.
    """
    forbidden_keywords = ["insert", "update", "delete", "drop", "alter", "truncate"]
    lowered_sql = sql.strip().lower()

    if not lowered_sql.startswith("select"):
        logger.error(f"Unsafe SQL detected (not SELECT): {sql}")
        return False
    if any(keyword in lowered_sql for keyword in forbidden_keywords):
        logger.error(f"Unsafe SQL detected (forbidden keyword): {sql}")
        return False

    logger.info("SQL validated successfully")
    return True
