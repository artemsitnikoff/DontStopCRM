from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.config import settings
from src.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler,
)

# Import all routers
from src.auth.router import router as auth_router
from src.leads.router import router as leads_router
from src.chats.router import router as chats_router
from src.calendar.router import router as calendar_router
from src.dashboard.router import router as dashboard_router

# Import exception handlers for specific modules
from fastapi.responses import JSONResponse
from src.auth.exceptions import (
    UserNotFoundException,
    InvalidCredentialsException,
    UserAlreadyExistsException,
    InactiveUserException,
)
from src.leads.exceptions import (
    LeadNotFound,
)
from src.chats.exceptions import (
    ChatNotFound,
)
from src.calendar.exceptions import (
    AppointmentNotFoundException,
    InvalidLeadException as CalendarInvalidLeadException,
    TimeSlotConflictException,
)


def create_application() -> FastAPI:
    """Create FastAPI application with all configurations."""

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="DontStopCRM - Customer Relationship Management System",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(auth_router)
    app.include_router(leads_router)
    app.include_router(chats_router)
    app.include_router(calendar_router)
    app.include_router(dashboard_router)

    # Add exception handlers
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    # Custom exception handlers mapping
    EXCEPTION_HANDLERS = {
        UserNotFoundException: (404, "USER_NOT_FOUND"),
        InvalidCredentialsException: (401, "INVALID_CREDENTIALS"),
        UserAlreadyExistsException: (400, "USER_ALREADY_EXISTS"),
        InactiveUserException: (400, "INACTIVE_USER"),
        LeadNotFound: (404, "LEAD_NOT_FOUND"),
        ChatNotFound: (404, "CHAT_NOT_FOUND"),
        AppointmentNotFoundException: (404, "APPOINTMENT_NOT_FOUND"),
        CalendarInvalidLeadException: (400, "CALENDAR_INVALID_LEAD"),
        TimeSlotConflictException: (409, "TIME_SLOT_CONFLICT"),
    }

    # Register exception handlers using the mapping
    for exc_class, (status_code, error_code) in EXCEPTION_HANDLERS.items():
        def create_handler(status: int, code: str):
            async def handler(request, exc):
                return JSONResponse(
                    status_code=status,
                    content={
                        "error": code,
                        "detail": str(exc),
                    },
                )
            return handler

        app.add_exception_handler(exc_class, create_handler(status_code, error_code))

    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": "DontStopCRM API",
            "version": "1.0.0",
            "docs": "/docs",
            "redoc": "/redoc",
        }

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy"}

    return app


app = create_application()