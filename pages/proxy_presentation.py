import streamlit as st
import reveal_slides as rs
import os

st.set_page_config(page_title="Proxy", layout="wide")
st.header("📕 Презентация: Паттерн Proxy")

slide_path = os.path.join("proxy", "slide1.md")
if os.path.exists(slide_path):
    with open(slide_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
    rs.slides(
        markdown_content,
        height=600,
        theme="solarized",
        config={
            "transition": "slide",
            "controls": True,
            "progress": True
        },
        key="proxy_slides"
    )
else:
    st.error(f"Слайды не найдены: {slide_path}")

st.subheader("✏️ Пример: Прокси-доступ к банковскому счету")

class BankAccount:
    def __init__(self, balance):
        self.balance = balance

class BankAccountProxy:
    def __init__(self, real_account, password):
        self.real_account = real_account
        self.password = password

    def check_balance(self, input_password):
        if input_password == self.password:
            return self.real_account.balance
        return "Доступ запрещен"

password = st.text_input("Введите пароль:", type="password")
account = BankAccount(1000)
proxy = BankAccountProxy(account, "admin123")

if st.button("Проверить баланс"):
    result = proxy.check_balance(password)
    st.write(f"Баланс: {result}")
