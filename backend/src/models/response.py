class Response:
    """
    Custom Response class that encloses success or error into a JSON.
    """

    @classmethod
    def success(cls, code=200, message="Request processed successfully", **kwargs):
        """
        Returns a formatted success JSON.
        """
        return {
            "success": True,
            "message": message,
            "code": code,
            **kwargs,
        }, code

    @classmethod
    def error(cls, code=500, message="Internal Server Error", **kwargs):
        """
        Returns a formatted error JSON.
        """
        return {"success": False, "message": message, "code": code, **kwargs}, code