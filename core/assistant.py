import customtkinter as Ctk
from PIL import Image, ImageTk
import time
import random
from queue import Queue
import speech_recognition as sr
import threading
from voice import speaker, set_volume, set_subtitles
from driver import assistant, act, fast_act, auto_role, perform_simulated_keypress, write_action
from window_focus import activate_windowt_title

# Initialize the speech recognition and text to speech engines
assistant_voice_recognition_enabled = True  # Disable if you don't want to use voice recognition
assistant_name_handle = "Ok Computer"  # Change this to your preferred name, will be used for voice activation.
assistant_anim_enabled = True
assistant_voice_enabled = True
set_volume(0.25)
assistant_subtitles_enabled = True
recognizer = sr.Recognizer()
message_queue = Queue()
Ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
Ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green


def listen_to_speech():
    # Function to listen for speech and add the recognized text to the message queue
    with sr.Microphone() as source:
        try:
            print("Assistant Listening...")
            audio = recognizer.listen(source, timeout=5)  # Listen for 5 seconds
            message = recognizer.recognize_google(audio)
            print("You said:", message)
            message_queue.put(message)
            return message
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        except sr.WaitTimeoutError:
            print("Listening timed out.")
        finally:
            # Schedule the function to be called again
            # root.after(1000, listen_to_speech) # This if you want to try it indefinitely.
            print("Google Speech Recognition could not understand audio")
            pass


def process_queue():
    # Function to check the message queue and show messages as bubbles
    try:
        while not message_queue.empty():
            message = message_queue.get_nowait()
            if message:
                show_message(None, message)  # Pass None for event
                speaker(message)
    finally:
        # Schedule the function to be called again
        root.after(100, process_queue)
        pass


def on_drag(event):
    # Function to move the window on drag
    global is_dragging, position_right, position_bottom, drag_time
    drag_time = time.time()
    is_dragging = True
    x = root.winfo_pointerx() - offset_x
    y = root.winfo_pointery() - offset_y
    root.geometry(f'+{x}+{y}')
    label.configure(image=assistant_dragging_photo)


def end_drag(event):
    global is_dragging, position_right, position_bottom, drag_time, click_time
    if not click_time:
        return
    dragged_message = "Whats the action?" if time.time() - click_time < 0.15 else "You dragged me!"
    # If the duration of the drag is less than the threshold for a click
    if time.time() - drag_time < 0.15:
        is_dragging = False
        position_right = root.winfo_x()
        position_bottom = root.winfo_y()
        label.configure(image=assistant_photo)
        animate_move()
        show_message(event, dragged_message)
        speaker(dragged_message)
    else:
        label.configure(image=assistant_photo)
        animate_move()  # Resume the movement animation
        show_message(event, dragged_message)
        speaker(dragged_message)
        create_input_bubble(action=True)
    print(f"Clicked on the assistant: {dragged_message}")


