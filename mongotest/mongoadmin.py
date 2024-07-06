# Import the MongoAdmin base class
from mongonaut.sites import MongoAdmin

# Import your custom models
from .models import ToolList_Mongo

# Instantiate the MongoAdmin class
# Then attach the mongoadmin to your model
ToolList_Mongo.mongoadmin = MongoAdmin()