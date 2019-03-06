from webwhatsapi import WhatsAPIDriver

def start():
    driver = WhatsAPIDriver(client='Chrome',
                            username='FRTNX',
                            headless=True)
    qrcode = driver.get_qr_plain()
    driver.wait_for_login()
    return {"qrcode": qrcode}
    