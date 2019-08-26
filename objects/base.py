import inspect


class Base(object):
    def to_dict(self):
        attributes = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
        return dict([a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))])
