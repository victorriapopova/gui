"""
Класс календаря - хранит события.
он умеет искать все события из промежутка (в том числе повторяющиеся)
он умеет добавлять/удалять события.
У каждого календаря ровно один пользователь.

"""
from datetime import date, timedelta
from typing import Optional
import unittest


def is_event_in_range(event, start_date: date, end_date: date) -> bool:
    # Проверка, попадает ли событие в заданный промежуток
    event_date = event.date
    repeat_days: Optional[int] = getattr(event, 'repeat', None)

    if not repeat_days:
        return start_date <= event_date <= end_date
    else:
        current_date = start_date
        while current_date <= end_date:
            if current_date == event_date:
                return True
            current_date += timedelta(days=repeat_days)
        return False


# Аннотации для параметров и возвращаемых значений
class Calendar:
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        self.events = []

    def add_event(self, event) -> None:
        # Добавление события
        self.events.append(event)

    def remove_event(self, event) -> None:
        # Удаление события
        if event in self.events:
            self.events.remove(event)

    def find_events_in_range(self, start_date: date, end_date: date):
        # Поиск событий в заданном промежутке
        found_events = []
        for event in self.events:
            if is_event_in_range(event, start_date, end_date):
                found_events.append(event)
        return found_events

    def pack(self):
        pass

    def bind(self, param, show_selected_date_events):
        pass

    def get_date(self):
        pass


# Переходим к тестам
class TestCalendar(unittest.TestCase):
    def setUp(self):
        self.calendar = Calendar(user_id=5)

    def test_add_and_remove_event(self):
        event = {"name": "Event 5", "date": date.today()}

        # Добавляем событие
        self.calendar.add_event(event)
        self.assertIn(event, self.calendar.events)

        # Удаляем событие
        self.calendar.remove_event(event)
        self.assertNotIn(event, self.calendar.events)

    def test_find_events_in_range(self):
        today = date.today()
        tomorrow = today + timedelta(days=1)
        yesterday = today - timedelta(days=1)

        event_in_range = {"name": "Event in Range", "date": today}
        event_out_of_range = {"name": "Event out of Range", "date": yesterday}

        self.calendar.add_event(event_in_range)
        self.calendar.add_event(event_out_of_range)

        # Ищем события в заданном промежутке
        found_events = self.calendar.find_events_in_range(today, tomorrow)

        # Проверяем, что только event_in_range попадает в заданный промежуток
        self.assertIn(event_in_range, found_events)
        self.assertNotIn(event_out_of_range, found_events)


class TestCalendar1(unittest.TestCase):
    def setUp(self):
        self.calendar = Calendar(user_id=5)

    def test_add_and_remove_event(self):
        event = {"name": "Event 1", "date": date.today()}

        # Добавляем событие
        self.calendar.add_event(event)
        self.assertIn(event, self.calendar.events)

        # Удаляем событие
        self.calendar.remove_event(event)
        self.assertNotIn(event, self.calendar.events)

    def test_find_events_in_range(self):
        today = date.today()
        tomorrow = today + timedelta(days=1)
        yesterday = today - timedelta(days=1)

        event_in_range = {"name": "Event in Range", "date": today}
        event_out_of_range = {"name": "Event out of Range", "date": yesterday}
        event_recurring = {"name": "Recurring Event", "date": today, "repeat": 7}  # Повторяющееся событие каждые 7 дней

        self.calendar.add_event(event_in_range)
        self.calendar.add_event(event_out_of_range)
        self.calendar.add_event(event_recurring)

        # Ищем события в заданном промежутке
        found_events = self.calendar.find_events_in_range(today, tomorrow)

        # Проверяем, что только event_in_range и event_recurring попадают в заданный промежуток
        self.assertIn(event_in_range, found_events)
        self.assertNotIn(event_out_of_range, found_events)
        self.assertIn(event_recurring, found_events)


if __name__ == '__main__':
    unittest.main()

if __name__ == '__main__':
    unittest.main()
