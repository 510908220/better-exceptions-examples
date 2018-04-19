# -*- encoding: utf-8 -*-
import logging
from better_exceptions import format_exception

logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter.formatException = lambda exc_info: format_exception(*exc_info)

file_handler = logging.FileHandler("example.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_student_infos(logs):
    student_infos = []
    for log in logs:
        name, catgory, grade = log.split(' ')
        student_infos.append({
            'name': name,
            'catgory': catgory,
            'grade': grade,

        })
    return student_infos


if __name__ == '__main__':
    exam_logs = [
        'zhangsan math 60',
        'lisi english 80',
        'wangwu chinese 90',
        'qianliu music'
    ]
    try:
        get_student_infos(exam_logs)
    except Exception as e:
        logger.exception(e)
