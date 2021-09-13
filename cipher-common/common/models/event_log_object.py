
class EventLogObject:

    log_time: str
    log_level: str
    log_module: str
    log_function: str
    log_message: str

    def __init__(self, log_time=None, log_level=None, log_module=None, log_function=None, log_message=None):
        self.log_time = log_time
        self.log_level = log_level
        self.log_module = log_module
        self.log_function = log_function
        self.log_message = log_message

    def to_dict(self):
        obj_dict = {}
        for attr, value in self.__dict__.items():
            obj_dict[attr] = value
        return obj_dict

    def to_obj(self, dict_data):
        return EventLogObject(**dict_data)
