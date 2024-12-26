import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")
        ''' Создание основного поля программы '''
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)
        ''' Данные холста'''
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()
        ''' Данные границы '''
        self.text_for_enter = ['blank', 'Arial', ' ', 'off']
        ''' Переменная текста для ввода и параметров шрифта'''
        self.setup_ui()
        ''' Установка меню управления '''
        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        ''' Установка базовых параметров кисти '''
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<Button-1>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        ''' Привязка меню управления '''
        self.is_rubber_on = False
        self.backup_color = 'white'
        ''' Задание параметров ластика '''
        self.canvas.bind('<Button-3>', self.pick_color)
        ''' Привязка функции к правой кнопке мыши '''
        self.hotkey_list_creator()
        ''' Активация списка горячих клавиш '''
        self.brush_type = 'brush'
        ''' Перменная типа отрисовываемого '''


    def setup_ui(self):
        """ Функция создания меню """
        scale_min = 1
        ''' Задание минимального размера кисти '''
        scale_max = 21
        '''  Задание максимального размера кисти '''
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)
        ''' Создание холста '''
        new_draw_button = tk.Button(control_frame, text="См. размера", command=self.window_size_choice)
        ''' Создание кнопки смены размера '''
        new_draw_button.pack(side=tk.LEFT, padx=5)
        ''' Отрисовка кнопки смены размера'''
        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        ''' Создание кнопки очистки холста '''
        clear_button.pack(side=tk.LEFT, padx=5)
        ''' Отрисовка кнопки очистки холста в меню '''
        self.text_button = tk.Button(control_frame, text="Ввести текст", command=self.text_creator)
        self.text_button.pack(side=tk.LEFT, padx=5)
        ''' Отрисовка кнопки ввода текста '''
        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        ''' Создание кнопки выбора цвета из палитры '''
        color_button.pack(side=tk.LEFT, padx=5)
        ''' Отрисовка кнопки выбора цвета в меню '''
        color_background = tk.Button(control_frame, text="Выбрать цвет фона", command=self.choose_background)
        ''' Создание кнопки выбора цвета фона '''
        color_background.pack(side=tk.LEFT, padx=5)
        ''' Отрисовка кнопки выбора цвета фона '''
        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        ''' Создание кнопки сохранения '''
        save_button.pack(side=tk.LEFT, padx=5)
        ''' Отрисовка кнопки сохранения в меню '''
        rubber_button = tk.Button(control_frame, text="Ластик", command=self.rubber_button)
        ''' Создание кнопки ластика '''
        rubber_button.pack(side=tk.LEFT, padx=5)
        ''' Отрисовка кнопки ластика в меню '''
        brush_size_menu = self.brush_size_menu(control_frame, scale_min, scale_max)
        ''' Вызов функции создания выпадающего меню '''
        brush_size_menu.config(width=5, font=("Helvetica", 12))
        ''' Отрисовка выпадающего меню '''
        brush_size_menu.pack(side=tk.LEFT, padx=5)
        ''' Установка расположения выпадающего меню в строке меню '''
        self.brush_size_scale = tk.Scale(control_frame, length=50, from_=scale_min, to=scale_max, orient=tk.HORIZONTAL)
        ''' Создание ползунка выбора размера кисти '''
        self.brush_size_scale.pack(side=tk.LEFT, padx=5)
        ''' Отрисовка ползунка выбора размера кисти '''
        brush_lable = tk.Label(control_frame, text='Brush color:', fg='#000')
        ''' Создане подписи к цвету кисти '''
        brush_lable.pack(side=tk.LEFT)
        ''' Отрисовка подписи к цвету кисти '''
        self.brush_color_lable = tk.Label(control_frame, text=' ', bg='#000')
        ''' Создание индикатора цвета кисти '''
        self.brush_color_lable.pack(side=tk.LEFT, padx=5)
        ''' Отрисовка индикатора цвета кисти '''


    def brush_color_lable_control(self, color):
        """ Функция изменения индикатора цвета кисти """
        self.brush_color_lable.config(fg=color, bg=color)
        ''' Изменение индикатора цвета кисти '''

    def hotkey_list_creator(self):
        """ Функция создания списка горячих клавиш """
        self.root.bind('<Control-c>', self.hotkey_list_action)
        ''' Горячая клавиша выбора цвета'''
        self.root.bind('<Control-s>', self.hotkey_list_action)
        ''' Горячая клавиша сохранения рисунка '''

    def hotkey_list_action(self, event):
        """ Функция описания действия горячих клавмиш """
        if event.keysym == 'c':
            self.choose_color()
            ''' Активация горячей клавиши выбора цвета '''
        elif event.keysym == 's':
            self.save_image()
            ''' Активация горячей клавиши сохранения '''

    def paint(self, event):
        """ Функция рисования кисти """
        data = [self.last_x, self.last_y, event.x, event.y]
        ''' Сохранение данных события '''
        self.brush_type_action(data)
        ''' Отрисовка по заданным параметрам '''
        self.last_x = event.x
        self.last_y = event.y
        ''' Фиксация расположения '''

    def brush_type_action(self, data):
        """ Функция отрисовки по параметрам и типу кисти """
        if self.brush_type == 'brush':
            if self.last_x and self.last_y:
                self.canvas.create_line(data[0], data[1], data[2], data[3],
                                        width=self.brush_size_scale.get(), fill=self.pen_color,
                                        capstyle=tk.ROUND, smooth=tk.TRUE)
                self.draw.line([data[0], data[1], data[2], data[3]], fill=self.pen_color,
                               width=int(self.brush_size_scale.get()))
            ''' Отрисовка карандаша '''
        elif self.brush_type == 'text':
            fontsize = self.brush_size_scale.get()
            if self.text_for_enter[2] != ' ':
                fontdata = f'{self.text_for_enter[1]} {fontsize} {self.text_for_enter[2]}'
            else:
                fontdata = f'{self.text_for_enter[1]} {fontsize}'
            self.canvas.create_text(data[2], data[3], text=self.text_for_enter[0], fill=self.pen_color,
                                    font=fontdata)
            ''' Отображение текста '''

    def reset(self, event):
        """ Функция сброса последних параметров """
        self.last_x, self.last_y = None, None
        ''' Сброс параметров '''

    def clear_canvas(self):
        """ Функция очистки холста """
        self.canvas.delete("all")
        ''' Очистка холста '''
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)
        ''' Заполнение холста белым цветом '''

    def choose_color(self):
        """ Функция выбора цвета"""
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        ''' Выбор цвета '''
        self.is_rubber_on = False
        ''' Фиксация отключения ластика '''
        self.brush_color_lable_control(self.pen_color)
        ''' Изменение индикатора цвета кисти '''

    def save_image(self):
        """ Функция сохранения изображения """
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        ''' Задача пути к файлу'''
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")
        ''' Сохранение и вывод информации об этом '''

    def rubber_button(self):
        """ Функция ластика """
        self.is_rubber_on = not self.is_rubber_on
        ''' Фиксация включения/выключения kfcnbrf '''
        if self.is_rubber_on:
            self.backup_color = self.pen_color
            self.pen_color = 'white'
        else:
            self.pen_color = self.backup_color
        ''' Установка цвета кисти'''

    def brush_size_menu(self, control_frame, scale_min, scale_max):
        """ Функция создания меню """
        optionlist = []
        if scale_max - scale_min <= 10:
            for i in range(scale_min, scale_max+1):
                optionlist.append(f'{i}')
        elif 10 < scale_max - scale_min <= 20:
            for i in range(scale_min, scale_max + 1, 2):
                optionlist.append(f'{i}')
        else:
            step = int((scale_max - scale_min)/10)
            for i in range(scale_min, scale_max + 1, step):
                optionlist.append(f'{i}')
        ''' Значение параметров размера кисти '''
        variable = tk.StringVar(control_frame)
        variable.set(optionlist[0])
        ''' Задание параметров кисти '''
        brush_menu = tk.OptionMenu(control_frame, variable, *optionlist)
        ''' Отрисовка выпадающего меню '''
        def menu_callback(*data):
            data1 = variable.get()
            self.brush_size_scale.set(int(data1))
        ''' Функция настройки размера кисти'''
        variable.trace("w", menu_callback)
        ''' Отслеживания выбора элемента меню'''
        return brush_menu

    def pick_color(self, event):
        """ Функция получения цвета из пикселя """
        xy = [event.x, event.y]
        ''' Получение координат контрольного пикселя '''
        temp_color = self.image.getpixel(xy)
        ''' Получение цвета пикселя в формате RGB '''
        temp_color_rgb = "#{:02x}{:02x}{:02x}".format(temp_color[0], temp_color[1], temp_color[2])
        ''' Ппреобразование формата RGB в Hex '''
        self.pen_color = f'{temp_color_rgb}'
        ''' Присвоение значения цвета кисте'''
        self.is_rubber_on = False
        ''' Фиксация отключения ластика '''
        self.brush_color_lable_control(self.pen_color)
        ''' Изменение индикатора цвета кисти '''

    def window_size_choice(self):
        """ Функция для кнопки смены размера """
        width = tk.simpledialog.askinteger("Input", "Enter your age")
        ''' Запрос ввода длины '''
        height = tk.simpledialog.askinteger("Input", "Enter your age")
        ''' Запрос ввода ширины '''
        self.canvas.config(width=width, height=height)
        ''' Переконфигурация границы '''
        self.canvas.delete("all")
        ''' Очистка холста '''
        self.image.close()
        ''' Закрытие старого изображения '''
        self.image = Image.new("RGB", (width, height), "white")
        self.draw = ImageDraw.Draw(self.image)
        ''' Создание нового белого холста заданного размера'''

    def text_creator(self):
        """ Функция получения текста для ввода """
        if self.text_for_enter[3] == 'off':
            self.brush_type = 'text'
            self.text_for_enter[0] = tk.simpledialog.askstring("Input", "Введите текст")
            self.text_for_enter[3] = 'on'
            self.text_button.config(text='Исп. Карандаш')
            ''' Установка параметров для включенного ввода текста '''
        else:
            self.brush_type = 'brush'
            self.text_for_enter[3] = 'off'
            self.text_button.config(text='Ввести текст')
            ''' Установка параметров для выключенного ввода текста '''

    def choose_background(self):
        """ Функция перекраски фона """
        background_color = colorchooser.askcolor(color=self.pen_color)[1]
        ''' Выбор цвета фона из палитры '''
        self.canvas.config(background=background_color)
        ''' Замена цвета фона '''

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()