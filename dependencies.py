from fastapi import Depends, HTTPException, status

from auth import get_current_user


# =====================================================
# Admin Only
# =====================================================

def admin_only(current_user=Depends(get_current_user)):
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Admin can perform this action."
        )
    return current_user


# =====================================================
# Admin or Warehouse Manager
# =====================================================

def admin_or_manager(current_user=Depends(get_current_user)):
    if current_user.role not in ["Admin", "Warehouse Manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied."
        )
    return current_user