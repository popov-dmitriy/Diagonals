import tkinter as tk
from functools import partial
import random

background = 'seashell3'
letters = 'абвгдезиклмнопрстух'

with open("RUS.txt", "r") as file:  # считываем словарь русских слов
    rus_dict = file.readlines()
rus_dict = [line.rstrip() for line in rus_dict]


def create_field(n):
    fld_lst = []
    buttons = []
    for j in range(n):
        for i in range(n):
            element = tk.Text(root, width=2, height=1, font='Arial 16')
            element.bind('<KeyPress>', lambda event, fun=element: insert_symb(event, fun))  # удалять символы > 1
            fld_lst.append(element)
        button = tk.Button(root, text='подтвердить', width=10, height=1)  # , command=lambda: clicked_button(button))
        button.bind('<Button-1>', partial(clicked_button, buttons, button, n))  # у каждой кнопки unique name .!button_
        buttons.append(button)
    return fld_lst, buttons


def fill_field(field_list, button_list, n):
    shift = 0  # для сдвига полей друг от друга, чтобы между ними была 1 строка
    for i in range(3, n + 1):
        shift += i
    for j in range(n):
        for i in range(n):
            field_list[i * n + j].place(relx=i / 14, rely=(j + shift - 3) / 31)
            if i == j:
                field_list[i * n + j].insert(tk.INSERT, letter)
                field_list[i * n + j].configure(state=tk.DISABLED)
        button_list[j].place(relx=n / 13, rely=(j + shift - 3) / 31)


def clicked_button(general_pos, concrete_pos, n, event):
    what_field = buttons_list.index(general_pos)  # в каком по счёту поле кнопка нажата
    what_button = buttons_list[what_field].index(concrete_pos)  # какая конкретно кнопка

    word = ''
    for i in range(n):
        word += fields_list[what_field][what_button + i * n].get(1.0, tk.END)
        word = word.rstrip()  # удаляем \n после каждого символа

    if len(word) == n and word in rus_dict:
        accept_word(word, what_field, what_button, n)


def accept_word(word, what_field, what_button, n):
    buttons_list[what_field][what_button].destroy()
    for i in range(n):
        fields_list[what_field][what_button + i * n].destroy()

    shift = 0
    for i in range(3, n + 1):
        shift += i

    ans = ' '  # для красивого вывода найденных слов
    for i in range(len(word)):
        ans += word[i]
        ans += '   '

    lbl = tk.Label(root, text=ans, font='Arial 15', bg=background, fg='red')
    lbl.place(rely=(what_button + shift - 3) / 31)

    global counter
    counter += 1
    if counter == 25:
        win()


def win():
    new_wind = tk.Tk()
    root.destroy()
    new_wind.title('ПОБЕДА')
    new_wind["bg"] = 'RosyBrown'
    new_wind.geometry('400x400')
    x = (new_wind.winfo_screenwidth()) / 2 - 400 / 2  # чтобы окно было по центру экрана
    y = (new_wind.winfo_screenheight()) / 2 - 400 / 2
    new_wind.wm_geometry("+%d+%d" % (x, y))
    label = tk.Label(new_wind, text='Поздравляю\nс победой!!!', font='Arial 20', bg='RosyBrown', fg='firebrick')
    label.place(relx=0.3, rely=0.3)
    new_wind.mainloop()


def insert_symb(event, sym):
    if len(sym.get(1.0, tk.END)) > 1:
        sym.delete(1.0, tk.END)


root = tk.Tk()
root.title("Диагонали")
root["bg"] = background
width_rez = '400'
heigh_rez = '900'
root.geometry(width_rez + 'x' + heigh_rez)
root.resizable(width=False, height=False)
x = (root.winfo_screenwidth()) / 2 - int(width_rez) / 2  # чтобы окно было по центру экрана
y = (root.winfo_screenheight()) / 2 - int(heigh_rez) / 2
root.wm_geometry("+%d+%d" % (x, y))

counter = 0  # счетчик, по которому определится конец игры
letter = letters[random.randrange(len(letters))]
fields_list = []  # список списков полей 3х3 ... 7х7
buttons_list = []  # список кнопок 'подтвердить'
for num in range(3, 8):
    tmp_flds, tmp_bttns = create_field(num)
    fill_field(tmp_flds, tmp_bttns, num)
    fields_list.append(tmp_flds)
    buttons_list.append(tmp_bttns)

root.mainloop()
