from datetime import timedelta
def timedelta_to_hhmm(td: timedelta) -> str:
    """
    Преобразует timedelta в строку формата HH:MM.
    :param td: Объект timedelta
    :return: Строка в формате HH:MM
    """
    total_seconds = int(td.total_seconds())  # Общее количество секунд
    hours = total_seconds // 3600  # Получаем часы
    minutes = (total_seconds % 3600) // 60  # Получаем минуты
    return f"{hours:02d}:{minutes:02d}"