def create_input_bubble(action=False):
    # Get dimensions for proper placement
    bubble_width = 450  # Set a fixed width for the bubble
    bubble_height = 28  # A reasonable height to fit the text entry
    # Calculate the bubble position to the left of the assistant
    bubble_x = root.winfo_x() - bubble_width + 40  # Adjust the X position as needed
    bubble_y = root.winfo_y() + (assistant_photo_height // 2) - (bubble_height // 2) + 40
    # Create bubble as a top-level window
    bubble = Ctk.CTkToplevel(root)
    bubble.attributes('-alpha', 0.85)
    bubble.bind("<Escape>", lambda e: bubble.destroy())
    bubble.bind("<FocusOut>", lambda e: bubble.destroy())
    bubble.overrideredirect(True)
    bubble.attributes('-topmost', True)
    bubble.geometry(f'{bubble_width}x{bubble_height}+{bubble_x}+{bubble_y}')
    # Create the entry widget
    entry = Ctk.CTkEntry(bubble, corner_radius=6, placeholder_text_color="#0b2d39",
                         fg_color="#e1f2f1", text_color="#040f13",
                         placeholder_text="Type here the action to perform...", width=450,
                         border_width=1, border_color="darkgray")
    entry.bind("<Escape>", lambda e: bubble.destroy())
    entry.pack(padx=0, pady=0)
    # Force focus on the entry and bubble
    try:
        bubble.after(10, lambda: [bubble.focus_force(), entry.focus_force()])
    except Ctk.ctk_tk.TclError:
        # Ignore the error, as the window or widget is no longer valid
        pass
    # Bind Return and Escape keys to process input or destroy bubble
    entry.bind("<Return>", lambda e: process_input_and_close(bubble, entry, action))
    # Bind mouse click to focus back on entry
    bubble.bind("<Button-1>", lambda e: entry.focus_force())
    # Make sure bubble is focused as well when clicking on it
    bubble.bind("<FocusIn>", lambda e: entry.focus_force())
    return bubble  # Returning bubble reference in case it needs to be accessed

def process_input_and_close(bubble, entry, action=False):
    user_input = entry.get()
    print(f"Processing input: {user_input}")
    if user_input.strip():
        bubble.destroy()
        # Use the user input as needed: display, speech, or further processing.
        show_message(None, user_input)
        # speaker(user_input.strip())
        if action:
            print("Performing action: ", user_input)
            fast_act(single_step=user_input.strip())
        else:
            print(f"Running assistant... Generating test case: {user_input.strip()}")
            speaker(f"Running assistant... Generating test case: {user_input.strip()}")
            # assistant(assistant_goal=user_input.strip(), called_from="assistant")
            assistant_thread = threading.Thread(target=run_assistant, args=(user_input.strip(),))
            assistant_thread.start()
            # assistant(user_input.strip())
        # auto_prompt(user_input.strip())
    bubble.destroy()  # Ensure the bubble is destroyed after submission

def listen_and_respond():
    action = listen_to_speech()
    if action:  # Check if action is not None or empty string
        show_message(None, action)
        # Execute the assistant function in a separate thread
        # assistant_thread = threading.Thread(target=run_assistant, args=(action,))
        # assistant_thread.start()


def run_assistant(action):
    print("Running assistant...")
    assistant(assistant_goal=action, called_from="assistant")


def start_drag(event):
    # Record the starting point for dragging
    global offset_x, offset_y, click_time
    offset_x = event.x
    offset_y = event.y
    click_time = time.time()


def show_message(event=None, message="Hello! How can I help you?"):
    # Function to show a pop-up message bubble
    message_window = Ctk.CTkToplevel(root)  # Create a new window
    message_window.overrideredirect(True)  # Remove the window border
    message_window.attributes('-topmost', True)  # Keep the window on top
    # Get dimensions for the message window
    # temp_label = Ctk.CTkLabel(message_window, text=message)
    # temp_label.pack()
    message_window.update_idletasks()  # Update the layout to get size
    message_width = message_window.winfo_width()
    message_height = message_window.winfo_height()
    # temp_label.destroy()
    if event:
        pos_x = event.x_root + 20
        pos_y = event.y_root - message_height // 2
    else:
        # Calculate position based on assistant current position
        pos_x = root.winfo_x() + label.winfo_width() + 10
        pos_y = root.winfo_y() + label.winfo_height() // 2 - message_height // 2
    # Adjust position if the message window goes offscreen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    if pos_x + message_width > screen_width:
        pos_x = screen_width - message_width
    if pos_y + message_height > screen_height:
        pos_y = screen_height - message_height
    if pos_y < 0:
        pos_y = 0
    # Set the geometry and display the message
    message_window.geometry(f'+{pos_x}+{pos_y}')
    message_label = Ctk.CTkLabel(message_window, text=message)
    message_label.configure(corner_radius=6, fg_color="#e1f2f1", text_color="black", bg_color="gray")
    message_label.pack(padx=0, pady=0)
    # Close the message bubble after 3 seconds
    message_window.after(3000, message_window.destroy)

def create_context_menu(event_x_root, event_y_root):
    global context_menu_ref, assistant_voice_enabled, assistant_anim_enabled, assistant_subtitles_enabled, assistant_voice_recognition_enabled  # Use the global references

    # Create a custom context menu using Ctk widgets
    context_menu = Ctk.CTkToplevel(root)
    context_menu.overrideredirect(True)
    context_menu.attributes('-topmost', True)
    context_menu.attributes('-alpha', 0.95)  # Set transparency (0.0 to 1.0)
    # Set the theme to light
    # Change buttons color
    # Ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
    # context_menu visual options
    context_menu.configure(borderless=True, border_color="black")
    context_menu.bind("<Escape>", lambda e: context_menu.destroy())
    context_menu.bind("<FocusOut>", lambda e: context_menu.destroy())
    # Frame to hold menu items
    menu_frame = Ctk.CTkFrame(context_menu)
    menu_frame.pack()
    # Wrapper function to execute command and close the menu
    def menu_command(command):
        if callable(command):
            print(f"Executing command: {command}")
            command()  # Execute command if it's callable
        else:
            print(f"Command '{command}' not implemented yet")
        context_menu.destroy()  # Destroy the menu after executing the command

    # Buttons with commands
    Ctk.CTkButton(menu_frame, text="Call assistant", command=lambda: menu_command(generate_assistant_test_case(False))).pack(fill="x")
    Ctk.CTkButton(menu_frame, text="Fast action", command=lambda: menu_command(generate_assistant_test_case(True))).pack(fill="x")
    Ctk.CTkButton(menu_frame, text="Content analysis", command=lambda: menu_command(dummy_command)).pack(fill="x")

    # Add separator or space between groups of options (This is an improvisation since Ctk doesn't have a separator widget)
    Ctk.CTkLabel(menu_frame, text="", height=3).pack(fill="x")

    # Toggle buttons for voice, animation, and subtitles with the current status check
    volume_option = "Enable assistant voice" if not assistant_voice_enabled else "Disable assistant voice"
    anim_option = "Enable animations" if not assistant_anim_enabled else "Disable animations"
    subs_option = "Enable subtitles" if not assistant_subtitles_enabled else "Disable subtitles"
    voice_option = "Enable voice recognition" if not assistant_voice_recognition_enabled else "Disable voice recognition"
    # Add the buttons to the menu frame
    Ctk.CTkButton(menu_frame, text=volume_option, command=lambda: menu_command(toggle_volume)).pack(fill="x")
    Ctk.CTkButton(menu_frame, text=anim_option, command=lambda: menu_command(toggle_animations)).pack(fill="x")
    Ctk.CTkButton(menu_frame, text=subs_option, command=lambda: menu_command(toggle_subtitles)).pack(fill="x")
    Ctk.CTkButton(menu_frame, text=voice_option, command=lambda: menu_command(toggle_voice_recognition)).pack(fill="x")
    # Add separator or space between groups of options (This is an improvisation since Ctk doesn't have a separator widget)
    Ctk.CTkLabel(menu_frame, text="", height=3).pack(fill="x")
    # Extra options
    Ctk.CTkButton(menu_frame, text="Minimize", command=lambda: menu_command(minimize_assistant)).pack(fill="x")
    Ctk.CTkButton(menu_frame, text="Hide", command=lambda: menu_command(root.withdraw)).pack(fill="x")
    Ctk.CTkButton(menu_frame, text="Reset", command=lambda: menu_command(restart_assistant)).pack(fill="x")
    Ctk.CTkButton(menu_frame, text="Stop", command=lambda: menu_command(stop_assistant)).pack(fill="x")
    Ctk.CTkLabel(menu_frame, text="", height=3).pack(fill="x")
    Ctk.CTkButton(menu_frame, text="Back...", command=lambda: menu_command(root.deiconify)).pack(fill="x")

    # Update the layout to calculate the width and height
    context_menu.update_idletasks()
    menu_width = menu_frame.winfo_reqwidth()
    menu_height = menu_frame.winfo_reqheight()

    # Position the menu at the cursor position
    # If the menu goes off the screen to the right, move it left; same for bottom
    if event_x_root + menu_width > root.winfo_screenwidth():
        event_x_root = root.winfo_screenwidth() - menu_width - 93
    if event_y_root + menu_height > root.winfo_screenheight():
        event_y_root = root.winfo_screenheight() - menu_height - 100

    context_menu.geometry(f"{menu_width}x{menu_height}+{event_x_root}+{event_y_root}")
    context_menu.focus_force()  # Force focus on the menu
    context_menu_ref = context_menu  # Store the reference to the menu in a global variable
    return context_menu_ref

def minimize_assistant():
    root.withdraw()
    root.overrideredirect(False)
    root.iconify()
    # root.overrideredirect(True)


def show_config(event):
    # Function to display the settings menu using a custom context menu
    create_context_menu(event.x_root, event.y_root)

# Just for example purpose, you will replace this with actual commands
def dummy_command():
    speaker("Dummy item clicked")
    print("Dummy item clicked")

def generate_assistant_test_case(fast_act=False):
    # Function to perform a fast action
    if fast_act:
        speaker("What's the fast action step?")
        print("What's the fast action step?")
        create_input_bubble(fast_act)
    else:
        speaker("What's the test-case to generate?")
        print("What's the test-case to generate?")
        create_input_bubble(fast_act)

def toggle_voice_recognition():
    global assistant_voice_recognition_enabled
    assistant_voice_recognition_enabled = not assistant_voice_recognition_enabled
    if assistant_voice_recognition_enabled:
        show_message(None, "Voice recognition enabled")
        speaker("Voice recognition enabled")
    else:
        show_message(None, "Voice recognition disabled")
        speaker("Voice recognition disabled")


def toggle_animations():
    global assistant_anim_enabled
    assistant_anim_enabled = not assistant_anim_enabled
    if assistant_anim_enabled:
        animate_blink()  # Restart blinking animation
        animate_move()   # Restart moving animation
        show_message(None, "Animations enabled")
    else:
        show_message(None, "Animations disabled")


def toggle_subtitles():
    global assistant_subtitles_enabled
    assistant_subtitles_enabled = not assistant_subtitles_enabled
    if assistant_subtitles_enabled:
        show_message(None, "Subtitles enabled")
        set_subtitles(True)
    else:
        set_subtitles(False)
        show_message(None, "Subtitles disabled")


def toggle_volume():
    global assistant_voice_enabled
    assistant_voice_enabled = not assistant_voice_enabled
    if assistant_voice_enabled:
        show_message(None, "Assistant voice enabled")
        set_volume(0.25)
        speaker("Voice enabled")
    else:
        show_message(None, "Assistant voice disabled")
        set_volume(0)


def stop_assistant():
    root.destroy()
    pass


def restart_assistant():
    root.destroy()
    create_app()
    pass


def calculate_duration_of_speech(text, lang='en', wpm=150):
    # Estimate the duration the subtitles should be displayed based on words per minute (WPM)
    duration_in_seconds = (len(text.split()) / wpm) * 60
    return int(duration_in_seconds * 1000)  # Convert to milliseconds for tkinter's after method


def animate_blink():
    # Function for blinking animation
    label.configure(image=assistant_blink_photo)
    root.after(150, lambda: label.configure(image=assistant_photo))
    next_blink = random.randint(500, 10000) if assistant_anim_enabled else 10000
    root.after(next_blink, animate_blink)


def animate_move(step=0, direction=1, amplitude=3, start_time=1):
    global position_bottom, is_dragging
    max_steps = 15
    if start_time is None:
        start_time = time.time()
    if assistant_anim_enabled and not is_dragging:
        new_position = position_bottom + amplitude * direction * (1 - abs(step / max_steps * 2 - 1))
        root.geometry(f'+{position_right}+{int(new_position)}')
        next_step = step + 1
        if next_step > max_steps:
            current_time = time.time()
            next_step = 0
            movement_duration = current_time - start_time
            if 1 <= movement_duration <= 2:
                direction = -direction
                start_time = current_time
            amplitude = random.randint(0, 3)
        random_delay = random.randint(30, 200)
        root.after(random_delay, lambda: animate_move(next_step, direction, amplitude, start_time))


def listen_thread():
    global assistant_voice_recognition_enabled
    print("Assistant listening thread started...")
    while True:
        if not assistant_voice_recognition_enabled:
            # If voice recognition got disabled, wait for a bit before checking again ToDo: Maybe use a condition variable instead, but im planning on performing other actions here. Like a low power mode or something like that works for now
            time.sleep(1)
            # print("Voice recognition disabled, waiting...")
            continue

        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=1.5)
                if assistant_voice_recognition_enabled:
                    message = recognizer.recognize_google(audio)
                    message_low = message.lower()
                    # Speaking the message
                    message_queue.put(message)
                    # Only process the audio if voice recognition is enabled
                    if "okay computer" in message_low[0:13] or assistant_name_handle.lower() in message_low[0:11]:
                        message_queue.put("Assistant here! How can I help you?")
                        ok_computer = listen_to_speech()
                        if ok_computer:
                            show_message(None, ok_computer)
                            assistant(ok_computer)
                    elif "open" in message_low[0:4]:
                        if len(message) < 18:
                            print("Opening the program: ", message)
                            activate_windowt_title(message.strip("open "))
                        else:
                            assistant(message)
                    elif "stop" in message_low:
                        print("Stopping...")
                        stop_assistant()
                    elif "double click" in message_low[0:12]:
                        print("Double clicking on:", message)
                        fast_act(single_step=message.strip("double "), double_click=True)
                    # Or if message starts with the first word click and
                    elif "click on" in message_low[0:8] or "click the" in message_low[0:9] or "click" in message_low[0:5]:
                        print("Clicking on:", message)
                        fast_act(single_step=message)
                    elif "press" in message_low[0:5]:
                        print("press: ", message)
                        perform_simulated_keypress(message.strip("press ").strip(""))
                    elif "type" in message_low[0:4] or "write" in message_low[0:5] or "bright" in message_low[0:6] or "great" in message_low[0:5]:
                        # Remove "bright ", "write ", "type ", "great " from the message:
                        new_message = message.replace("bright ", "").replace("write ", "").replace("type ", "").replace("great ", "")
                        print("Typing:", new_message)
                        write_action(goal=new_message, last_step="text_entry")
                    elif "reminder" in message_low or "remind" in message_low or "timer" in message_low or "alarm" in message_low:
                        # Call internal_clock.py - Generated.
                        # Here's thoughts of when remind the user if is not noticing any important upcoming event:
                        # Advice the user for upcoming events. Add reminders, timers, alarms, etc.
                        print("Reminder: ", message)
                    elif "scroll" in message_low[0:6]:
                        print("Scrolling: ", message)
                        import pyautogui
                        pyautogui.scroll(-850)
                    else:
                        auto_prompt(message)
                else:
                    # Voice recognition was disabled while audio was being processed, skip it
                    continue
            except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
                # If you want to handle specific errors, you can separate them with additional except blocks
                pass


