import os
from typing import Literal

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def iniciar_driver(driver_type: Literal["chrome", "edge"] = "chrome") -> webdriver.Remote:
    os.environ['NO_PROXY'] = 'localhost,127.0.0.1'
    os.environ['no_proxy'] = 'localhost,127.0.0.1'

    if driver_type == "edge":
        options = EdgeOptions()
        options.add_argument('--no-proxy-server')
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)

    options = ChromeOptions()
    options.add_argument('--no-proxy-server')
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)
