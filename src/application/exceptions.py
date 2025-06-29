class ApplicationException(Exception):
    """Base class for every custom Exception"""
    @property
    def message(self):
        return self.args[0]


class ProfileNotFoundError(ApplicationException):
    pass

class TalentAlreadyExistsError(ApplicationException):
    pass

class TalentNotFoundError(ApplicationException):
    pass