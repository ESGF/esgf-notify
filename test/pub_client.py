import requests

class publisherClient(object):

    def __init__(self, cert_fn, hostname):

        self.certFile = cert_fn
        self.keyFile = cert_fn

        urlbase = 'https://{}/esg-search/ws'.format(hostname)

        retractUrl = '{}/retract'.format(urlbase)
        updateUrl = '{}/update'.format(urlbase)
        publishUrl = '{}/publish'.format(urlbase)


    def publish(self, xmldata):

        try:
            response = requests.post(self.publishUrl, data=xmldata, cert=(self.certFile, self.keyFile), verify=False, allow_redirects=True)
        except requests.exceptions.SSLError, e:
            print("error!", e )

    def update(self, xmldata):

        try:
            response = requests.post(self.retractUrl, data=xmldata, cert=(self.certFile, self.keyFile), verify=False, allow_redirects=True)
        except requests.exceptions.SSLError, e:
            print("error!", e )

    def retract(self, object_id):
        data = { 'id' : object_id }

        try:
            response = requests.post(self.retractUrl, data=data, cert=(self.certFile, self.keyFile), verify=False, allow_redirects=True)
        except requests.exceptions.SSLError, e:
            print("error!", e )

        # root = etree.fromstring(response.content)
        # text = root[0].text
        # return (response.status_code, text)