from typing import Optional

from pydantic import BaseModel, Field, field_validator


class BaseLogSchema(BaseModel):
    name: str                                               # Name of the logger (logging channel)
    level_name: str                                         # Text logging level for the message ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

    module: str                                             # Module (name portion of filename)
    func_name: str                                          # Function name
    filename: str                                           # Filename portion of pathname
    pathname: Optional[str]                                 # Full pathname of the source file where the logging call was issued (if available)

    timestamp: str = Field(..., alias='@timestamp')  # Logging time
    thread_id: Optional[int] = None                         # Thread ID (if available)
    process_id: Optional[int] = None                        # Process ID (if available)

    message: str                                            # The result of record.getMessage(), computed just as the record is emitted

    app_name: str                                           # Application name
    app_version: str                                        # Application version
    app_env: str                                            # Application environment ("DEV", "LOCAL", "PROD")
    duration: int                                           # Duration

    exceptions: Optional[list[str] | str] = None            # Exception text

    class Config:
        populate_by_name = True


class RequestLogSchema(BaseModel):
    request_uri: str
    request_referer: str
    request_method: str
    request_path: str
    request_host: str
    request_size: int
    request_content_type: str
    request_headers: dict
    request_body: Optional[str]
    request_direction: str
    response_status_code: int
    response_size: int
    response_headers: dict
    response_body: Optional[str]
    duration: int

    @classmethod
    @field_validator(
        "request_body",
        "response_body"
    )
    def valid_body(cls, field):
        if isinstance(field, bytes):
            try:
                field = field.decode()
            except UnicodeDecodeError:
                field = b'file_bytes'
            return field

        if isinstance(field, str):
            return field
