from datetime import datetime, timedelta

class Tracker:
    """time format %H:%M"""
    def __init__(self, current_time: str = None, user=None, daily_target: str = '08:00'):
        # Преобразуем daily_target в timedelta
        self.daily_target = datetime.strptime(daily_target, '%H:%M')
        self.daily_target = timedelta(hours=self.daily_target.hour, minutes=self.daily_target.minute)
        
        # Преобразуем current_time в timedelta, если оно передано
        if current_time:
            current_time_dt = datetime.strptime(current_time, '%H:%M')
            self.current_time = self.daily_target - timedelta(hours=current_time_dt.hour, minutes=current_time_dt.minute)
        else:
            self.current_time = self.daily_target
        
        self.user = user

    def uppload_work_time(self, work_time: str):
        """time format %H:%M"""
        # Преобразуем work_time в timedelta
        work_time_dt = datetime.strptime(work_time, '%H:%M')
        work_time_td = timedelta(hours=work_time_dt.hour, minutes=work_time_dt.minute)
        
        # Вычитаем work_time_td из current_time
        self.current_time -= work_time_td
        return self.current_time