"""
TG_WINDOWS_Proxy_by_SANYA
Modern dark theme Telegram WS Proxy
"""

import toga
from toga import validators
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
from concurrent.futures import Future
import webbrowser
import sys
import os
import threading
import asyncio

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import proxy_backend.tg_ws_proxy_NEW as backend


class TGWindowsProxyBySanya(toga.App):
    """Modern Telegram WS Proxy for Windows"""

    port = 1080
    host = "127.0.0.1"
    dc_ip = ["2:149.154.167.220", "4:149.154.167.220"]
    proxy_launched = False
    proxy_task = None
    stop_event = None
    completion_future = Future()

    def __init__(self, *args, **kwargs):
        kwargs['formal_name'] = 'TG_WINDOWS_Proxy_by_SANYA'
        kwargs['app_id'] = 'com.sanya.tgwswindowsproxy'
        super().__init__(*args, **kwargs)

    def stop_proxy(self):
        if self.proxy_launched:
            # Устанавливаем событие остановки
            if self.stop_event:
                self.stop_event.set()
            self.proxy_launched = False

            self.status_dot.text = '●'
            self.status_dot.style.background_color = '#ef4444'
            self.status_label.text = 'Остановлен'
            self.status_label.style.color = '#ef4444'

            self.main_btn.text = '⚡ Запустить прокси'
            self.main_btn.style.background_color = '#6366f1'

            print("PROXY OFF")

    def apply_dcip(self, widget):
        self.dc_ip = widget.value.split(";")

    def apply_port(self, widget):
        try:
            self.port = int(widget.value)
        except ValueError:
            pass

    def apply_host(self, widget):
        self.host = widget.value

    def run_proxy_async(self):
        """Запуск прокси в asyncio event loop"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Создаем threading.Event для остановки
            self.stop_event = threading.Event()
            
            # Создаем asyncio.Event и синхронизируем их
            async_stop = asyncio.Event()
            
            # Фоновая задача для проверки threading.Event
            async def check_stop():
                while not self.stop_event.is_set():
                    await asyncio.sleep(0.1)
                async_stop.set()
            
            # Запускаем задачу проверки
            check_task = loop.create_task(check_stop())
            
            # Создаем и запускаем задачу прокси
            command = ["--host", self.host, "--port", str(self.port)]
            for ip in self.dc_ip:
                command.append("--dc-ip")
                command.append(ip)
            
            # Запускаем прокси
            proxy_task = loop.create_task(
                backend._run(self.port, backend.parse_dc_ip_list(self.dc_ip), 
                           async_stop, self.host)
            )
            
            # Ждем завершения
            loop.run_until_complete(proxy_task)
            
        except Exception as e:
            print(f"Proxy error: {e}")
        finally:
            self.proxy_launched = False
            try:
                # Отменяем все задачи
                for task in asyncio.all_tasks(loop):
                    task.cancel()
                loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(loop), return_exceptions=True))
                loop.close()
            except:
                pass

    async def toggle_proxy(self, widget):
        if not self.proxy_launched:
            self.apply_dcip(self.dcip_input)
            self.apply_port(self.port_input)
            self.apply_host(self.host_input)

            try:
                # Запускаем в отдельном потоке с asyncio event loop
                self.proxy_thread = threading.Thread(
                    target=self.run_proxy_async,
                    daemon=True
                )
                self.proxy_thread.start()
                self.proxy_launched = True

                self.status_dot.text = '●'
                self.status_dot.style.background_color = '#22c55e'
                self.status_label.text = 'Активен'
                self.status_label.style.color = '#22c55e'

                self.main_btn.text = '⏹ Остановить прокси'
                self.main_btn.style.background_color = '#ef4444'

                print("PROXY ON")
            except Exception as e:
                self.main_window.info_dialog(
                    "Ошибка",
                    f"Не удалось запустить прокси:\n{str(e)}"
                )
                self.proxy_launched = False
        else:
            self.stop_proxy()

    def open_telegram(self, widget):
        host_value = '127.0.0.1' if self.host == '0.0.0.0' else self.host
        url = f"https://t.me/socks?server={host_value}&port={self.port}"
        webbrowser.open(url)

    def startup(self):
        backend.appclass = self
        
        # Главный контейнер
        main_box = toga.Box()
        main_box.style.background_color = '#09090b'
        main_box.style.padding = 0
        main_box.style.direction = COLUMN
        
        # Верхняя панель с заголовком
        header_box = toga.Box()
        header_box.style.background_color = '#09090b'
        header_box.style.padding = 30
        header_box.style.direction = COLUMN
        
        title = toga.Label('TG WINDOWS PROXY', font_size=28, font_weight='bold')
        title.style.color = '#ffffff'
        title.style.margin_bottom = 5
        
        subtitle = toga.Label('by SANYA', font_size=14)
        subtitle.style.color = '#a855f7'
        
        header_box.add(title)
        header_box.add(subtitle)
        
        # Блок статуса
        status_box = toga.Box()
        status_box.style.background_color = '#18181b'
        status_box.style.margin_left = 30
        status_box.style.margin_right = 30
        status_box.style.margin_bottom = 25
        status_box.style.padding = 20
        status_box.style.direction = ROW
        status_box.style.align_items = CENTER
        status_box.style.border_radius = 12
        
        self.status_dot = toga.Label('●', font_size=20)
        self.status_dot.style.color = '#ef4444'
        self.status_dot.style.margin_right = 12
        
        self.status_label = toga.Label('Остановлен', font_size=16, font_weight='bold')
        self.status_label.style.color = '#ef4444'
        
        status_box.add(self.status_dot)
        status_box.add(self.status_label)
        
        # Контейнер для полей ввода
        inputs_container = toga.Box()
        inputs_container.style.padding_left = 30
        inputs_container.style.padding_right = 30
        inputs_container.style.direction = COLUMN
        inputs_container.style.gap = 20
        
        # Поле хоста
        host_label = toga.Label('Хост', font_size=12, font_weight='bold')
        host_label.style.color = '#a1a1aa'
        host_label.style.margin_bottom = 8
        
        self.host_input = toga.TextInput(placeholder='127.0.0.1')
        self.host_input.value = '127.0.0.1'
        self.style_input_field(self.host_input)
        
        host_wrapper = toga.Box()
        host_wrapper.style.direction = COLUMN
        host_wrapper.add(host_label)
        host_wrapper.add(self.host_input)
        
        # Поле порта
        port_label = toga.Label('Порт', font_size=12, font_weight='bold')
        port_label.style.color = '#a1a1aa'
        port_label.style.margin_bottom = 8
        
        self.port_input = toga.TextInput(placeholder='1080')
        self.port_input.value = '1080'
        self.style_input_field(self.port_input)
        
        port_wrapper = toga.Box()
        port_wrapper.style.direction = COLUMN
        port_wrapper.add(port_label)
        port_wrapper.add(self.port_input)
        
        # Поле DC IP
        dcip_label = toga.Label('DC IP (через ;)', font_size=12, font_weight='bold')
        dcip_label.style.color = '#a1a1aa'
        dcip_label.style.margin_bottom = 8
        
        self.dcip_input = toga.TextInput(placeholder='2:149.154.167.220;4:149.154.167.220')
        self.dcip_input.value = '2:149.154.167.220;4:149.154.167.220'
        self.style_input_field(self.dcip_input)
        
        dcip_wrapper = toga.Box()
        dcip_wrapper.style.direction = COLUMN
        dcip_wrapper.add(dcip_label)
        dcip_wrapper.add(self.dcip_input)
        
        inputs_container.add(host_wrapper)
        inputs_container.add(port_wrapper)
        inputs_container.add(dcip_wrapper)
        
        # Кнопки
        buttons_box = toga.Box()
        buttons_box.style.padding_left = 30
        buttons_box.style.padding_right = 30
        buttons_box.style.padding_top = 25
        buttons_box.style.direction = COLUMN
        buttons_box.style.gap = 12
        
        self.main_btn = toga.Button('⚡ Запустить прокси', on_press=self.toggle_proxy)
        self.main_btn.style.background_color = '#6366f1'
        self.main_btn.style.color = '#ffffff'
        self.main_btn.style.border_radius = 10
        self.main_btn.style.padding_top = 16
        self.main_btn.style.padding_bottom = 16
        self.main_btn.style.font_size = 14
        self.main_btn.style.font_weight = 'bold'
        
        self.tg_btn = toga.Button('📱 Подключить Telegram', on_press=self.open_telegram)
        self.tg_btn.style.background_color = '#22c55e'
        self.tg_btn.style.color = '#ffffff'
        self.tg_btn.style.border_radius = 10
        self.tg_btn.style.padding_top = 14
        self.tg_btn.style.padding_bottom = 14
        self.tg_btn.style.font_size = 13
        
        buttons_box.add(self.main_btn)
        buttons_box.add(self.tg_btn)
        
        # Информационная панель
        info_panel = toga.Box()
        info_panel.style.background_color = '#18181b'
        info_panel.style.margin_left = 30
        info_panel.style.margin_right = 30
        info_panel.style.margin_top = 25
        info_panel.style.padding = 20
        info_panel.style.border_radius = 12
        
        info_title = toga.Label('Настройки для Telegram', font_size=12, font_weight='bold')
        info_title.style.color = '#a855f7'
        info_title.style.margin_bottom = 12
        
        info_text = toga.Label(
            'Сервер: 127.0.0.1\n'
            'Порт: 1080\n'
            'Тип: SOCKS5\n'
            'Без авторизации',
            font_size=11
        )
        info_text.style.color = '#71717a'
        info_text.style.line_height = 1.8
        
        info_panel.add(info_title)
        info_panel.add(info_text)
        
        # Собираем всё вместе
        main_box.add(header_box)
        main_box.add(status_box)
        main_box.add(inputs_container)
        main_box.add(buttons_box)
        main_box.add(info_panel)
        
        # Окно
        self.main_window = toga.MainWindow(
            title=self.formal_name,
            size=(480, 680),
        )
        self.main_window.content = main_box
        self.main_window.show()

    def style_input_field(self, widget):
        widget.style.background_color = '#27272a'
        widget.style.color = '#ffffff'
        widget.style.border_radius = 8
        widget.style.padding_top = 14
        widget.style.padding_bottom = 14
        widget.style.padding_left = 16
        widget.style.padding_right = 16
        widget.style.font_size = 14


def main():
    return TGWindowsProxyBySanya()
