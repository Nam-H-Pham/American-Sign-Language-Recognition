
from pathlib import Path
import cv2
import threading
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import EstimateASL
from timeit import default_timer as timer
import time

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def start_timer(): #Timer Thread
    global game_status, score
    print('>>>Timer thread loaded')
    while True:
        if game_status == True:
            start = timer()
            while len(letters2learn) > 0:
                score = timer()-start
                canvas.itemconfigure(lblTimer, text = "Time Elapsed: "+(str(round(score, 2)))+"s",)
                #time.sleep(0.05)

    

def ASL_guess(): #Camera Thread
    global game_status, score
    cap = cv2.VideoCapture(0)
    print('>>>Capture thread loaded')
    canvas.itemconfigure(lblInstructions, text = "Click 'Begin' to start" )
    messagebox.showinfo("Instructions",  "Place your camera in good lighting conditions. Try to ensure the image of your hand represents the images in the guide. Press begin to start.")
    button_1.place(x=111, y=97) 
    while True:
        if game_status == True:
            correct_confirmation = 0
            correct_confirmation_threshold = 3
            while True:
                    success, image = cap.read()
                    #print(letters2learn)
                    
                    if len(letters2learn) == 0:
                        cv2.destroyAllWindows()
                        game_status = False
                        canvas.itemconfigure(lblPresentLetter, text = '')
                        canvas.itemconfigure(lblProgress, text = "Letters Learnt: 26/26",)
                        canvas.itemconfigure(lblInstructions, text = "Click 'Begin' to restart" )
                        button_1.place(x=111, y=97) 

                        if HIGHSCORE == "Unavailable":
                            update_highscore()
                        elif score < int(HIGHSCORE):
                            update_highscore()
                        break
                    try:
                        guess = ""
                        guess, image = EstimateASL.get_prediction(image)

                        if guess.lower() == letters2learn[0].lower():
                            correct_confirmation += 1
                        if correct_confirmation >= correct_confirmation_threshold: #if number of frames with matching guesses matches a threshhold (fixes random validations and artifacts)
                            letters2learn.pop(0)
                            canvas.itemconfigure(lblPresentLetter, text = letters2learn[0].upper())
                            canvas.itemconfigure(lblProgress, text = "Letters Learnt: "+ str(26-len(letters2learn)) +"/26",)
                            correct_confirmation = 0        
                    except:
                        pass

                    #cv2.putText(image,"Confidence: "+str(correct_confirmation)+'/'+str(correct_confirmation_threshold),(50,60), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 255, 255), 1, cv2.LINE_AA) 
                    cv2.putText(image,"Confidence: "+str(int(correct_confirmation/correct_confirmation_threshold*100))+"%",(50,60), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 255, 255), 1, cv2.LINE_AA)       
                    
                    #cv2.putText(image,"Estimation: "+guess,(50,90), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 255, 255), 1, cv2.LINE_AA)
                   
                    cv2.imshow('Camera', image)
                    if cv2.waitKey(5) & 0xFF == 27: #press escape to break
                                break
            cv2.destroyAllWindows()

window = Tk()

window.geometry("836x517")
window.configure(bg = "#FFFFFF")
window.title('Learn the ASL Alphabet')

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
    
if True: #Handle window canvas
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
        outline="#fafafa")

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
        text="Loading Prerequisites...",
        fill="#000000",
        font=("Microsoft YaHei Light", 18 * -1)
    )

    lblHighscore = canvas.create_text(
        160.0,
        200.0,
        anchor="nw",
        text="Best Time:",
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

guess_thread = threading.Thread(target = ASL_guess, name = 'ASL guesser')
timer_thread = threading.Thread(target = start_timer, name = 'Timer')

game_status = False

with open('Highscore.txt') as f:
    try:
        HIGHSCORE = f.readlines()[0]
    except:
        HIGHSCORE = "Unavailable"
canvas.itemconfigure(lblHighscore, text = "Best Time: "+str(HIGHSCORE)+"s",)
    
def update_highscore():
    global HIGHSCORE, score
    with open('Highscore.txt', 'w') as f:
        f.write(str(int(score)))
    with open('Highscore.txt') as f:
        HIGHSCORE = f.readlines()[0]
    canvas.itemconfigure(lblHighscore, text = "Best Time: "+str(HIGHSCORE)+"s",)

guess_thread.start()
timer_thread.start()

button_1.place(x=-500, y=-500) 
def Begin_Test():
    global letters2learn, ALPHABET, game_status, button_1
    ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    letters2learn = ALPHABET
    canvas.itemconfigure(lblPresentLetter, text = letters2learn[0].upper())
    canvas.itemconfigure(lblInstructions, text = "Create This Letter:" )
    canvas.itemconfigure(lblProgress, text = "Letters Learnt: 0/26",)
    game_status = True
    button_1.place(x=-500, y=-500) 


window.resizable(False, False)
window.mainloop()
