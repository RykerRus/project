import pytest
from discord import Webhook, RequestsWebhookAdapter, File

def report_on_discord(message, file=None):
    print("send report ")
    
    bot_name = "Отчетов повелитель"
    
    webhook = Webhook.partial(601678713838501888,
                              'UNXBaQLPmha6jxC6TiqO353BtmIkw5IAnX_X6FyOCZEZFvPA4aIA66xFLuPSaSn-QOlg',
                              adapter=RequestsWebhookAdapter())
    webhook.send(message, username=bot_name, file=file)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    print("ВЫВОД *******************")
    count_passed = len(terminalreporter.stats.get('passed', ""))
    count_failed = len(terminalreporter.stats.get('failed', ""))
    count_skip = len(terminalreporter.stats.get('skipped', "")) + len(terminalreporter.stats.get('xfailed', ""))
    print(count_passed, count_failed, count_skip)
    print("reportchars", terminalreporter.reportchars)
    print("showlongtestinfo", terminalreporter.showlongtestinfo)
    if count_passed + count_failed + count_skip > 15:
        str_result = f"Тестирование авто-тестов на тестовом сервере \n Проект Теплолюкс \n Удачно {count_passed} Провалено {count_failed} Пропущено {count_skip}"
        # html = File("report.html", filename="report.html")
        report_on_discord(str_result)
