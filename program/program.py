from tkinter import Tk, Frame, Label, Button, BOTTOM
import sys
import time
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

    question = collections.namedtuple("question", ["nr", "question", "A", "B", "C", "D", "correctAnswer"])
    listOfQuestions = []
    for i in range(1, 11):
        listOfQuestions.append(question(i, data[i - 1][0], data[i - 1][1], data[i - 1][2], data[i - 1][3],
                                          data[i - 1][4], data[i - 1][5]))

    def begin(_event):
        buttonStart.pack_forget()
        line1.config(text="Good luck!")
        line2.pack_forget()
        line3.pack_forget()
        showQuestion(topFrame)

    def showQuestion(topFrame):
        global index, state
        view = Frame(topFrame, background='Blue')
        view.pack()
        askQuestion = Label(view, text=listOfQuestions[index].question)
        buttonA = Button(view, text=listOfQuestions[index].A)
        buttonB = Button(view, text=listOfQuestions[index].B)
        buttonC = Button(view, text=listOfQuestions[index].C)
        buttonD = Button(view, text=listOfQuestions[index].D)
        buttonNext = Button(view, text="Next", bg='Violet', fg='white')
        buttonScore = Button(view, text="Show score", bg='Violet', fg='white')
        askQuestion.pack()
        buttonA.pack()
        buttonB.pack()
        buttonC.pack()
        buttonD.pack()
        if state == State.lastQuestion or state == State.theEnd:
            buttonScore.pack()
        else:
            buttonNext.pack()
            state = State.unmarked
        buttonA.bind("<Button-1>", lambda e: check(e, "A", listOfQuestions[index].correctAnswer,
                                                   buttonA, buttonB, buttonC, buttonD))
        buttonB.bind("<Button-1>", lambda e: check(e, "B", listOfQuestions[index].correctAnswer,
                                                   buttonA, buttonB, buttonC, buttonD))
        buttonC.bind("<Button-1>", lambda e: check(e, "C", listOfQuestions[index].correctAnswer,
                                                   buttonA, buttonB, buttonC, buttonD))
        buttonD.bind("<Button-1>", lambda e: check(e, "D", listOfQuestions[index].correctAnswer,
                                                   buttonA, buttonB, buttonC, buttonD))
        buttonNext.bind("<Button-1>", lambda e: changeView(e, view, topFrame))
        buttonScore.bind("<Button-1>", showScore)
        return view

    def check(_event, choice, correctAnswer, buttonA, buttonB, buttonC, buttonD):
        global score, state
        if state == State.unmarked or state == State.lastQuestion:
            if state == State.lastQuestion:
                state = State.theEnd

            if choice == "A":
                buttonA.config(bg='DarkOrange')
                master.update()
            elif choice == "B":
                buttonB.config(bg='DarkOrange')
                master.update()
            elif choice == "C":
                buttonC.config(bg='DarkOrange')
                master.update()
            elif choice == "D":
                buttonD.config(bg='DarkOrange')
                master.update()
            else:
                assert False

            master.after(1000, lambda: helperToCheck(choice, correctAnswer, buttonA, buttonB,
                                                     buttonC, buttonD))

    def helperToCheck(choice, correctAnswer, buttonA, buttonB, buttonC, buttonD):
        global score, state
        if choice == correctAnswer:
            score += 1
            messagebox.showinfo(title="Info", message="Exactly!")
        else:
            messagebox.showinfo(title="Info", message="Wrong!")
            if choice == "A":
                buttonA.config(bg='Salmon')
            elif choice == "B":
                buttonB.config(bg='Salmon')
            elif choice == "C":
                buttonC.config(bg='Salmon')
            elif choice == "D":
                buttonD.config(bg='Salmon')
            else:
                assert False

        if correctAnswer == "A":
            buttonA.config(bg='SpringGreen')
        elif correctAnswer == "B":
            buttonB.config(bg='SpringGreen')
        elif correctAnswer == "C":
            buttonC.config(bg='SpringGreen')
        elif correctAnswer == "D":
            buttonD.config(bg='SpringGreen')
        else:
            assert False
        if state != State.lastQuestion and state != State.theEnd:
            state = State.marked

    def changeView(_event, view, topFrame):
            global index, state
            view.pack_forget()
            index += 1
            if index == 9:
                state = State.lastQuestion
            showQuestion(topFrame)

    def showScore(_event):
        messagebox.showinfo(title="Score", message="Your score: %d" % score)

    def end(_event):
        sys.exit()

    master = Tk()
    master.title("The Quiz about the world")
    master.geometry("700x600")
    master.configure(background='Blue')
    topFrame = Frame(master, background='Blue')
    bottomFrame = Frame(master, background='Blue')
    topFrame.pack()
    bottomFrame.pack(side=BOTTOM)

    line1 = Label(topFrame, text="Welcome to The Quiz about the world!", background='Blue', fg='white',
               justify='center')
    line2 = Label(topFrame, text="The quiz consists of 10 questions about geographical records.",
               background='Blue', fg='white', justify='center')
    line3 = Label(topFrame, text="It is only one correct answer to even question.", background='Blue',
               fg='white', justify='center')
    line1.pack()
    line2.pack()
    line3.pack()

    buttonStart = Button(master, text="Start quiz", bg='Violet', fg='white')
    buttonStart.bind("<Button-1>", begin)
    buttonStart.pack()
    buttonExit = Button(master, text="Exit", command=end, bg='Violet', fg='white')
    buttonExit.bind("<Button-1>", end)
    buttonExit.pack()

    master.mainloop()


if __name__ == "__main__":
    main()







