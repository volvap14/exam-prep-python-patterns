# Паттерн Memento

---
## Что делает паттерн Memento?

Memento- это поведенческий паттерн проектирования, который позволяет сохранять и восстанавливать предыдущее состояние объекта без раскрытия деталей его реализации

Основная цель:
- Сохранение состояния объекта
- Возможность отката к предыдущим состояниям 
- Инкапсуляция деталей состояния

---
## Проблема
Ситуации, когда нужен Memento:
- Необходимость реализовать механизм отмены операций (undo)
- Требуется сохранять состояние объекта для последующего восстановления
- Прямой доступ к состоянию объекта нарушает инкапсуляцию

Примеры:
- Текстовый редактор с историей изменений
- Игры с возможностью сохранения/загрузки
- Финансовые транзакции с откатом

---
## Решение

Структура паттерна:
- Originator - создает снимки своего состояния
- Memento - хранит состояние Originator
- Caretaker - управляет историей снимков

Key принцип: Originator создает Memento с текущим состоянием и может восстановить состояние из Memento.

---
### Диаграмма классов

```[Originator]
|-> createMemento()
|-> restore(memento)

[Memento]
|- state
|+ getState()

[Caretaker]
|- mementos[]
|+ addMemento()
|+ getMemento()
```

---
### Преимущества

- Сохраняет инкапсуляцию
- Упрощает создание механизма отмены 
- Позволяет хранить историю состояний 
- Разделяет ответственность за сохранение состояния

---
### Недостатки

- Может потреблять много памяти при частых сохранениях
- Усложняет код дополнительными классами 
- Originator должен раскрывать достаточно информации для Memento

---
### Применение

Типичные сценарии использования:
- Редакторы (текст, графика) с undo/redo
- Игровые сохранения
- Транзакционные системы
- Системы контроля версий

---
### Пример кода
```
from typing import List
from dataclasses import dataclass

@dataclass
class TextEditorMemento:
    def __init__(self):
        self._text = ""
    
    @property
    def text(self) -> str:
        return self._next
    
    @text.setter
    def text(self, value: str) -> None:
        self._text = value
    
    def save(self) -> TextEditorMemento:
        return TextEditorMemento(self._text)
    
    def restore(self, memento: TextEditorMemento) -> None:
        self._text = memento.text

class History:
    def __init__(self):
        self._mementos: List[TextEditorMemento] = []
    
    def save(self, memento: TextEditorMemento) -> None:
        self._mementos.append(memento)
    
    def undo(self) -> TextEditorMemento:
        if not self._mementos:
            raise ValueError("Нет сохраненных состояний")
        return self._mementos.pop()
```

---
### Альтернативы

Другие подходы:
- Command + undo operations
- Prototype для клонирования состояния
- Сериализация объекта

---
### Заключение

Memento - мощный паттерн для:

Реализации механизмов отмены

Сохранения и восстановления состояния

Поддержки истории изменений

Используйте, когда важно сохранять состояния объектов без нарушения инкапсуляции.
