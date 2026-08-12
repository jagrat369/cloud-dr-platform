from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import APP_NAME, APP_VERSION
from app.database import Base, engine

# Import models so SQLAlchemy creates the tables
import app.models

# Import routers
from app.routes.health import router as health_router
from app.routes.users import router as users_router
from app.routes.backup import router as backup_router
from app.routes.failure import router as failure_router
from app.routes.restore import router as restore_router
from app.routes.metrics import router as metrics_router
from app.routes.auth import router as auth_router

# Import scheduler
from app.scheduler import start_scheduler, stop_scheduler


# =====================================================
# Create database tables
# =====================================================

Base.metadata.create_all(bind=engine)


# =====================================================
# Application Lifespan
# =====================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Start automatic backup scheduler
    start_scheduler()

    yield

    # Stop scheduler when application shuts down
    stop_scheduler()


# =====================================================
# Create FastAPI app
# =====================================================

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Cloud Disaster Recovery Platform",
    lifespan=lifespan
)


# =====================================================
# Register Routers
# =====================================================

app.include_router(health_router)
app.include_router(users_router)
app.include_router(backup_router)
app.include_router(failure_router)
app.include_router(restore_router)
app.include_router(metrics_router)
app.include_router(auth_router)