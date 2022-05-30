import random
import json
import pyperclip
from tkinter import *
from tkinter import messagebox

FONT = ('Calibri', 10)
USER_DATA_JSON = r'C:\Users\montv\python_work\100_days_of_code\day_30\my_pass\user_data.json'

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_random_password():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    random_letters = [random.choice(LETTERS) for _ in range(nr_letters)]
    random_symbols = [random.choice(SYMBOLS) for _ in range(nr_symbols)]
    random_numbers = [random.choice(NUMBERS) for _ in range(nr_numbers)]

    random_samples = random_letters + random_symbols + random_numbers
    random.shuffle(random_samples)
    random_password = ''.join(random_samples)

    pyperclip.copy(random_password)

    return random_password


def find_password():
    website = entry_website.get()

    try:
        with open(USER_DATA_JSON, 'r') as f:
            data = json.load(f)

    except FileNotFoundError:
        messagebox.showerror(title="File Not Found",
                             message="No data file found. Create new login before searching.")

    else:
        if website in data.keys():
            messagebox.showinfo(title='Login Information',
                                message=f'Website: {website}\nPassword: {data[website]["password"]}')
        else:
            messagebox.showinfo(title="Login Information",
                                message=f"Website named '{website}' not found in user data file.")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def close_window(event=None):
    window.destroy()


def save_data(event=None):
    """Writes user data to a file, then clears the input fields."""
    fields = [entry_website.get(), entry_username.get(), entry_password.get()]

    new_data = {
        fields[0]: {
            'email': fields[1],
            'password': fields[2],

        }
    }

    if fields[0] and fields[1] and fields[2]:
        confirm_msg = f"You entered\n\nWebsite: {entry_website.get()}\nUsername: {entry_username.get()}\nPassword: " \
                      f"{entry_password.get()}\n\nIs this correct?"

        confirm_entries = messagebox.askokcancel(title="Confirm Password", message=confirm_msg)

        if confirm_entries:
            try:
                with open(USER_DATA_JSON, 'r') as f:
                    data = json.load(f)

            except FileNotFoundError:
                with open(USER_DATA_JSON, 'w') as f:
                    json.dump(new_data, f, indent=4)

            else:
                data.update(new_data)
                with open(USER_DATA_JSON, 'w') as f:
                    json.dump(data, f, indent=4)

            finally:
                entry_password.delete(0, END)
                entry_website.delete(0, END)
                entry_website.focus_set()

    else:
        messagebox.showerror(title="Missing Entry(s)", message="Please complete all fields.")


def show_random_password():
    entry_password.delete(0, END)
    entry_password.insert(index=0, string=f'{generate_random_password()}')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("MyPass//Password Manager")
window.minsize(height=350, width=450)
window.maxsize(height=600, width=450)
window.config(padx=10, pady=50, bg='white')

window.bind(sequence='<Return>', func=save_data)
window.bind(sequence='<Escape>', func=close_window)

logo_filepath = r'C:\Users\montv\python_work\100_days_of_code\day_30\my_pass\logo.png'
logo_img = PhotoImage(file=logo_filepath)

canvas = Canvas(width=200, height=200, bg='white', highlightthickness=0)
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
label_website = Label(pady=5)
label_website.config(text='                Website: ', font=FONT, bg='white')
label_website.grid(row=1, column=0)

label_username = Label(pady=5)
label_username.config(text='Email/Username: ', font=FONT, bg='white')
label_username.grid(row=2, column=0)

label_password = Label(pady=5)
label_password.config(text='             Password: ', font=FONT, bg='white')
label_password.grid(row=3, column=0)

# Entries
entry_website = Entry()
entry_website.focus_set()
entry_website.config(width=35, relief='ridge', borderwidth=2)
entry_website.grid(row=1, column=1)

entry_username = Entry()
entry_username.config(width=50, relief='ridge', borderwidth=2)
entry_username.insert(index=END, string='ksmontville@gmail.com')
entry_username.grid(row=2, column=1, columnspan=2)

entry_password = Entry()
entry_password.config(width=35, relief='ridge', borderwidth=2)
entry_password.grid(row=3, column=1)

# Buttons
button_password = Button(width=11)
button_password.config(command=show_random_password, text='Randomize', font=FONT, relief='ridge', bg='IndianRed',
                       borderwidth=0)
button_password.grid(row=3, column=2)

button_search = Button(width=11)
button_search.config(command=find_password, text='Search', font=FONT, relief='ridge', bg='IndianRed', borderwidth=0)
button_search.grid(row=1, column=2)

button_add = Button()
button_add.config(command=save_data, width=42, text='Add', font=FONT, relief='ridge', bg='IndianRed', borderwidth=0)
button_add.grid(row=4, column=1, columnspan=2)

window.mainloop()
