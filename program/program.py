from tkinter import Tk, Frame, Label, Button, BOTTOM
import sys
from time import sleep
import collections
from tkinter import messagebox
from enum import Enum

index = 0
score = 0


class State(Enum):
    unmarked = 0
    marked = 1
    lastQuestion = 2
    theEnd = 3


state = State.unmarked


def f(x):
    return x.split(";")


def main():

    with open('questions', "r") as i:
        data = [line.rstrip("\n") for line in i]

    data = list(map(f, data))

    question = collections.namedtuple("question", ["nr", "question", "A", "B", "C", "D", "correct_answer"])
    list_of_questions = []
    for i in range(1, 11):
        list_of_questions.append(question(i, data[i - 1][0], data[i - 1][1], data[i - 1][2], data[i - 1][3],
                                          data[i - 1][4], data[i - 1][5]))

    def begin(_event):
        b_start.pack_forget()
        l1.config(text="Good luck!")
        l2.pack_forget()
        l3.pack_forget()
        show_question(top_frame)

    def show_question(top_frame):
        global index, state
        view = Frame(top_frame, background='Blue')
        view.pack()
        l_question = Label(view, text=list_of_questions[index].question)
        b_A = Button(view, text=list_of_questions[index].A)
        b_B = Button(view, text=list_of_questions[index].B)
        b_C = Button(view, text=list_of_questions[index].C)
        b_D = Button(view, text=list_of_questions[index].D)
        b_next = Button(view, text="Next", bg='Violet', fg='white')
        b_score = Button(view, text="Show score", bg='Violet', fg='white')
        l_question.pack()
        b_A.pack()
        b_B.pack()
        b_C.pack()
        b_D.pack()
        if state == State.lastQuestion or state == State.theEnd:
            b_score.pack()
        else:
            b_next.pack()
            state = State.unmarked
        b_A.bind("<Button-1>", lambda e: check(e, "A", list_of_questions[index].correct_answer))
        b_B.bind("<Button-1>", lambda e: check(e, "B", list_of_questions[index].correct_answer))
        b_C.bind("<Button-1>", lambda e: check(e, "C", list_of_questions[index].correct_answer))
        b_D.bind("<Button-1>", lambda e: check(e, "D", list_of_questions[index].correct_answer))
        b_next.bind("<Button-1>", lambda e: change_view(e, view, top_frame))
        b_score.bind("<Button-1>", show_score)
        return view

    def check(_event, choice, correct_answer):
        global index, score, state
        if state == State.unmarked or state == State.lastQuestion:
            if state == State.lastQuestion:
                state = State.theEnd
            if choice == correct_answer:
                score += 1
                messagebox.showinfo(title="Info", message="Exactly!")
            else:
                messagebox.showinfo(title="Info", message="Wrong!")
            if state != State.lastQuestion and state != State.theEnd:
                state = State.marked

    def change_view(_event, view, top_frame):
            global index, state
            view.pack_forget()
            index += 1
            if index == 9:
                state = State.lastQuestion
            show_question(top_frame)

    def show_score(_event):
        messagebox.showinfo(title="Score", message="Your score: %d" % score)

    def end(_event):
        sys.exit()

    master = Tk()
    master.title("The Quiz about the world")
    master.geometry("700x600")
    master.configure(background='Blue')
    top_frame = Frame(master, background='Blue')
    bottom_frame = Frame(master, background='Blue')
    top_frame.pack()
    bottom_frame.pack(side=BOTTOM)

    l1 = Label(top_frame, text="Welcome to The Quiz about the world!", background='Blue', fg='white',
               justify='center')
    l2 = Label(top_frame, text="The quiz consists of 10 questions about geographical records.",
               background='Blue', fg='white', justify='center')
    l3 = Label(top_frame, text="It is only one correct answer to even question.", background='Blue',
               fg='white', justify='center')
    l1.pack()
    l2.pack()
    l3.pack()

    b_start = Button(master, text="Start quiz", bg='Violet', fg='white')
    b_start.bind("<Button-1>", begin)
    b_start.pack()
    b_exit = Button(master, text="Exit", command=end, bg='Violet', fg='white')
    b_exit.bind("<Button-1>", end)
    b_exit.pack()

    master.mainloop()


if __name__ == "__main__":
    main()







