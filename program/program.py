from tkinter import Tk, Frame, Label, Button, BOTTOM, Canvas, PhotoImage, NW, mainloop
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

    question = collections.namedtuple("question", ["nr", "question", "A", "B", "C", "D", "correctAnswer",
                                                   "info"])

    listOfQuestions = []
    for i in range(1, 11):
        listOfQuestions.append(question(i, data[i - 1][0], data[i - 1][1], data[i - 1][2], data[i - 1][3],
                                          data[i - 1][4], data[i - 1][5], data[i-1][6]))

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
        empty11 = Label(view, text="", bg='Blue', fg='Blue')
        empty12 = Label(view, text="", bg='Blue', fg='Blue')
        empty13 = Label(view, text="", bg='Blue', fg='Blue')
        empty14 = Label(view, text="", bg='Blue', fg='Blue')
        empty15 = Label(view, text="", bg='Blue', fg='Blue')
        askQuestion = Label(view, text=listOfQuestions[index].question, bg='LightSteelBlue', font=('Arial', 15, 'bold'))
        buttonA = Button(view, text=listOfQuestions[index].A, bg='LightSkyBlue', font=('Arial', 15, 'bold'))
        buttonB = Button(view, text=listOfQuestions[index].B, bg='LightSkyBlue', font=('Arial', 15, 'bold'))
        buttonC = Button(view, text=listOfQuestions[index].C, bg='LightSkyBlue', font=('Arial', 15, 'bold'))
        buttonD = Button(view, text=listOfQuestions[index].D, bg='LightSkyBlue', font=('Arial', 15, 'bold'))
        buttonNext = Button(view, text="Next", bg='Violet', fg='white', font=('Arial', 15, 'bold'))
        buttonScore = Button(view, text="Show score", bg='Violet', fg='white', font=('Arial', 15, 'bold'))
        askQuestion.pack()
        empty11.pack()
        buttonA.pack()
        empty12.pack()
        buttonB.pack()
        empty13.pack()
        buttonC.pack()
        empty14.pack()
        buttonD.pack()
        empty15.pack()
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
        global score, state, index
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

        messagebox.showinfo(title="More information", message=listOfQuestions[index].info)

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
        messagebox.showinfo(title="Score", message="Your score: %d / 10\nThank You for asking the questions" % score)

    def end(_event):
        sys.exit()

    master = Tk()
    master.title("The Quiz about the world")
    master.geometry("800x700")
    master.configure(background='Blue')
    topFrame = Frame(master, background='Blue')
    bottomFrame = Frame(master, background='Blue')
    canvas = Canvas(bottomFrame, width=500, height=270)
    empty1 = Label(topFrame, text="", bg = 'Blue')
    empty2 = Label(topFrame, text="", bg='Blue')
    empty3 = Label(topFrame, text="", bg='Blue')
    empty4 = Label(bottomFrame, text="", bg='Blue', fg='Blue')
    empty5 = Label(bottomFrame, text="", bg='Blue', fg='Blue')
    line1 = Label(topFrame, text="Welcome to The Quiz about the world!", bg='Blue', fg='white',
                  justify='center', font=('Arial', 20, 'bold'))
    line2 = Label(topFrame, text="The quiz consists of 10 questions about geographical records.",
                  background='Blue', fg='white', justify='center', font=('Arial', 20, 'bold'))
    line3 = Label(topFrame, text="It is only one correct answer to even question.", background='Blue',
                  fg='white', justify='center', font=('Arial', 20, 'bold'))

    buttonStart = Button(topFrame, text="Start quiz", bg='Violet', fg='white', font=('Arial', 15, 'bold'))
    buttonStart.bind("<Button-1>", begin)
    buttonExit = Button(bottomFrame, text="Exit", command=end, bg='Violet', fg='white', font=('Arial', 15, 'bold'))
    buttonExit.bind("<Button-1>", end)

    topFrame.pack()
    bottomFrame.pack(side=BOTTOM)
    empty1.pack()
    empty2.pack()
    line1.pack()
    line2.pack()
    line3.pack()
    empty3.pack()
    buttonStart.pack()
    canvas.pack()
    photo = PhotoImage(file='0.gif')
    canvas.create_image(0, 0, image=photo, anchor=NW)
    empty4.pack()
    buttonExit.pack()
    empty5.pack()

    master.mainloop()


if __name__ == "__main__":
    main()







