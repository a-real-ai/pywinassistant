# PyWinAssistant
"PyWinAssistant" is an open-source Windows 10/11 Python framework to artificially assist the user interface using chatGPT API without using OCR and with minimal usage of vision models.

Image analysis is implemented but not used. It's a work in progress to use the minimal data.
AI-Driven UI Testing Framework using the win32api "PyWinAssistant," an innovative Apache 2.0 open-source Python framework designed for Windows 10/11. This project pioneers a new approach in UI assistance and testing by leveraging the capabilities of ChatGPT.

###  Overview
Talk with your computer friendly and naturally. 

Use natural language to operate freely your Windows Operating System.

Generate test cases of your UI applications for continuous testing on any Win32api supported application by simply using natural language.

Your own open personal assistant that responds as you want, control the way you want your computer to assist you.

It's engineered to be modular, understand and execute a wide range of tasks, from playing music on Spotify to conducting specific tasks on the internet, and even automating interactions with desktop applications.

### Key Features
- Dynamic Case Generator: The assistant() function accepts a goal parameter, which is a natural language command, and intelligently maps it to a series of executable actions. This allows for a seamless translation of user intentions into effective actions on the computer.
1. Single Action Execution:
The act() function is a streamlined method for executing single, straightforward actions, enhancing the tool's efficiency and responsiveness.
2. Advanced Context Handling: The framework is adept at understanding context through the keep_in_mind parameter, ensuring that actions are carried out with an awareness of the necessary prerequisites or steps.
3. Wide Application Range: From multimedia control (like playing songs or pausing playback on Spotify and YouTube) to complex actions (like creating AI-generated text, sending emails, or managing applications like Telegram or Firefox), the framework covers a broad spectrum of tasks.
4. Customizable AI Identity: The write_action() function allows for a customizable assistant identity, enabling personalized interactions and responses that align with the user's preferences or the nature of the task.
5. Robust Error Handling and Feedback: The framework is designed to handle unexpected scenarios gracefully, providing clear feedback and ensuring reliability. (In Overview)
5. Projects for mood and personality: Generate or suggest now and then useful scenarios basing in your mood and personality. (In Overview)

### Technical Innovations:
1. Natural Language Processing (NLP): Employs advanced NLP techniques to parse and understand user commands in a natural, conversational manner.
2. Task Automation Algorithms: Utilizes sophisticated algorithms to break down complex tasks into executable steps.
3. Context-Aware Execution: Integrates contextual awareness for more nuanced and effective task execution.
4. Cross-Application Functionality: Seamlessly interfaces with various applications and web services, demonstrating extensive compatibility and integration capabilities.
5. Use Cases.
6. Automating repetitive tasks in a Windows environment.
7. Streamlining workflows for professionals and casual users alike.
8. Enhancing accessibility for users with different needs, enabling voice or simple text commands to control complex actions.
9. Assisting in learning and exploration by providing AI-driven guidance and execution of tasks.

### Conclusion:
This Artificially Assisted User Interface Testing framework is a pioneering tool in the realm of desktop automation. Its ability to understand and execute a wide range of commands in a natural, intuitive manner makes it an invaluable asset for anyone looking to enhance their productivity and interaction with their Windows environment. It's not just a tool; it's a step towards a future where AI seamlessly integrates into our daily computing tasks, making technology more accessible and user-friendly.

# Usage
Run "Assistant.py", talk to it or enable the chat. Use Right click above the Assistant to see the available options for the assistant.
For debugging mode execute "Driver.py". Inside it you can debug and try easily the funcitons of "act", "fast_act" and "assitant" by using the examples.
To run a JSON test case, modify the JSON path from the "assistant" function.

# Working cases (on cases.py)

