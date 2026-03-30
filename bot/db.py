import motor.motor_asyncio
import time
from .config import DB_URI, DB_NAME, LOGS

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, id, name):
        return dict(
            id=id,
            name=name,
            session=None,
            role="free",
            expiry=0,
            code=None,
            usage={"batches": 0, "files": 0, "last_reset": int(time.time())}
        )
    
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)

    async def set_session(self, id, session):
        await self.col.update_one({'id': int(id)}, {'$set': {'session': session}})
        
    async def get_session(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('session', None) if user else None

    async def remove_session(self, id):
        await self.col.update_one({'id': int(id)}, {'$set': {'session': None}})

# Initialize Database connection dynamically
try:
    if DB_URI and DB_NAME:
        db = Database(DB_URI, DB_NAME)
        LOGS.info("Database connected successfully.")
    else:
        db = None
        LOGS.info("DB_URI not found. Database features will be disabled.")
except Exception as e:
    LOGS.info(f"Database connection failed: {e}")
    db = None
