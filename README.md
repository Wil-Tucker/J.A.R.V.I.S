# J.A.R.V.I.S

A3 Submission

## Installation

0. Install Python.
1. Create a virtual environment
```bash
py -m venv venv
```
2. Activate the virtual environment
```bash
.\venv\Scripts\activate
```
3. Install the requirements
```bash
pip install -r requirements.txt
```
4. You can now run the program using 
```bash
py run.py
```
OR
5. You can create a .exe file by running 
```bash
pyinstaller --onefile --windowed --icon=UI-Icon.ico run.py
```

## Running the .exe
0. After running
```bash
pyinstaller --onefile --windowed --icon=UI-Icon.ico run.py
```
1. Open JARVIS.exe
2. Press the 'Speak' button and say whatever you want.
3. Wait for J.A.R.V.I.S. to reply.


## Explanation
The only notable files are the 'run.py' file, which contains all modules for the code to run, and the 'requirements.txt' that installs the required libraries. 
The majority of the other files were generated when creating the .exe file.

'run.py' can be understood from top to bottom as follows:
1. The necessary imports for the code to function are run.
2. The .env file containing the required API keys is loaded.
3. The 'get_speech_input' function returns 'spoken_text' and is run using the 'speech_recognition' library, which transcribes voice input from the user or displays an error if necessary.
4. The 'spoken_text' variable is then passed to the 'get_openai_response' function, which sends the contained text to OpenAI's API.
5. Powered by the 'gpt-3.5-turbo' model, J.A.R.V.I.S. is given the prompt to tell it what it is and to respond in a concise manner, so too many tokens aren't used.
6. After determining a response to the user's input, 'jarvis_reply' is returned and passed to 'speak_response' function.
7. The 'speak_response' function uses the ElevenLabs API and the voice I selected (Matthew), and generates and streams 'jarvis_reply' to the user.

8. The 'main' function is the key to actually running the code and consists of the 'pressed_speak_button', and 'separateThreadTask' functions and GUI customization.
9. The 'main()' function sets up the GUI, initiating the code when the 'Speak' button is clicked, which calls the 'pressed_speak_button' function, running the code, and disabling the 'Speak' button.
10. The 'pressed_speak_button' function calls the 'separateThreadTask' function, which calls the 'get_speech_input' function, getting the user's spoken words.
11. If there is no error, the spoken words are passed to the 'get_openai_response' functions.
12. The spoken words are then passed to the 'speak_response' function, and the 'Speak' button is re-enabled.
13. This is all carried out on the separate thread that is created in order to avoid the window 'not-responding' issue that happens with Tkinter GUI.
14. The rest of the code mainly consists of customising the Tkinter GUI, as well as naming the pop-up window and setting its dimensions.
15. 'root.mainloop()' runs in the main thread, which is responsible for all GUI interactions.