```
assistant(goal=f"Play the song \'One More Time - Daft Punk\' on Spotify", keep_in_mind=f"To start playback double click the song.")  # Working 100%
assistant(goal=f"Open a new tab the song \'Wall Of Eyes - The Smile\', from google search results filter by videos then play it on Firefox")  # Working 100%
assistant(goal=f"Open a new tab the song \'Windows XP Error beat\', from google search results filter by videos then play it by clicking on the text on Firefox.")  # Working 100%
act(goal=f"Click on the Like button on Mozilla Firefox")
assistant(goal=f"Pause the music on Spotify")  # Working 100%
act("Inside of Youtube, Add a comment on Mozilla Firefox") # Working 100%
write_action(goal="Comment about why IA is great for the current playing song", assistant_identity="You\'re an advanced music AI agent that specializes on music") # Working 100%
assistant(f"Create a long AI essay about an AI Starting to control a Windows computer on Notepad")  # Working 100%
act(goal="Click on Stop Light Sync button in HueSync app")  # Working 100%
act(goal="Click on the button at the bottom in HueSync app")  # Working 100%
write_action(goal="Weird Fishes - Radiohead")  # Working 100%
assistant(f"Open Calc and press 4 x 4 - 4 * 4 + 1 =")  # Working 100%
assistant(goal=f"Open 3 new tabs on google chrome and in each of them search for 3 different types of funny dogs", keep_in_mind=" Filter the results by images.")  # Working 100%
assistant(goal=f"Stop the playback from Firefox app")  # Working 100%
assistant(f"Send a list of steps to make a joke about engineers whilist making it an essay to my friend Diana in Telegram")  # Working 100%
assistant(goal=f"Open the Photos folder on the Windows Explorer") # works weird but it complies the goal. Working 100%
assistant(f"Send a list of steps to make a chocolate cake to my saved messages in Telegram")  # Working 100%
assistant(f"Create three new tabs on Firefox, in each of them search 3 different types of funny youtube bad tutorial videos, generate the titles to search.")  # Working 100%
assistant(f"Write an essay about an AI that a person created to use freely the computer, like you. Write it in notepad.exe") # Working 100%
assistant(f"Send a list of steps to make a cake to my friend X in Telegram")  # Working 100%
assistant(f"Send an AI joke and say it's generated by an AI to my friend X on Discord")  # Working 100%
assistant(goal=f"Create a short greet text for the user using AI Automated Windows in notepad.exe") # Working 100%
assistant(goal=f"Open calc.exe and press 4 x 4 =")  # Working 100%
assistant(goal=f"Send a mail to \'testmail@gmail.com\' with the subject \'Hello\' and generate the message \'Generate a message about how an AI is helping everyone as an users\' on the Mail app",
          keep_in_mind="Press \'Tab\' tree times to navigate to the subject area. Do not combine steps.")  # Working 100% and also it sends it lol
assistant(goal=f"Play the song \'The Smile - Wall Of Eyes\' on Spotify", keep_in_mind=f"To start playback double click the song.")  # Working 100%
assistant(goal=f"Play the song \'Panda Bear - Tropic of cancer\' on Spotify", keep_in_mind=f"To start playback double click the song.")  # Working 100%
assistant(goal="Pause the music on the Spotify app")  # Working 100%
assistant(goal=f"Open 3 new tabs with different Daft Punk songs on each of them on Firefox")  # Working 100%
act("Open spotify and Search the album \'Grimes - Visions\'")  # Working 100%
write_action("Open spotify and Search the album \'Grimes - Visions\'")  # Working 100%
act("Click on the first result on spotify")  # Working 100%
act("Click on the green play button on spotify")  # Working 100%
act("Skip to the next song on Spotify")  # Working 100%
act("Add the album to the library")  # Working 100%
act("Go to Home on Spotify")  # Working 100%
act("Save the song to my library on Spotify")  # Working 100%
# Other actions:
act("Click on the button start the light sync in Phillips Hue App")
```
___
# Current approaches to UI Testing
### There are three main types of GUI testing approaches, namely:

1. ***Manual Testing:***

In manual testing, a human tester performs a set of operations to check whether the application is functioning correctly and that the graphical elements conform to the documented requirements. Manual-based testing has notable downsides in that it can be time-consuming, and the test coverage is extremely low. Additionally, the quality of testing in this approach depends on the knowledge and capabilities of the testing team.

2. ***Record-and-Playback Testing:***

Also known as record-and-replay testing, it is executed using automation tools. The automated UI testing tool records all tasks, actions, and interactions with the application. The recorded steps are then reproduced, executed, and compared with the expected behavior. For further testing, the replay phase can be repeated with various data sets.

3. ***Model-Based Testing:***

In this testing approach, we focus on building graphical models that describe the behavior of a system. This provides a deeper understanding of the system, which allows the tester to generate highly efficient test cases. In the models, we determine the inputs and outputs of the system, which are in turn, used to run the tests. Model-based testing works as follows:

    Create a model for the system
    Determine system inputs
    Verify the expected output
    Execute tests
    Check and validate system output vs. the expected output

The model-based approach is great because it allows a higher level of automation. It also covers a higher number of states in the system, thereby improving the test coverage.

# New Approaches to UI Testing using AI
4. ***Artificially Assisted User Interface Testing:***

Artificially Assisted User Interface Testing harnesses the power of artificial intelligence to revolutionize the process of testing graphical user interfaces. Unlike traditional methods, Artificially Assisted User Interface Testing integrates machine learning algorithms and intelligent decision-making processes to autonomously identify, analyze, and interact with UI elements. This approach significantly enhances the depth and breadth of testing in several ways:

    Dynamic Interaction with UI Elements: AI-driven tests can adapt to changes in the UI, such as modified button locations or altered element properties. This flexibility is achieved through the use of AI models trained to recognize and interact with various UI components, regardless of superficial changes.
    Learning and Pattern Recognition: Utilizing machine learning, Artificially Assisted User Interface Testing systems can learn from previous interactions, test runs, and user feedback. This enables the AI to recognize patterns and predict potential issues, improving over time and offering more thorough testing with each iteration.
    Automated Test Case Generation: The AI can generate test cases based on its understanding of the application's functionality and user behavior patterns. This not only saves time but also ensures that a wider range of scenarios is tested, including edge cases that might be overlooked in manual testing.
    Natural Language Processing (NLP): AI Testing tools often incorporate NLP to interpret and execute tests written in plain language. This feature makes the testing process more accessible to non-technical stakeholders and facilitates better communication across the team.
    Real-Time Feedback and Analytics: AI systems provide real-time insights into the testing process, identifying bugs, performance issues, and usability problems promptly. This immediate feedback loop enables quicker rectifications and enhances the overall quality of the product.
    Predictive Analysis and Risk Assessment: By analyzing past data, Artificially Assisted User Interface Testing tools can predict potential problem areas and allocate testing resources more efficiently. This proactive approach to risk management ensures that critical issues are identified and addressed early in the development lifecycle.

In conclusion, Artificially Assisted User Interface Testing represents a significant leap forward in software quality assurance. By automating and enhancing the testing process, AI-driven tools offer improved accuracy, speed, and coverage, paving the way for more reliable and user-friendly applications.
