
from pathlib import Path
import cv2
import threading
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import EstimateASL
from timeit import default_timer as timer


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def start_timer():
    global game_status
    while True:
        if game_status == True:
            start = timer()
            while len(letters2learn) > 0:
                canvas.itemconfigure(lblTimer, text = "Time Elapsed: "+(str(round(timer()-start, 2)))+"s",)
    

cap = cv2.VideoCapture(0)
def ASL_guess():
    global game_status
    cap = cv2.VideoCapture(0)
    while True:
        if game_status == True:
            while True:
                    success, image = cap.read()
                    #print(letters2learn)
                    
                    if len(letters2learn) == 0:
                        cv2.destroyAllWindows()
                        game_status = False
                        canvas.itemconfigure(lblPresentLetter, text = '')
                        canvas.itemconfigure(lblProgress, text = "Letters Learnt: 26/26",)
                        canvas.itemconfigure(lblInstructions, text = "Click 'Begin' to restart" )
                        break
                    try:
                        guess = EstimateASL.get_prediction(image)
                        cv2.putText(image,guess,(50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

                        if guess.lower() == letters2learn[0].lower():
                            letters2learn.pop(0)
                            canvas.itemconfigure(lblPresentLetter, text = letters2learn[0].upper())
                            canvas.itemconfigure(lblProgress, text = "Letters Learnt: "+ str(26-len(letters2learn)) +"/26",)
                        
                    except:
                        pass

                    cv2.imshow('Camera', image)
                    if cv2.waitKey(5) & 0xFF == 27: #press escape to break
                                break
            cv2.destroyAllWindows()

    #retVal.result = 0
    #while True:
    #    retVal.result += 1

#https://stackoverflow.com/a/53555027/13868464

guess_thread = threading.Thread(target = ASL_guess, name = 'ASL guesser')
timer_thread = threading.Thread(target = start_timer, name = 'Timer')

game_status = False

guess_thread.start()
timer_thread.start()

def Begin_Test():
    global letters2learn, ALPHABET, game_status
    ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    letters2learn = ALPHABET
    canvas.itemconfigure(lblPresentLetter, text = letters2learn[0].upper())
    canvas.itemconfigure(lblInstructions, text = "Create This Letter:" )
    game_status = True

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("836x517")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 517,
    width = 836,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    430.0,
    517.0,
    fill="#FBFBFB",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    635.0,
    443.0,
    image=image_image_1
)

canvas.create_text(
    43.0,
    30.0,
    anchor="nw",
    text="Learn American Sign Language",
    fill="#000000",
    font=("Microsoft YaHei Light", 24 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    636.0,
    195.0,
    image=image_image_2
)

lblProgress = canvas.create_text(
    555.0,
    413.0,
    anchor="nw",
    text="Letters Learnt: 0/26",
    fill="#000000",
    font=("Microsoft YaHei Light", 18 * -1)
)

lblTimer = canvas.create_text(
    555.0,
    444.0,
    anchor="nw",
    text="Time Elapsed: 0.00s",
    fill="#000000",
    font=("Microsoft YaHei Light", 18 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: Begin_Test(),
    relief="flat"
)
button_1.place(
    x=111.0,
    y=97.0,
    width=209.0,
    height=42.0
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    215.0,
    340.0,
    image=image_image_3
)

lblInstructions = canvas.create_text(
    140.0,
    237.0,
    anchor="nw",
    text="Click 'Begin' to start",
    fill="#000000",
    font=("Microsoft YaHei Light", 18 * -1)
)

lblPresentLetter = canvas.create_text(
    189.0,
    318.0,
    anchor="nw",
    text='',
    fill="#000000",
    font=("Microsoft YaHei Light", 96 * -1)
)
window.resizable(False, False)
window.mainloop()
