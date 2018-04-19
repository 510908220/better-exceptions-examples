# [better-exceptions](https://github.com/Qix-/better-exceptions)

介绍这个库前,我们先看一个简单的例子(example.py),代码如下:

```python
# -*- encoding: utf-8 -*-

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
```

运行输出:

```python
Traceback (most recent call last):
  File "example.py", line 24, in <module>
    get_student_infos(exam_logs)
  File "example.py", line 7, in get_student_infos
    name, catgory, grade = log.split(' ')
ValueError: not enough values to unpack (expected 3, got 2)
```



如果我们给`example.py`增加一行代码`import better_exceptions`,使用前需要执行:

- `pip install better_exceptions`

- ```bash
  export BETTER_EXCEPTIONS=1  # Linux / OSX
  setx BETTER_EXCEPTIONS 1    # Windows
  最好是加入到系统环境变量里
  或者
  import better_exceptions; 
  better_exceptions.hook()
  ```

再执行,输入如下:

```python
Traceback (most recent call last):
  File "example_with_better_exceptions.py", line 25, in <module>
    get_student_infos(exam_logs)
    │                 └ ['zhangsan math 60', 'lisi english 80', 'wangwu chinese 90', 'qianliu music']
    └ <function get_student_infos at 0x7fa594d1fe18>
  File "example_with_better_exceptions.py", line 8, in get_student_infos
    name, catgory, grade = log.split(' ')
    │     │        │       └ 'qianliu music'
    │     │        └ '90'
    │     └ 'chinese'
    └ 'wangwu'
ValueError: not enough values to unpack (expected 3, got 2)

```

看到了吗,加上`import better_exceptions`后, 异常时会将调用栈每一层用的变量值打印出来, 和普通异常时输出有比有什么好处呢,然我们来回忆一下,

- 没有`better_exceptions`时是这样对待异常的:
  - 看到一个异常,  能看到异常的类型, 但是无法直接给出错误原因
  - 追踪异常时, 往往得修改代码,将关键变量打印出来. 如果是线上环境, 貌似没什么好办法,只能上线上改一改.
- 有`better_exceptions`时:
  - 从异常时打印出来的信息可以清晰的看到异常发生时变量的值,可很容易定位问题.



是不是有小伙伴会想, 要是某些变量特别大(比如有几万个元素的列表),这样会造成日志很大的.确实存在这样的问题,不过这个库的作者已经够给解决方案了: 加上这句`better_exceptions.MAX_LENGTH = 字符数`控制字符的个数, 对于上面的例子加上`better_exceptions.MAX_LENGTH = 20`这句输出如下:

```python
Traceback (most recent call last):
  File "example_with_better_exceptions_limit_length.py", line 25, in <module>
    get_student_infos(exam_logs)
    │                 └ ['zha...
    └ <func...
  File "example_with_better_exceptions_limit_length.py", line 8, in get_student_infos
    name, catgory, grade = log.split(' ')
    │     │        │       └ 'qian...
    │     │        └ '90'
    │     └ 'chin...
    └ 'wang...
ValueError: not enough values to unpack (expected 3, got 2)

```



看到了吗,只是简单的再代码上加上一句`import better_exceptions`就有如此神奇的效果.  但是, 这个库目前只会在控制台打印出这样的错误信息,   下面说一下怎么与logging、django集成.



##  logging接入

先简单说一下,:

- logging模块在输出一个异常的时候,会调用`handler`的`formater`的`formatException`函数来格式化异常.
- `better_exceptions`有个`format_exception`方法会将异常调用栈变量值输出,就是 上面例子的那种输出.



看代码:

```python
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
```

查看`example.log`文件输出:

```python
2018-04-18 14:12:17,751 - root - ERROR - not enough values to unpack (expected 3, got 2)
Traceback (most recent call last):
  File "better_exceptions_with_logging.py", line 36, in <module>
    get_student_infos(exam_logs)
    │                 └ ['zhangsan math 60', 'lisi english 80', 'wangwu chinese 90', 'qianliu music']
    └ <function get_student_infos at 0x7f5c28d088c8>
  File "better_exceptions_with_logging.py", line 18, in get_student_infos
    name, catgory, grade = log.split(' ')
    │     │        │       └ 'qianliu music'
    │     │        └ '90'
    │     └ 'chinese'
    └ 'wangwu'
ValueError: not enough values to unpack (expected 3, got 2)

```



## django接入

思路和`logging接入`一样的. 例如有如下`django`项目:

```
☁  test_better_exceptions_django  tree
.
├── db.sqlite3
├── manage.py
└── test_better_exceptions_django
    ├── fm.py
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── views.py
    └── wsgi.py
```

两处修改:

- 增加一个`fm.py`文件:

  ```python
  import logging
  from better_exceptions import format_exception
  class ExceptionFormatter(logging.Formatter):
      def formatException(self, ei):
          return format_exception(*ei)
  ```

- 修改`settings.py`的LOGGING配置:

  ```python
  LOGGING = {
      'version': 1,
      'disable_existing_loggers': True,
      'formatters': {
          'simple': {
              '()': 'test_better_exceptions_django.fm.ExceptionFormatter',
              'format': '%(levelname)s %(message)s'
          },
      },
      'handlers': {
          'console': {
              'level': 'INFO',
              'class': 'logging.StreamHandler',
              'formatter': 'simple'
          },
          'file': {
              'level': 'ERROR',
              'class': 'logging.FileHandler',
              'filename': os.path.join(BASE_DIR, "error.log"),
              'formatter': 'simple'

          }
      },
      'loggers': {
          'django': {
              'handlers': ['console', 'file'],

          }
      }
  }
  ```

  这里主要是自定义了一个`formatters`.



我是在请求里故意出发了一个异常,代码如下:

- urls.py:

  ```python
  from django.conf.urls import url
  from django.contrib import admin
  from . import views

  urlpatterns = [
      url(r'^$', views.index, name='index'),
  ]

  ```

- views.py:

  ```python
  from django.http import HttpResponse
  import logging
  logger = logging.getLogger('django')
  def index(request):
      a, b = 2, 0
      try:
          a / b
      except Exception as e:
          logger.exception(e)
      return HttpResponse("You have an excepion, see console and log")
  ```

  ​

接着打开浏览器,可以看到根目录下`error.log`文件内容:

```python
Traceback (most recent call last):
  File "/opt/github/better-exceptions-example/test_better_exceptions_django/test_better_exceptions_django/views.py", line 7, in index
    a / b
    │   └ 0
    └ 2
ZeroDivisionError: division by zero
```



## 说明

所有的例子都在`examples`目录下.

