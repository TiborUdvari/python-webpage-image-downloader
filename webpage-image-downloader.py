from HTMLParser import HTMLParser
import urllib2
import urlparse
import os


def is_absolute(url):
    return bool(urlparse.urlparse(url).netloc)


def get_domain(url):
    parsed_uri = urlparse.urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain


def download_image(img_url, local_path='downloads'):
    try:
        if not os.path.exists(local_path):
            os.makedirs(local_path)

        if len(urlparse.urlparse(img_url).scheme) < 3:
            img_url = "http:" + img_url

        img = urllib2.urlopen(img_url)
        img_name = img_url.split('/')[-1]
        with open(local_path + '/' + img_name, 'wb') as localFile:
            localFile.write(img.read())
    except Exception as e:
        print "Failed to download " + img_url + " because of " + str(e)
        print "the scheme is " + urlparse.urlparse(img_url).scheme
        pass


class ImageParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.imageURLs = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.imageURLs.append(dict(attrs)["src"])

if __name__ == "__main__":
    parser = ImageParser()

    pageAddress = raw_input("Please enter the page you want to scrape for images (with protocol): ")
    baseAddress = get_domain(pageAddress)

    response = urllib2.urlopen(pageAddress)
    page_source = response.read()

    parser.feed(page_source)

    for imgAddr in parser.imageURLs:
        if not is_absolute(imgAddr):
            imgAddr = baseAddress + '/' + imgAddr
        download_image(imgAddr)