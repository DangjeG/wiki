from typing import Optional, Iterable


def get_html_frame(body: Optional[str | Iterable] = None) -> str:
    if isinstance(body, Iterable):
        body = "".join(body)
    return f"""<!doctype html>
<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset="UTF-8">
    <meta name="viewport"
          content="width=device-width,
                   user-scalable=no,
                   initial-scale=1.0,
                   maximum-scale=1.0,
                   minimum-scale=1.0"
    >
    <meta http-equiv="X-UA-Compatible"
          content="ie=edge"
    >
</head>
<body>
    {body or ""}
</body>
</html>
"""


def get_html_base_img_teg(src: Optional[str] = None, width: Optional[float] = 600) -> str:
    return f"""<img src="{src or ''}" width="{width or 600}">"""


def get_html_base_file(src: Optional[str] = None, filename: Optional[str] = "File") -> str:
    return f"""<a href="{src or ''}">{filename or 'File'}</a>"""
