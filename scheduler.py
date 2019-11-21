from config import *
from multiprocessing import Process
from generator import GushiwenCookieGenerator
from tester import ValidTester
from api import app
import time


class Scheduler(object):
    @staticmethod
    def valid_cookie(cycle=CYCLE):
        while True:
            print('Checking Cookies')
            try:
                tester = ValidTester()
                tester.test()
                print('Tester Finished')
                del tester
                time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def generate_cookie(cycle=CYCLE):
        while True:
            print('Generating Cookies')
            try:
                generator = GushiwenCookieGenerator()
                generator.run()
                print('Generator Finished')
                generator.close()
                print('Deleted Generator')
                time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def api():
        app.run(host=API_HOST, port=API_PORT)

    def run(self):
        if GENERATOR_PROCESS:
            generate_process = Process(target=Scheduler.generate_cookie)
            generate_process.start()

        if VALID_PROCESS:
            valid_process = Process(target=Scheduler.valid_cookie)
            valid_process.start()

        if API_PROCESS:
            api_process = Process(target=Scheduler.api)
            api_process.start()
            
if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.run()