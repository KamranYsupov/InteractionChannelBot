from aiogram import Router

from .start import router as start_router
from .feedbacks import router as feedbacks_router
from .actions import router as actions_router
from .events import router as events_router
from .language import router as language_router
from .html_echo import router as html_echo_router  
def get_main_router():
    main_router = Router()

    main_router.include_router(start_router)
    main_router.include_router(feedbacks_router)
    main_router.include_router(actions_router)
    main_router.include_router(events_router)
    main_router.include_router(language_router)
    main_router.include_router(html_echo_router)

    return main_router