
from seleniumwire.proxy import backend
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from seleniumwire.webdriver.request import InspectRequestsMixin
from selenium.webdriver import ChromeOptions
from selenium.webdriver import Opera as _Opera
class Opera(InspectRequestsMixin, _Opera):
    """Extends the Chrome webdriver to provide additional methods for inspecting requests."""

    def __init__(self, *args, seleniumwire_options=None, **kwargs):
        """Initialise a new Chrome WebDriver instance.

        Args:
            seleniumwire_options: The seleniumwire options dictionary.
        """
        if seleniumwire_options is None:
            seleniumwire_options = {}

        self.proxy = backend.create(
            port=seleniumwire_options.get('port', 0),
            options=seleniumwire_options
        )

        if 'port' not in seleniumwire_options:  # Auto config mode
            try:
                capabilities = dict(kwargs.pop('desired_capabilities'))
            except KeyError:
                capabilities = DesiredCapabilities.CHROME.copy()

            addr, port = self.proxy.address()

            capabilities['proxy'] = {
                'proxyType': 'manual',
                'httpProxy': '{}:{}'.format(addr, port),
                'sslProxy': '{}:{}'.format(addr, port),
                'noProxy': ','.join(seleniumwire_options.pop('exclude_hosts', []))
            }
            capabilities['acceptInsecureCerts'] = True

            kwargs['desired_capabilities'] = capabilities

        try:
            chrome_options = kwargs.pop('options')
        except KeyError:
            chrome_options = ChromeOptions()

        # Prevent Chrome from bypassing the Selenium Wire proxy
        # for localhost addresses.
        chrome_options.add_argument('proxy-bypass-list=<-loopback>')
        kwargs['options'] = chrome_options

        super().__init__(*args, **kwargs)

    def quit(self):
        self.proxy.shutdown()
        super().quit()