from ..database.models.user import User
from ..database.models.task import Task

User.create_table()
Task.create_table()