from handlers.base import BaseHandler


class FrontPage(BaseHandler):
    def get(self):
        self.tv['content'] = "Hello world! :)"
        self.render('front.html')
        