# Now start the listening thread when initializing
listening_thread = threading.Thread(target=listen_thread, daemon=True)
listening_thread.start()


def auto_prompt(message):
    role_function = auto_role(message)
    print(f"Assistant: {role_function.strip('windows_assistant').strip('joyful_conversation').strip(' - ')}")
    if "windows_assistant" in role_function:
        message_queue.put(f"{role_function.strip('windows_assistant').strip(' - ')}")
        # Start the assistant in a new thread:
        assistant_thread = threading.Thread(target=run_assistant, args=(message,))
        assistant_thread.start()
    elif "joyful_conversation" in role_function:
        message_queue.put(f"{role_function.strip(f'joyful_conversation').strip(' - ')} How can I help you?")
    else:
        print("NOT WORKING")


def load_image(file_path, scale=0.333):
    # Helper function to load and scale the image
    image = Image.open(file_path)
    original_width, original_height = image.size
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)
    image = image.resize((new_width, new_height), Image.Resampling.BICUBIC)
    ctk_image = Ctk.CTkImage(light_image=image, size=(new_width, new_height))
    return ctk_image, new_width, new_height


def create_app():
    global root, label, assistant_photo, assistant_dragging_photo, assistant_blink_photo, assistant_anim_enabled, is_dragging, position_right, position_bottom, drag_time, \
        assistant_voice_enabled, assistant_subtitles_enabled, assistant_name_handle, assistant_photo_width, assistant_photo_height, scale_factor # Add width and height globals
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    root = Ctk.CTk()
    root.title("AI Drone Assistant")
    root.iconbitmap("media/headico.ico")
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.wm_attributes("-transparentcolor", 'gray')

    # Load images and get their sizes
    assistant_photo, assistant_photo_width, assistant_photo_height = load_image("media/assistant_transparent.png")
    assistant_dragging_photo, _, _ = load_image("media/assistant_transparent_dragging.png")
    assistant_blink_photo, _, _ = load_image("media/assistant_transparent_blink.png")
    label = Ctk.CTkLabel(root, image=assistant_photo, bg_color="gray", cursor="hand2", text="")
    label.pack()
    label.bind('<ButtonPress-1>', start_drag)
    label.bind('<B1-Motion>', on_drag)
    label.bind('<ButtonRelease-1>', end_drag)
    label.bind('<ButtonPress-3>', show_config)

    # Calculate initial position (bottom right)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Use assistant_photo_width and assistant_photo_height instead of width() and height()
    position_right = int(screen_width - assistant_photo_width) + 35
    position_bottom = int(screen_height - assistant_photo_height) - 30
    drag_time = time.time()

    # Set initial geometry to place the assistant at the bottom right
    root.geometry(f'+{position_right}+{position_bottom}')
    is_dragging = False  # Flag to track dragging state
    root.after(1000, animate_blink)  # Start the blinking animation
    root.after(1000, animate_move)  # Start the moving animation
    root.after(100, process_queue)  # Start processing the message queue
    # Call the mainloop
    root.mainloop()
    pass

create_app()