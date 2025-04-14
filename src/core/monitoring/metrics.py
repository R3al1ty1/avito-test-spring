from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_fastapi_instrumentator import Instrumentator, metrics
import time
from fastapi import Response


REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"]
)

PVZ_CREATED = Counter(
    "pvz_created_total",
    "Total number of PVZ locations created"
)

RECEPTIONS_CREATED = Counter(
    "receptions_created_total",
    "Total number of receptions created"
)

PRODUCTS_ADDED = Counter(
    "products_added_total",
    "Total number of products added"
)


def setup_metrics(app):
    instrumentator = Instrumentator(
        should_group_status_codes=False,
        should_ignore_untemplated=True,
        should_respect_env_var=True,
        should_instrument_requests_inprogress=True,
        excluded_handlers=["/metrics"]
    )
    
    @app.get("/metrics")
    async def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    instrumentator.instrument(app)

    @app.middleware("http")
    async def metrics_middleware(request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        return response
    
    return instrumentator
