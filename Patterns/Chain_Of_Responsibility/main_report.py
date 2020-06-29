#------------------------------------------------------------------------------
# Chain Of Responsibility | Behavioral Design Pattern
#------------------------------------------------------------------------------
#
# The Chain Of Responsibility Pattern is used to achieve loose coupling in
# programs where a specified request from the client is passed through a chain
# of objects, where it is unknown which object will handle the request.
#
# - In this example we have a Report Object that is passed along a chain of
#   handlers, one that handles PDF reports another that handles Text repoorts.
#   There are just 2 handlers for illustration but there could be more.
# - We use a class to enumerate some constants which define a Report, and then
#   refer to these constants in the handler request check conditional to
#   determine whether to pass or play.
# - We also use a class to define a terminator in the chain which errors
#   whenever a request cannot be handled.


class ReportFormat(object):
    PDF = 0
    TEXT = 1


class Report(object):
    def __init__(self, format_):
        self.title = 'Monthly report'
        self.text = ['Things are going', 'really, really well.']
        self.format_ = format_


class Handler(object):
    def __init__(self):
        self.nextHandler = None

    def handle(self, request):
        self.nextHandler.handle(request)


class PDFHandler(Handler):

    def handle(self, request):
        if request.format_ == ReportFormat.PDF:
            self.output_report(request.title, request.text)
        else:
            super(PDFHandler, self).handle(request)


    def output_report(self, title, text):
        print '<html>'
        print ' <head>'
        print ' <title>%s</title>' % title
        print ' </head>'
        print ' <body>'
        for line in text:
            print ' <p>%s ' % line
            print ' </body>'
            print '</html>'


class TextHandler(Handler):

    def handle(self, request):
        if request.format_ == ReportFormat.TEXT:
            self.output_report(request.title, request.text)
        else:
            super(TextHandler, self).handle(request)

    def output_report(self, title, text):
        print 5 * '*' + title + 5 * '*'
        for line in text:
            print line


class ErrorHandler(Handler):
    def handle(self, request):
        print "Invalid request"


#------------------------------------------------------------------------------
# Client Code

def main():

    #report = Report(ReportFormat.PDF)
    report = Report(ReportFormat.TEXT)

    pdf_handler = PDFHandler()
    txt_handler = TextHandler()

    pdf_handler.nextHandler = txt_handler
    txt_handler.nextHandler = ErrorHandler()
    pdf_handler.handle(report)


if __name__ == '__main__':
    main()



