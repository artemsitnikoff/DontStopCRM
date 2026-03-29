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
    LeadNotFoundException,
    LeadAlreadyExistsException,
)
from src.chats.exceptions import (
    MessageNotFoundException,
    InvalidLeadException as ChatInvalidLeadException,
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

    # Auth module exception handlers
    @app.exception_handler(UserNotFoundException)
    async def user_not_found_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={
                "error": "USER_NOT_FOUND",
                "detail": str(exc),
            },
        )

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_handler(request, exc):
        return JSONResponse(
            status_code=401,
            content={
                "error": "INVALID_CREDENTIALS",
                "detail": str(exc),
            },
        )

    @app.exception_handler(UserAlreadyExistsException)
    async def user_already_exists_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content={
                "error": "USER_ALREADY_EXISTS",
                "detail": str(exc),
            },
        )

    @app.exception_handler(InactiveUserException)
    async def inactive_user_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content={
                "error": "INACTIVE_USER",
                "detail": str(exc),
            },
        )

    # Leads module exception handlers
    @app.exception_handler(LeadNotFoundException)
    async def lead_not_found_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={
                "error": "LEAD_NOT_FOUND",
                "detail": str(exc),
            },
        )

    @app.exception_handler(LeadAlreadyExistsException)
    async def lead_already_exists_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content={
                "error": "LEAD_ALREADY_EXISTS",
                "detail": str(exc),
            },
        )

    # Chats module exception handlers
    @app.exception_handler(MessageNotFoundException)
    async def message_not_found_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={
                "error": "MESSAGE_NOT_FOUND",
                "detail": str(exc),
            },
        )

    @app.exception_handler(ChatInvalidLeadException)
    async def chat_invalid_lead_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content={
                "error": "INVALID_LEAD",
                "detail": str(exc),
            },
        )

    # Calendar module exception handlers
    @app.exception_handler(AppointmentNotFoundException)
    async def appointment_not_found_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={
                "error": "APPOINTMENT_NOT_FOUND",
                "detail": str(exc),
            },
        )

    @app.exception_handler(CalendarInvalidLeadException)
    async def calendar_invalid_lead_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content={
                "error": "INVALID_LEAD",
                "detail": str(exc),
            },
        )

    @app.exception_handler(TimeSlotConflictException)
    async def time_slot_conflict_handler(request, exc):
        return JSONResponse(
            status_code=409,
            content={
                "error": "TIME_SLOT_CONFLICT",
                "detail": str(exc),
            },
        )

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