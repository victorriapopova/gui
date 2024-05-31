import tkinter
import tkinter as tk
from tkinter import messagebox, simpledialog

from tkcalendar import Calendar, DateEntry


class AuthenticationSystem:
    def __init__(self):
        self.users = {"user1": "password1", "user2": "password2"}  # Такие базы данных пользователей

    def authenticate(self, username, password):
        if username in self.users and self.users[username] == password:
            return True
        else:
            return False

    def add_user(self, username, password):
        if username and password:  # Проверка на ввод данных
            self.users[username] = password
            messagebox.showinfo("Success", "User {} has been added successfully!".format(username))
        else:
            messagebox.showerror("Error", "Invalid input! Please enter username and password.")

    def reset_password(self):
        username = simpledialog.askstring("Reset Password", "Enter your username:")
        if username:
            if username in self.users:
                new_password = simpledialog.askstring("Reset Password", "Enter new password:")
                if new_password:
                    self.users[username] = new_password
                    messagebox.showinfo("Success", "Password for user {} has been reset successfully!".format(username))
            else:
                messagebox.showerror("Error", "User {} does not exist!".format(username))


def show_events_window(auth_system):
    root000 = tk.Tk()
    EventsGUI(root000, auth_system)
    root000.mainloop()


class LoginGUI:
    def __init__(self, master, auth_system1):
        self.master = master
        self.auth_system = auth_system1

        self.master.title("Login System")

        self.username_label = tk.Label(master, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        self.password_label = tk.Label(master, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(master, text="Login", command=self.login, bg="lightblue")
        self.login_button.pack(pady=5)

        self.register_button = tk.Button(master, text="Register", command=self.register, bg="lightgreen")
        self.register_button.pack(pady=5)

        self.reset_password_button = tk.Button(master, text="Reset Password", command=self.reset_password,
                                               bg="lightyellow")
        self.reset_password_button.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.auth_system.authenticate(username, password):
            self.master.destroy()
            show_events_window(self.auth_system)
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.auth_system.add_user(username, password)

    def reset_password(self):
        self.auth_system.reset_password()


def get_events_for_date(date, events):
    return events.get(date, "No events found for this date.")


def show_notifications():
    # если есть есть список новых уведомлений
    new_notifications = ["New event added!", "Reminder: Meeting tomorrow"]

    if new_notifications:
        # Создаем строку из списка уведомлений
        notification_text = "\n".join(new_notifications)
        # Отображаем окно с уведомлением
        tkinter.messagebox.showinfo("New Notifications", notification_text)
    else:
        # Если уведомлений нет
        tkinter.messagebox.showinfo("New Notifications", "No new notifications")


class EventsGUI:
    # noinspection PyTypeChecker
    def __init__(self, master, auth_system):
        self.master = master
        self.auth_system = auth_system
        self.events = {}

        self.master.title("Events")

        self.menu_bar = tk.Menu(master)
        master.config(menu=self.menu_bar)

        self.nav_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Navigation", menu=self.nav_menu)
        self.nav_menu.add_command(label="Today", command=self.goto_today)
        self.nav_menu.add_command(label="Next Day", command=self.goto_next_day)
        self.nav_menu.add_command(label="Previous Day", command=self.goto_previous_day)

        self.notif_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Notifications", menu=self.notif_menu)
        self.notif_menu.add_command(label="Show Notifications", command=show_notifications)

        self.event_listbox = tk.Listbox(master)
        self.event_listbox.pack(pady=10)

        self.add_event_button = tk.Button(master, text="Add Event", command=self.add_event, bg="lightblue")
        self.add_event_button.pack(pady=5)

        self.delete_event_button = tk.Button(master, text="Delete Event", command=self.delete_event, bg="light coral")
        self.delete_event_button.pack(pady=5)

        self.edit_event_button = tk.Button(master, text="Edit Event", command=self.edit_event, bg="lightgreen")
        self.edit_event_button.pack(pady=5)

        self.calendar = Calendar(master, selectmode='day', date_pattern='dd/MM/yyyy')
        self.calendar.pack(pady=10)

        self.calendar.bind("<<CalendarSelected>>", self.show_selected_date_events)

    def add_event(self):
        new_event_window = tk.Toplevel(self.master)
        new_event_window.title("Add Event")

        tk.Label(new_event_window, text="Event Name:").pack(pady=5)
        event_name_entry = tk.Entry(new_event_window)
        event_name_entry.pack(pady=5)

        tk.Label(new_event_window, text="Event Date:").pack(pady=5)
        event_date_entry = DateEntry(new_event_window, date_pattern='dd/MM/yyyy')
        event_date_entry.pack(pady=5)

        def on_submit():
            event_name = event_name_entry.get()
            event_date = event_date_entry.get()
            users = self.select_users(new_event_window)
            if event_name and event_date and users:
                event_details = f"{event_name} on {event_date} for {', '.join(users)}"
                self.event_listbox.insert(tk.END, event_details)
                self.events[event_date] = event_details
                self.calendar.calevent_create(event_date_entry.get_date(), event_name, 'event')
                new_event_window.destroy()
            else:
                messagebox.showerror("Error", "All fields are required!")

        tk.Button(new_event_window, text="Submit", command=on_submit, bg="lightblue").pack(pady=10)

    def delete_event(self):
        selected_index = self.event_listbox.curselection()
        if selected_index:
            self.event_listbox.delete(selected_index)

    def edit_event(self):
        selected_index = self.event_listbox.curselection()
        if selected_index:
            new_event_window = tk.Toplevel(self.master)
            new_event_window.title("Edit Event")

            tk.Label(new_event_window, text="Event Name:").pack(pady=5)
            event_name_entry = tk.Entry(new_event_window)
            event_name_entry.pack(pady=5)

            tk.Label(new_event_window, text="Event Date:").pack(pady=5)
            event_date_entry = DateEntry(new_event_window, date_pattern='dd/MM/yyyy')
            event_date_entry.pack(pady=5)

            def on_submit():
                new_event_name = event_name_entry.get()
                new_event_date = event_date_entry.get()
                users = self.select_users(new_event_window)
                if new_event_name and new_event_date and users:
                    event_details = f"{new_event_name} on {new_event_date} for {', '.join(users)}"
                    self.event_listbox.delete(selected_index)
                    self.event_listbox.insert(selected_index, event_details)
                    self.events[new_event_date] = event_details
                    self.calendar.calevent_create(event_date_entry.get_date(), new_event_name, 'event')
                    new_event_window.destroy()
                else:
                    messagebox.showerror("Error", "All fields are required!")

            tk.Button(new_event_window, text="Submit", command=on_submit, bg="lightblue").pack(pady=10)

    # noinspection PyArgumentList
    def show_selected_date_events(self):
        selected_date = self.calendar.get_date()
        #
        events = get_events_for_date()  # Предполагаю, что функция get_events_for_date() не требует аргументов
        messagebox.showinfo("Selected Date Events", f"Events for {selected_date}: \n {events}")

    # noinspection PyTypeChecker
    def select_users(self, parent):
        users = list(self.auth_system.users.keys())
        selected_users = []

        def on_select():
            for i in users_listbox.curselection():
                selected_users.append(users[i])
            users_selection_window.destroy()

        users_selection_window = tk.Toplevel(parent)
        users_selection_window.title("Select Users")

        search_label = tk.Label(users_selection_window, text="Search User:")
        search_label.pack(pady=5)
        search_entry = tk.Entry(users_selection_window)
        search_entry.pack(pady=5)

        def update_listbox():
            search_term = search_entry.get()
            users_listbox.delete(0, tk.END)
            for user_1 in users:
                if search_term.lower() in user_1.lower():
                    users_listbox.insert(tk.END, user_1)

        search_entry.bind("<KeyRelease>", update_listbox)

        users_listbox = tk.Listbox(users_selection_window, selectmode=tk.MULTIPLE)
        for user in users:
            users_listbox.insert(tk.END, user)
        users_listbox.pack(pady=5)

        tk.Button(users_selection_window, text="Select", command=on_select, bg="lightblue").pack(pady=10)

        users_selection_window.wait_window()

        return selected_users

    def goto_today(self):
        today = self.calendar.datetime.today()
        self.calendar.selection_set(today)

    def goto_next_day(self):
        selected_date = self.calendar.get_date()
        next_day = self.calendar.datetime.strptime(selected_date, '%d/%m/%Y') + self.calendar.timedelta(days=1)
        self.calendar.selection_set(next_day)

    def goto_previous_day(self):
        selected_date = self.calendar.get_date()
        previous_day = self.calendar.datetime.strptime(selected_date, '%d/%m/%Y') - self.calendar.timedelta(days=1)
        self.calendar.selection_set(previous_day)


if __name__ == "__main__":
    def show_login_screen():
        root = tk.Tk()
        auth_system = AuthenticationSystem()
        LoginGUI(root, auth_system)
        root.mainloop()


    show_login_screen()
