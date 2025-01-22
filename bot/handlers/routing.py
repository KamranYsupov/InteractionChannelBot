from aiogram import Router

from .start import router as start_router
from .feedbacks import router as feedbacks_router

def get_main_router():
    main_router = Router()

    main_router.include_router(start_router)
    main_router.include_router(feedbacks_router)

    return main_router