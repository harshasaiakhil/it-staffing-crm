from fastapi import Depends, HTTPException
from app.core.security import get_current_user

def require_role(roles: list):
    def checker(user = Depends(get_current_user)):
        if user.role.name not in roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return user
    return checker
