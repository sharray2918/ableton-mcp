"""Error handling utilities for AbletonMCP Remote Script."""

import traceback


def handle_exception(logger, operation_name, exception):
    """
    Handle exceptions with consistent logging and error formatting.

    Args:
        logger: Logger instance to use for error logging
        operation_name: Name of the operation that failed
        exception: The exception that occurred

    Returns:
        dict: Error response dictionary
    """
    error_message = f"Error {operation_name}: {str(exception)}"
    logger.log_message(error_message)
    logger.log_message(traceback.format_exc())

    return {"status": "error", "message": str(exception), "operation": operation_name}


def safe_execute(logger, operation_name, func, *args, **kwargs):
    """
    Safely execute a function with error handling.

    Args:
        logger: Logger instance to use for error logging
        operation_name: Name of the operation being performed
        func: Function to execute
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function

    Returns:
        tuple: (success: bool, result: any)
    """
    try:
        result = func(*args, **kwargs)
        return True, result
    except Exception as e:
        handle_exception(logger, operation_name, e)
        return False, None


def format_error_response(message, operation=None):
    """
    Format a consistent error response.

    Args:
        message: Error message
        operation: Optional operation name

    Returns:
        dict: Formatted error response
    """
    response = {"status": "error", "message": message}
    if operation:
        response["operation"] = operation
    return response


def format_success_response(result, operation=None):
    """
    Format a consistent success response.

    Args:
        result: Result data
        operation: Optional operation name

    Returns:
        dict: Formatted success response
    """
    response = {"status": "success", "result": result}
    if operation:
        response["operation"] = operation
    return response
