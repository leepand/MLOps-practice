from werkzeug.wsgi import ClosingIterator

class AfterResponse:
    '''中间件的应用程序扩展的封装
    '''
    def __init__(self, app):
        self.callbacks = []
        
        # 安装扩展
        app.after_response = self
        
        # 安装中间件
        app.wsgi_app = AfterResponseMiddleware(app.wsgi_app, self)
    def __call__(self, callback):
        self.callbacks.append(callback)
        return callback
    def flush(self):
        for fn in self.callbacks:
            fn()
class AfterResponseMiddleware:
    '''WSGI中间件返回`ClosingIterator`与回调函数
    '''
    def __init__(self, application, after_response_ext):
        self.application = application
        self.after_response_ext = after_response_ext
    def __call__(self, environ, after_response):
        iterator = self.application(environ, after_response)
        try:
            return ClosingIterator(iterator,
                                  [self.after_response_ext.flush])
        except:
            return iterator
