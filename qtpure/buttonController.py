import os.path
from datetime import datetime, timedelta
from pathlib import Path
from threading import Lock
from typing import Callable, List

import moviepy.editor as mp
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QTableWidgetItem, \
    QHeaderView, QLabel

from design_second import Ui_MainWindow
from upload_task import API_URL, UploadTask


def get_video_length(path):
    duration = mp.VideoFileClip(path).duration
    return duration


def get_films_from_folder(folder: str) -> List[str]:
    # Получить все файлы из папки рекурсивно типа .mp4 .avi .mkv
    films = []
    possible_formats = ('.mp4', '.avi', '.mkv')
    for root, dirs, files in os.walk(folder):
        for file in files:
            file: str
            if file.endswith(possible_formats):
                films.append(os.path.join(root, file))

    return films




def main_function(path, new_window, ui_window: Ui_MainWindow):
    in_progress_count = 0
    finished_count = 0
    total_count = 0
    progress_lock = Lock()
    table = ui_window.tableWidget
    table.setColumnCount(5)
    table.horizontalHeader().setStretchLastSection(True)
    table.horizontalHeader().setSectionResizeMode(
        QHeaderView.Stretch)
    table.setHorizontalHeaderLabels(["Путь", "Длительность", "Состояние",
                                     "Ссылка на видео", "Ссылка на обработанное видео"])
    table.verticalHeader().setVisible(False)

    # Если path это папка
    if os.path.isdir(path):
        films_filename = get_films_from_folder(path)
    else:
        films_filename = [path]
    total_count = len(films_filename)
    lock = Lock()
    data_return = [dict() for i in range(total_count)]
    for film_num in range(total_count):
        film_path = films_filename[film_num]
        film_name = Path(film_path).name
        film_length_seconds = get_video_length(film_path)
        film_length = datetime(1, 1, 1) + timedelta(seconds=film_length_seconds)
        table.insertRow(film_num)
        table.setItem(film_num, 0, QTableWidgetItem(film_path))
        table.setItem(film_num, 1, QTableWidgetItem(film_length.strftime("%H:%M:%S")))

        # for i in range(3, 4 + 1):
        #     table.setCellWidget(film_num, i, QtWidgets.QLabel("В обработке...", openExternalLinks=True))

        def upload_progress_callback(pr: float):
            with progress_lock:
                ui_window.status.setText(
                    f"Статус выполнения: обработка... {finished_count}/{total_count}")
                table.setItem(film_num, 2, QTableWidgetItem("Обрабатывается"))
                table.setHidden(True)
                table.setHidden(False)

        def upload_finish_callback(film_id: int):
            try:
                nonlocal data_return, in_progress_count, finished_count, total_count
                with progress_lock:
                    in_progress_count -= 1
                    finished_count += 1
                    if finished_count == total_count:
                        ui_window.status.setText(
                            f"Статус выполнения: загрузка завершена")
                    else:
                        ui_window.status.setText(
                            f"Статус выполнения: обработка... {finished_count}/{total_count}")
                    ui_window.ready_count.setText(f"Готово: {finished_count}")
                    ui_window.proc_count.setText(f"В процессе: {in_progress_count}")
                    data_return[film_num]['film_id'] = film_id
                    item = table.item(film_num, 3)
                    if film_id < 1:
                        table.setItem(film_num, 2, QTableWidgetItem("Ошибка обработки"))
                    else:
                        table.setItem(film_num, 2, QTableWidgetItem("Потоковая обработка"))
                        table.setItem(film_num, 3, None)
                        label = QLabel()
                        label.setText(f"<a href='{API_URL}/api/get_video?film_id={film_id}' "
                                      f"style=\"color:black;font-size:18px\">Ссылка на видео</a>")
                        label.setOpenExternalLinks(True)
                        table.setCellWidget(film_num, 3, label)
                        label = QLabel()
                        label.setText(f"<a href='{API_URL}/api/get_video?film_id={film_id}&only_updated=1' "
                                      f"style=\"color:black;font-size:18px\">Ссылка на видео</a>")
                        label.setOpenExternalLinks(True)
                        table.setItem(film_num, 3, None)
                        table.setCellWidget(film_num, 4, label)
                    # Обновить таблицу
                    table.setHidden(True)
                    table.setHidden(False)
            except Exception as e:
                print(e)
                raise e
                # table.setCellWidget(film_num, 4, QLabel(f"<a href='http://{API_URL}/"
                #                                         f"api/get_video?film_id={film_id}&"
                #                                         f"only_updated=1'>{film_name}</a>", table))

        # upload_film(film_path, upload_progress_callback, upload_finish_callback)
        # th = threading.Thread(target=upload_film,
        #                       args=(film_path, upload_progress_callback, upload_finish_callback),
        #                       daemon=True)
        qth = UploadTask(film_path, lock)
        qth.progress_changed_signal.connect(upload_progress_callback)
        qth.finished_signal.connect(upload_finish_callback)

        with lock:
            in_progress_count += 1
        qth.start()
    ui_window.status.setText("Статус выполнения: обработка...")
    new_window.show()


    # if total_count != finished_count:
    # ui_window.status.setText("Статус выполнения: ошибка!")


def uploadController(main_window: QMainWindow, new_window: QMainWindow,
                     ui_window) -> Callable:
    try:
        def upload():
            # Допустимый выбор: папка, файл видео формата .mp4 .avi .mkv
            dialog = QFileDialog(main_window)
            dialog.setFileMode(QFileDialog.AnyFile)
            dialog.setOption(QFileDialog.DontResolveSymlinks)
            # Установка формата файлов .mp4 .avi .mkv
            dialog.setNameFilter("Video files (*.mp4 *.avi *.mkv)")
            dialog.setViewMode(QFileDialog.Detail)

            if dialog.exec_():
                path = dialog.selectedFiles()[0]
                if not path:
                    return
                main_window.setHidden(True)
                main_function(path, new_window, ui_window)

        return upload
    except Exception as e:
        print(e)
        raise e


def uploadControllerSecond(new_window: QMainWindow,
                           ui_window) -> Callable:
    def upload(path):
        main_function(path, new_window, ui_window)

    return upload
