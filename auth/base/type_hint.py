from typing import Dict, Literal

Field_names = str
Sorted_direction = Literal["ASC", "DESC"]
Sorted_order = Dict[Field_names, Sorted_direction]
Url = str

ALGORITHM = Literal[
    "HS256",
    "HS128",
]

METHOD = Literal[
    "HEAD",
    "OPTIONS",
    "GET",
    "POST",
    "DELETE",
    "PATCH",
    "PUT",
    "*",
]

HEADERS = Literal[
    "Accept-Encoding",
    "Content-Type",
    "Set-Cookie",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Origin",
    "Authorization",
    "*",
]

Public_access = list[tuple[Url, METHOD]]
