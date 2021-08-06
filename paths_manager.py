from os import listdir
from datetime import date


storage_dir = 'storage'

class PathsManager():
    def __init__(self, storage_path):
        self.dir = storage_path


    # возвращает отсортированный список дат из названий файлов
    def get_last_dates(self, period=0):
        onlyfiles = [f[:-5] for f in listdir(self.dir) if f.endswith('.html')]
        file_dates = []
        for file in onlyfiles:
            day, month, year = map(int, file.split('.'))
            file_dates.append(date(day=day, month=month, year=year))
        file_dates = sorted(file_dates)
        return [d.strftime('%d.%m.%Y') for d in file_dates][-period:]


# print(PathsManager(storage_dir).get_last_dates(6))