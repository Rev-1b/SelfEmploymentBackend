import hashlib
import hmac
from datetime import datetime, timedelta


def verify_telegram_auth(data: dict, bot_token: str) -> bool:
    auth_data = data.copy()
    check_hash = auth_data.pop("hash", None)
    auth_date = auth_data.get('auth_date')

    try:
        auth_date = int(auth_date)
    except (TypeError, ValueError):
        return False

    # now_ts = int(datetime.utcnow().timestamp())
    # if now_ts - auth_date > 60:
    #     return False

    data_check_string = '\n'.join(
        [f"{k}={auth_data[k]}" for k in sorted(auth_data)]
    )

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return hmac.compare_digest(calculated_hash, check_hash)