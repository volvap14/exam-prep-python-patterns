import streamlit as st
import datetime
import os
import reveal_slides as rs

st.set_page_config(page_title="Memento", layout="wide")
st.header("📘 Презентация: Паттерн Memento")

slide_path = os.path.join("memento", "slide1.md")
if os.path.exists(slide_path):
    with open(slide_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
    rs.slides(
        markdown_content,
        height=600,
        theme="serif",
        config={
            "transition": "slide",
            "controls": True,
            "progress": True,
        },
        key="memento_slides"
    )
else:
    st.error(f"Слайды не найдены: {slide_path}")

# Классы паттерна Memento
class DocumentMemento:
    def __init__(self, content, date):
        self._content = content
        self._date = date

    @property
    def content(self):
        return self._content

    @property
    def date(self):
        return self._date.strftime("%Y-%m-%d %H:%M:%S")

class Document:
    """Originator - создает и хранит состояния"""
    def __init__(self):
        self._content = ""
        self._font = "Arial"
        self._font_size = 12

    def write(self, text):
        self._content += text

    def save(self):
        return DocumentMemento(self._content, datetime.datetime.now())

    def restore(self, memento):
        self._content = memento.content

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

class History:
    """Caretaker - управляет историей состояний"""
    def __init__(self):
        self._mementos = []

    def push(self, memento):
        self._mementos.append(memento)

    def pop(self):
        if len(self._mementos) > 0:
            return self._mementos.pop()
        return None

    def get_history(self):
        return [(m.date, m.content[:30] + "..." if len(m.content) > 30 else m.content)
                for m in self._mementos]

# Инициализация состояния
if 'doc' not in st.session_state:
    st.session_state.doc = Document()
    st.session_state.history = History()

# UI редактора
st.subheader("✍️ Текстовый редактор")

# Используем ключ для text_area, который будет обновляться при восстановлении
if 'editor_key' not in st.session_state:
    st.session_state.editor_key = 0

content = st.text_area(
    "Содержание документа:",
    value=st.session_state.doc.content,
    height=200,
    key=f"editor_{st.session_state.editor_key}"  # Динамический ключ
)

col1, col2 = st.columns(2)
with col1:
    if st.button("💾 Сохранить состояние"):
        st.session_state.doc.content = content  # Сохраняем текущее содержимое
        memento = st.session_state.doc.save()
        st.session_state.history.push(memento)
        st.success(f"Сохранено состояние от {memento.date}")

with col2:
    if st.button("⏪ Восстановить предыдущее"):
        memento = st.session_state.history.pop()
        if memento:
            st.session_state.doc.restore(memento)
            st.session_state.editor_key += 1  # Изменяем ключ для пересоздания виджета
            st.rerun()
        else:
            st.warning("История изменений пуста!")

if st.button("🔄 Обновить текст"):
    st.session_state.doc.content = content
    st.rerun()

# Отображение истории
st.subheader("🕰️ История изменений")
history_data = st.session_state.history.get_history()

if history_data:
    for i, (date, content_preview) in enumerate(reversed(history_data), 1):
        st.write(f"{i}. {date}: {content_preview}")
else:
    st.info("История изменений пока пуста")

with st.expander("Код программы"):
    st.markdown("""
    
    class DocumentMemento:
    
        def __init__(self, content, date):
            self._content = content
            self._date = date
    
        @property
        def content(self):
            return self._content
    
        @property
        def date(self):
            return self._date.strftime("%Y-%m-%d %H:%M:%S")

    class Document:

        'Originator - создает и хранит состояния'
        def __init__(self):
            self._content = ""
            self._font = "Arial"
            self._font_size = 12
    
        def write(self, text):
            self._content += text
    
        def save(self):
            return DocumentMemento(self._content, datetime.datetime.now())
    
        def restore(self, memento):
            self._content = memento.content
    
        @property
        def content(self):
            return self._content
    
        @content.setter
        def content(self, value):
            self._content = value

    class History:

        def __init__(self):
            self._mementos = []
    
        def push(self, memento):
            self._mementos.append(memento)
    
        def pop(self):
            if len(self._mementos) > 0:
                return self._mementos.pop()
            return None
    
        def get_history(self):
            return [(m.date, m.content[:30] + "..." if len(m.content) > 30 else m.content)
                    for m in self._mementos]

    """)
