class S3BucketAlreadyExists(Exception):
    """Exception raised for custom error in the application."""

    def __init__(self, message, error_code):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
      
    def __str__(self):
        return f"{self.message} (Error Code: {self.error_code})"