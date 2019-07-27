windows_size = {"ipad": "768x1024", "galaxys5": "360x640"}

CHROME75_CAPS = {
               "browserName": "chrome",
               "version": "75.0",
               "enableVNC": True,
               "enableVideo": False}


CHROME74_CAPS = {
               "browserName": "chrome",
               "version": "74.0",
               "enableVNC": True,
               "enableVideo": False}

GALAXYS5_CAPS = {
               "browserName": "chrome",
               "version": "75.0",
               "enableVNC": True,
               "enableVideo": False,
               "goog:chromeOptions": {
                                        "mobileEmulation": {
                                                            "deviceName": "Galaxy S5"
                                                            }
                                    }
                }

IPAD_CAPS = {
               "browserName": "chrome",
               "version": "75.0",
               "enableVNC": True,
               "enableVideo": False,
               "goog:chromeOptions": {
                                        "mobileEmulation": {
                                                            "deviceName": "iPad"
                                                            }
                                    }
                }

FIREFOX68_CAPS = {
                "browserName": "firefox",
                "version": "68.0",
                "enableVNC": True,
                "enableVideo": False
                }


FIREFOX67_CAPS = {
                "browserName": "firefox",
                "version": "67.0",
                "enableVNC": True,
                "enableVideo": False
                }


OPERA60_CAPS = {
                "browserName": "opera",
                "version": "60.0",
                "enableVNC": True,
                "enableVideo": False
                }


OPERA58_CAPS = {
                "browserName": "opera",
                "version": "58.0",
                "enableVNC": True,
                "enableVideo": False
                }

browsers = [(CHROME75_CAPS, "Desktop"),
            (CHROME74_CAPS, "Desktop"),
            
            (GALAXYS5_CAPS, "Chrome - мобильная симуляция"),
            
            (IPAD_CAPS, "Chrome - планшетная симуляция"),
            
            (FIREFOX68_CAPS, "Desktop"),
            (FIREFOX67_CAPS, "Desktop"),
            
            (OPERA60_CAPS, "Desktop"),
            (OPERA58_CAPS, "Desktop"),
            ]