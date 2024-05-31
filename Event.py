"""
Описывает некоторе "событие" - промежуток времени с присвоенными характеристиками
У события должно быть описание, название и список участников
Событие может быть единожды созданым
Или периодическим (каждый день/месяц/год/неделю)

Каждый пользователь ивента имеет свою "роль"
организатор умеет изменять названия, список участников, описание, а так же может удалить событие
участник может покинуть событие

запрос на хранение в json
Уметь создавать из json и записывать в него

Иметь покрытие тестами
Комментарии на нетривиальных методах и в целом документация
"""

import json
from datetime import date
from typing import List, Optional


class Event:
    def __init__(self, name: str, description: str, participants: List[str], start_date: date,
                 repeat: Optional[int] = None):
        # Название события
        self.name = name
        # Описание события
        self.description = description
        # Участники события
        self.participants = participants
        # Дата начала события
        self.start_date = start_date
        # Если repeat не None, то событие является периодическим
        self.repeat = repeat

        # Роль по умолчанию у создателя события - Создатель - первый участник
        self.organizer = participants[0] if participants else None

    # Метод для изменения характеристик события
    def update_event(self, user_id: str, name: Optional[str] = None, description: Optional[str] = None,
                     participants: Optional[List[str]] = None) -> bool:
        # Метод доступен только организатору события
        if user_id == self.organizer:
            if name:
                self.name = name
            if description:
                self.description = description
            if participants:
                self.participants = participants
            return True
        return False

    def delete_event(self, user_id: str) -> bool:
        # Метод для удаления события. Доступен только организатору события.
        if user_id == self.organizer:
            # Удаляем событие
            del self
            return True
        return False

    def leave_event(self, user_id: str) -> bool:
        # Метод для участника события, чтобы выйти из него.
        if user_id in self.participants and user_id != self.organizer:
            self.participants.remove(user_id)
            return True
        return False

    @property
    def to_json(self) -> str | None:
        # Метод для преобразования события в JSON формат.
        event_dict = {
            "name": self.name,
            "description": self.description,
            "participants": self.participants,
            "start_date": str(self.start_date),
            "repeat": self.repeat,
            "organizer": self.organizer
        }
        return json.dumps(event_dict)

    @classmethod
    def from_json(cls, json_str: str) -> 'Event':
        # Метод для создания объекта события из строки JSON.
        event_dict = json.loads(json_str)
        return cls(name=event_dict["name"], description=event_dict["description"],
                   participants=event_dict["participants"], start_date=date.fromisoformat(event_dict["start_date"]),
                   repeat=event_dict["repeat"])
