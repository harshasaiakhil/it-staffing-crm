def is_admin(user):
    return user.role.name == "admin"

def is_manager(user):
    return user.role.name in ["admin", "manager"]

def is_sales(user):
    return user.role.name == "sales_rep"
