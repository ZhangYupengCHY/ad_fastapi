


class Message(object):
    """处理返回的信息"""

    @staticmethod
    def __error_msg__(message):
        return {'msg':'FAIL','detail':f'{message}'}

    @staticmethod
    def folder_not_exist(path):
        return Message.__error_msg__(f'{path} is VALID.')

    @staticmethod
    def type_error(param,type):
        return Message.__error_msg__(f'{param} type is not {type}.')

    @staticmethod
    def error_msg(message):
        return Message.__error_msg__(message)

    @staticmethod
    def success():
        return 'SUCCESS'

    @staticmethod
    def fail():
        return 'FAIL'


