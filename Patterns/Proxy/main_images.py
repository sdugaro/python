#------------------------------------------------------------------------------
# Proxy | Structural Design Pattern
#------------------------------------------------------------------------------
#
# A Proxy PAttern lets you provide a placeholder for an original object. A
# Proxy controls access to the original object, permitting additional logic to
# be inserted before or after a request gets through to the original object.
#
#
# - From the perspective of the client, there should be no difference between a
#   real service object and its proxy (stand-in body double)
# - While similar to the Facade Pattern in that both buffer a complex entity
#   and initialize them, a Proxy will have the same interface as its service
#   object which makes them interchangeable.
# - While similar to the Decorator Pattern in that both are built on the
#   composition of objects that work is delegated to, A Proxy will manage the
#   life cycle of its service object, while the composition of decorators is
#   managed by the client.
#


class Image:
    def __init__(self, filename):
        self._filename = filename

    def load_image_from_disk(self):
        print("loading " + self._filename)

    def display_image(self):
        print("display " + self._filename)


class Proxy:
    def __init__(self, subject):
        self._subject = subject
        self._proxystate = None


class ProxyImage(Proxy):
    def display_image(self):
        if self._proxystate is None:
            self._subject.load_image_from_disk()
            self._proxystate = 1
        print("display " + self._subject._filename)


#------------------------------------------------------------------------------
# Client Code

def main():

    proxy_image1 = ProxyImage(Image("HiRes_10Mb_Photo1"))
    proxy_image2 = ProxyImage(Image("HiRes_10Mb_Photo2"))

    proxy_image1.display_image()  # loading necessary
    proxy_image1.display_image()  # loading unnecessary
    proxy_image2.display_image()  # loading necessary
    proxy_image2.display_image()  # loading unnecessary
    proxy_image1.display_image()  # loading unnecessary


if __name__ == "__main__":
    main()

