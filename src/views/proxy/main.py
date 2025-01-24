from sanic import Sanic, Unauthorized
from sanic.request import Request
from sanic.response import json
from loguru import logger


from logger import S_LOGGING_CONFIG_DEFAULTS, setup_log
from services.bark import BarkNotifier
from config import CONFIG
from utils import check_sign
import views.proxy.sms as sms_utils
import views.proxy.apps as apps_utils

setup_log(CONFIG.LOG_LEVEL)

app = Sanic("bark_proxy", log_config=S_LOGGING_CONFIG_DEFAULTS)

bark = BarkNotifier(CONFIG.BARK_ENDPOINT, CONFIG.BARK_APIKEY, CONFIG.BARK_ENCRYPT_KEY)

success = json({"status": "success"})

@app.middleware("request")
async def verify_signature(request: Request):
    if request.path.startswith("/notify/") and request.method == "POST":
        if CONFIG.SIGN_SECRET is None:
            return
        timestamp = int(request.json.get("timestamp", "0"))
        sign = request.json.get("sign", None)
        check_sign(timestamp, sign)

@app.middleware("request")
async def log_request(request: Request):
    if request.path.startswith("/ping"):
        return
    logger.info(f"Request: {request.method} {request.url}")

@app.middleware("request")
async def auth(request: Request):
    if request.headers.get("Authorization") != f"Bearer {CONFIG.API_AUTH_KEY}":
        raise Unauthorized("Invalid api key")

@app.get("/ping")
async def ping(request):
    return success

@app.route("/apps", methods=["GET", "POST"])
async def upload_apps(request):
    if request.method == "GET":
        logger.trace("Received get apps request")
        return json(await apps_utils.get_all())
    elif request.method == "POST":
        data = request.json
        logger.trace(f"Received add app request, app: {data['name']} ({data['package']})")
        await apps_utils.add_icon(data["package"], data["icon"])
        return success
    else:
        raise Unauthorized("Invalid method", status_code=405)



@app.post("/notify/app")
async def notify_app(request):
    logger.trace(f"Received app request: {request.json}")
    title = request.json.get("title", None)
    content = request.json.get("content", None)
    app_from = request.json.get("from", "Unknown")
    app_name = request.json.get("app", app_from)

    args = {
        "title": title,
        "body": content,
        "group": app_name,
        "icon": apps_utils.get_image_url(app_from),
    }

    logger.debug(f"Sending notification: {args}")
    await bark.send(**args)

    return success


@app.post("/notify/sms")
async def notify_sms(request):
    logger.trace(f"Received sms request: {request.json}")
    number = request.json.get("from", "Unknown")
    content = request.json.get("content", "")

    title = sms_utils.extract_name(content)
    if title is None:
        title = str(number)
    else:
        content = content.replace(f"【{title}】", "").strip()

    verification_code = sms_utils.extract_verification_code(content)

    if verification_code:
        content = content.replace(verification_code, f"{verification_code}✅").strip()

    args = {
        "title": title,
        "body": content,
        "group": "SMS",
        "icon": apps_utils.get_image_url("com.android.mms"),
    }

    if verification_code:
        args["copy"] = verification_code
        args["auto_copy"] = True
        args["group"] = "SMS_CODE"


    logger.debug(f"Sending notification: {args}")
    await bark.send(**args)

    return success