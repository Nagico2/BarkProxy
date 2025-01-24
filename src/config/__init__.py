from loguru import logger


CONFIG = None

def load_config():
    from .config import Config
    return Config


if CONFIG is None:
    CONFIG = load_config()
    logger.info("====== Config ======")
    logger.info(f'\tDEBUG: {CONFIG.DEBUG}')
    logger.info(f'\tBASE_DIR: {CONFIG.BASE_DIR}')
    logger.info(f'\tBASE_URL: {CONFIG.BASE_URL}')
    logger.info(f'\tSTATIC_DIR: {CONFIG.STATIC_DIR}')
    logger.info(f'\tSTATIC_URL: {CONFIG.STATIC_URL}')
    logger.info(f'\tBARK_ENDPOINT: {CONFIG.BARK_ENDPOINT}')

    if not CONFIG.BARK_APIKEY:
        raise ValueError('BARK_APIKEY is required')

    logger.info(f'\tBARK_ENCRYPT_KEY: {"Enabled" if CONFIG.BARK_ENCRYPT_KEY else "Disabled"}')
    logger.info(f'\tSIGN_SECRET: {"Enabled" if CONFIG.SIGN_SECRET else "Disabled"}')
    logger.info(f'\tAPI_AUTH_KEY: {"Enabled" if CONFIG.API_AUTH_KEY else "Disabled"}')

    if not CONFIG.API_AUTH_KEY:
        logger.warning("API_AUTH_KEY is not set, it's dangerous to expose the interface to the public")

    logger.info("====================")