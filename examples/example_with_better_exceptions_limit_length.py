# -*- encoding: utf-8 -*-

import better_exceptions
better_exceptions.MAX_LENGTH = 5
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
    get_student_infos(exam_logs)
