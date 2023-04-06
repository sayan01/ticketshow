from app import app

def any_in(list1, list2):
    return any(elem in list2 for elem in list1)

# Jinja environment configuration
app.jinja_env.filters['any_in'] = any_in
