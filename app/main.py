from fastapi import FastAPI

from routers.metrics import metrics_router
from routers.skills import skills_router
from routers.pipline import pipline_router
from routers.cities import cities_router
from routers.professions import professions_router

app = FastAPI()

app.include_router(
    router=metrics_router,
    prefix='/metrics',
)

app.include_router(
    router=skills_router,
    prefix='/skills',
)

app.include_router(
    router=pipline_router,
    prefix='/pipline',
)

app.include_router(
    router=cities_router,
    prefix='/cities',
)

app.include_router(
    router=professions_router,
    prefix='/professions',
)