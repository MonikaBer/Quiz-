from tkinter import Tk, Frame, Label, Button, messagebox, Canvas, PhotoImage, mainloop, NW, BOTTOM
from enum import Enum
import collections
import time
import sys

index = 0
score = 0


class State(Enum):
    unmarked = 0
    marked = 1
    last_question = 2
    the_end = 3


state = State.unmarked


def f(x):
    return x.split(";")


def main():

    with open("questions", "r") as i:
        data = [line.rstrip("\n") for line in i]

    data = list(map(f, data))

    question = collections.namedtuple("question", ["nr", "ask", "A", "B", "C", "D", "correct_answer",
                                                   "info"])

    list_of_questions = []
    for i in range(1, 11):
        list_of_questions.append(question(i, data[i-1][0], data[i-1][1], data[i-1][2], data[i-1][3],
                                        data[i-1][4], data[i-1][5], data[i-1][6]))

    def begin(_event):
        line1.config(text="Good luck!")
        line2.pack_forget()
        line3.pack_forget()
        button_start.pack_forget()
        show_question(top_frame)

    def show_question(top_frame):
        global state
        view = Frame(top_frame, bg="Blue")
        view.pack()
        empty11 = Label(view, text="", bg="Blue")
        empty12 = Label(view, text="", bg="Blue")
        empty13 = Label(view, text="", bg="Blue")
        empty14 = Label(view, text="", bg="Blue")
        empty15 = Label(view, text="", bg="Blue")
        ask_question = Label(view, text=list_of_questions[index].ask, bg="LightSteelBlue",
                             font=("Arial", 20, "bold"))
        button_a = Button(view, text=list_of_questions[index].A, bg="LightSkyBlue", font=("Arial", 15, "bold"))
        button_b = Button(view, text=list_of_questions[index].B, bg="LightSkyBlue", font=("Arial", 15, "bold"))
        button_c = Button(view, text=list_of_questions[index].C, bg="LightSkyBlue", font=("Arial", 15, "bold"))
        button_d = Button(view, text=list_of_questions[index].D, bg="LightSkyBlue", font=("Arial", 15, "bold"))
        button_next = Button(view, text="Next", bg="Violet", fg="white", font=("Arial", 20, "bold"))
        button_score = Button(view, text="Show score", bg="Violet", fg="white", font=("Arial", 20, "bold"))
        ask_question.pack()
        empty11.pack()
        button_a.pack()
        empty12.pack()
        button_b.pack()
        empty13.pack()
        button_c.pack()
        empty14.pack()
        button_d.pack()
        empty15.pack()
        if state == State.last_question or state == State.the_end:
            button_score.bind("<Button-1>", show_score)
            button_score.pack()
        else:
            button_next.bind("<Button-1>", lambda e: change_view(e, view, top_frame))
            button_next.pack()
            state = State.unmarked
        button_a.bind("<Button-1>", lambda e: check(e, "A", list_of_questions[index].correct_answer,
                                                    button_a, button_b, button_c, button_d))
        button_b.bind("<Button-1>", lambda e: check(e, "B", list_of_questions[index].correct_answer,
                                                    button_a, button_b, button_c, button_d))
        button_c.bind("<Button-1>", lambda e: check(e, "C", list_of_questions[index].correct_answer,
                                                    button_a, button_b, button_c, button_d))
        button_d.bind("<Button-1>", lambda e: check(e, "D", list_of_questions[index].correct_answer,
                                                    button_a, button_b, button_c, button_d))

        return view

    def check(_event, choice, correct_answer, button_a, button_b, button_c, button_d):
        global state
        if state == State.unmarked or state == State.last_question:
            if state == State.last_question:
                state = State.the_end

            if choice == "A":
                button_a.config(bg="DarkOrange")
                master.update()
            elif choice == "B":
                button_b.config(bg="DarkOrange")
                master.update()
            elif choice == "C":
                button_c.config(bg="DarkOrange")
                master.update()
            elif choice == "D":
                button_d.config(bg="DarkOrange")
                master.update()
            else:
                assert False

            master.update()
            master.update()
            master.update()
            master.after(2000, lambda: helper_to_check(choice, correct_answer, button_a, button_b,
                                                       button_c, button_d))

    def helper_to_check(choice, correct_answer, button_a, button_b, button_c, button_d):
        global state, score
        if choice == correct_answer:
            score += 1
            messagebox.showinfo(title="Info", message="Exactly!")
        else:
            messagebox.showinfo(title="Info", message="Wrong!")
            if choice == "A":
                button_a.config(bg="Salmon")
            elif choice == "B":
                button_b.config(bg="Salmon")
            elif choice == "C":
                button_c.config(bg="Salmon")
            elif choice == "D":
                button_d.config(bg="Salmon")
            else:
                assert False

        if correct_answer == "A":
            button_a.config(bg="SpringGreen")
        elif correct_answer == "B":
            button_b.config(bg="SpringGreen")
        elif correct_answer == "C":
            button_c.config(bg="SpringGreen")
        elif correct_answer == "D":
            button_d.config(bg="SpringGreen")
        else:
            assert False

        messagebox.showinfo(title="More information", message=list_of_questions[index].info)

        if state != State.last_question and state != State.the_end:
            state = State.marked

    def change_view(_event, view, top_frame):
            global index, state
            view.pack_forget()
            index += 1
            if index == 9:
                state = State.last_question
            show_question(top_frame)

    def show_score(_event):
        messagebox.showinfo(title="Score", message="Your score: %d / 10\nThank You for asking the questions"
                                                   % score)

    def end(_event):
        sys.exit()

    master = Tk()
    master.title("The Quiz about the world")
    master.geometry("800x730")
    master.configure(bg="Blue")
    top_frame = Frame(master, bg="Blue")
    bottom_frame = Frame(master, bg="Blue")
    canvas = Canvas(bottom_frame, width=500, height=270, bg="Blue")
    empty1 = Label(top_frame, text="", bg="Blue")
    empty2 = Label(top_frame, text="", bg="Blue")
    empty3 = Label(top_frame, text="", bg="Blue")
    empty4 = Label(bottom_frame, text="", bg="Blue")
    empty5 = Label(bottom_frame, text="", bg="Blue")
    empty6 = Label(bottom_frame, text="", bg="Blue")
    empty7 = Label(bottom_frame, text="", bg="Blue")
    line1 = Label(top_frame, text="Welcome to The Quiz about the world!", bg="Blue", fg="white",
                  justify="center", font=("Arial", 25, "bold"))
    line2 = Label(top_frame, text="The quiz consists of 10 questions about geographical records.",
                  bg="Blue", fg="white", justify="center", font=("Arial", 25, "bold"))
    line3 = Label(top_frame, text="It is only one correct answer to even question.", bg="Blue",
                  fg="white", justify="center", font=("Arial", 25, "bold"))

    button_start = Button(top_frame, text="Start quiz", bg="Violet", fg="white", font=("Arial", 20, "bold"))
    button_start.bind("<Button-1>", begin)
    button_exit = Button(bottom_frame, text="Exit", bg="Violet", fg="white", font=("Arial", 20, "bold"))
    button_exit.bind("<Button-1>", end)

    top_frame.pack()
    bottom_frame.pack(side=BOTTOM)
    empty1.pack()
    empty2.pack()
    line1.pack()
    line2.pack()
    line3.pack()
    empty3.pack()
    button_start.pack()
    empty4.pack()
    canvas.pack()
    photo = PhotoImage(file="mountains.gif")
    canvas.create_image(0, 0, image=photo, anchor=NW)
    empty5.pack()
    button_exit.pack()
    empty6.pack()
    empty7.pack()

    master.mainloop()


if __name__ == "__main__":
    main()