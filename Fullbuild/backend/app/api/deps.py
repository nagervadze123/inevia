import time
from collections import defaultdict, deque

from fastapi import Cookie, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import User
from app.services.auth import decode_token

_rate = defaultdict(deque)


def rate_limit(request: Request):
    key = request.client.host if request.client else "anon"
    now = time.time()
    q = _rate[key]
    while q and now - q[0] > 60:
        q.popleft()
    if len(q) >= 120:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    q.append(now)


def get_current_user(access_token: str | None = Cookie(default=None), db: Session = Depends(get_db)) -> User:
    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    payload = decode_token(access_token)
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user
