**PyWinAssistant** – **MIT Licensed** | **Public Release: December 31, 2023** | Complies with federal coordinations AI Standards Coordination Working Group, Asilomar AI Principles and IEEE Global Initiative on Ethics of Autonomous and Intelligent Systems.

PyWinAssistant is the first open-source Artificial Narrow Intelligence to elicit spatial reasoning and perception as a generalist agentic framework Computer-Using-Agent that fully operates graphical-user-interfaces (GUIs) for Windows 10/11 **through direct OS-native semantic interaction**. It functions as a Computer-Using-Agent / Large-Action-Model, forming the foundation for a pure **symbolic spatial cognition framework** that enables artificial operation of a computer using only natural language, **without relying on computer vision, OCR, or pixel-level imaging**. PyWinAssistant emulates, plans, and simulates synthetic Human-Interface-Device (HID) interactions through **native Windows Accessibility APIs**, eliciting human-like abstraction across geometric, hierarchical, and temporal dimensions at an Operating-System level. This OS-integrated approach simulating spatial utilization of a computer provides a future-proof, generalized, modular, and dynamic ANI orchestration framework for multi-agent-driven automation, marking an important step in symbolic reasoning towards AGI.

**Key Features:**
*   **Not relying only on Imaging Pipeline**: Operates exclusively through Windows UI Automation (UIA) and programmatic GUI semantics.
*   **Symbolic Spatial Mapping**: Hierarchical element tracking via OS-native parent/child relationships and coordinate systems.
*   **Non-Visual Perception**: Real-time interface understanding through direct metadata extraction (control types, states, positions).
*   **Visual Perception**: A single screenshot can elicit comprehension and perception with attention to detail by visualizing goal intent and environment changes in a spatial space over time, can be fine-tuned to look up for visual cues, bugs, causal reasoning bugs, static, semantic grounding, errors, corruption...

PyWinAssistant has its own set of **reasoning agents**, utilizing Visualization-of-Thought (VoT) and Chain-of-Thought (CoT) to enhance generalization, dynamically simulating actions through abstract GUI semantic dimensions rather than visual processing, making it **future-proof** for next-generation **LLM models**. By **visualizing interface contents** to dynamically **simulate and plan actions** over **abstract GUI semantic dimensions, concepts, and differentials**, PyWinAssistant **redefines computer vision automation**, enabling **high-efficiency visual processing** at a fraction of traditional computational costs. PyWinAssistant has achieved **real-time spatial perception** at an **Operating-System level**, allowing for **memorization of visual cues and tracking of on-screen changes over time**.

By **directly interfacing with Windows underlying UI hierarchy**, it achieves real-time spatial perception at the OS level while eliminating traditional computer vision pipelines, enabling:
*   **100x Efficiency Gains**: Native API access vs pixel-based analysis.
*   **Blind Operation**: Can function on headless systems, virtual machines, or minimized windows.
*   **Precision Abstraction**: Mathematical modeling of GUI relationships rather than visual pattern matching.

  **Image-Free by Design (Core Architecture)**  
While some projects *require* visual processing for fundamental operation, PyWinAssistant achieves **complete GUI interaction capability without any imaging pipeline** through:  
1. **Native OS Semantic Access**  
   Direct Windows UIA API integration provides full control metadata:  
   ```python
   # Example of an element properties via UIA - No screenshots needed
   button = uia.Element.find(Name="Submit", ControlType="Button")
   print(button.BoundingRectangle)  # {x: 120, y: 240, width: 80, height: 30}
   ```
2. **Optional Imaging Module (Assistant Context Only)**  
   For specific edge cases, we offer *completely optional* visual supplements:  
   ```diff
   # PyWinAssistant imaging functions can be enabled as real-time spatial perception with memorization of visual cues and tracking of on-screen changes over time.
   + Experimental/opt-in features may use:
   - OCR fallback / object detection for non-UIA legacy apps.
   - Visual hash matching for dynamic elements.
   # These experimental features were added but not fully developed as it was not necessary for the current implementation as it currently works too well. To release in v0.6.5.
   ```
**Key Differentiation Table**  
| | PyWinAssistant | Traditional Automation |  
|-|----------------|------------------------|  
| **Primary Perception** | UIA Metadata | Screenshots/OCR |  
| **Vision Dependency** | Optional Add-on | Required Core |  
| **Headless Ready** | ✅ Native | ❌ Requires virtual display |  

PyWinAssistant represents a major paradigm shift in AI, pioneering **pure symbolic computer interaction** through these breakthroughs:
*   **First Agent** to bypass OCR/imaging entirely for GUI automation.
*   **First Framework** using Windows UIA as the primary spatial perception channel.
*   **First System** demonstrating OS-native hierarchical-temporal reasoning.

Released before key breakthroughs in AI for Spatial Reasoning, it predates:
*   **Microsoft’s** [**Visualization-of-Thought research paper**](https://arxiv.org/abs/2404.03622) (April 4, 2024)
*   **Anthropic** [**Claude’s Computer-Use Agent**](https://www.anthropic.com/news/3-5-models-and-computer-use) (October 22, 2024)
*   **OpenIA** [**ChatGPT’s Operator Computer-Using Agent (CUA)**](https://openai.com/index/introducing-operator/) (January 23, 2025)

### **Development Notes:**
PyWinAssistant is limited to model's intelligence and time to inference. New advancements on LLM's are required to reach for AGI.
The system's autonomous task decomposition leverages **native semantic differentials** rather than visual changes, visual changes can be optionally activated for real-time image corruption analysis in GUI/Screen.
Long-term memory and self-learning mechanisms were designed to evolve **symbolic state representations**, and can be also represented into visual patterns, aligning with AGI development.

Paper related: Visualization-of-Thought Elicits Spatial Reasoning in Large Language Models:
![image](https://github.com/a-real-ai/pywinassistant/assets/18397328/58c8e18d-b633-4a35-abc1-b8a76768e4e3)
https://arxiv.org/abs/2404.03622

# Overview

PyWinAssistant includes built-in assistant features designed to enhance human-computer interaction for all users. It integrates real-time voice recognition, customizable assistant personalities, subtitles, and chat functionality.
Talk with your computer friendly and naturally to perform any User Interface activity.
Use natural language to operate freely your Windows Operating System.
Generates and plans test cases of your User Interface applications for continuous testing on any Win32api supported application by simply using natural language.
Your own open and secure personal assistant that responds as you want, control the way you want your computer to assist you.
It's engineered to be modular, understand and execute a wide range of tasks, automating interactions with any desktop applications.

# Demos (Videos below)

![image](https://github.com/a-real-ai/pywinassistant/assets/18397328/93c0f123-2d57-419f-a586-32d9fe51e0b2)

![image](https://github.com/a-real-ai/pywinassistant/assets/18397328/42d2e3d5-9be7-4d4a-825d-e80891aeb0eb)

![Screenshot 2023-12-18 043612](https://github.com/a-real-ai/pywinassistant/assets/18397328/428d1a3f-ece7-4c58-9d1b-76138ce8807c)

![Screenshot 2023-12-18 040443](https://github.com/a-real-ai/pywinassistant/assets/18397328/50543e40-f810-4e4f-9cca-3f1131ae1cc1)

![Screenshot 2023-12-01 143812](https://github.com/a-real-ai/pywinassistant/assets/18397328/d88374c9-fb53-4ecf-b8b5-840ffaa5d8c1)

![Screenshot 2023-12-01 150047](https://github.com/a-real-ai/pywinassistant/assets/18397328/f0c904c7-0c96-4d57-90a0-dc9084728131)

![Screenshot 2023-11-13 161219](https://github.com/a-real-ai/pywinassistant/assets/18397328/b2c2a23c-f37f-4f1d-8628-69db6bf13ed9)

## Please enable the Audio for the demo videos.
Voice 1 - Input Human (English Female Australian TTS)

Voice 2 - Output Assistant (English Female US Google TTS)

### Use your computer by natural language - Real-time usage of VoT, an example of a Single Action Model.
Does not use any vision. Only API LLM calls.

https://github.com/a-real-ai/pywinassistant/assets/18397328/25b39d8c-62d6-442e-9d5e-bc8a35aa971a

### Use your computer as an assistant - Real-time usage of planning VoT, an example of a Large Action Model.
Uses minimal vision. Get to know what the user is doing and what is that the user wants to achieve, the assistant plans to perform it.

https://github.com/a-real-ai/pywinassistant/assets/18397328/d04f0609-68fb-4fb4-9ac3-279047c7a4f7

### The assistant can do anything for you - Real-time usage of planning VoT, an example of a Large Action Model.
The inference is the only constraint for speed.

https://github.com/a-real-ai/pywinassistant/assets/18397328/6d3bb6e6-ccf8-4380-bc89-df512ae207f2

### Other demos with Real-time usage of planning VoT.

November 16th 2023 live demo: (Firefox, Spotify, Notepad, Calculator, Mail)

https://github.com/a-real-ai/pywinassistant/assets/18397328/ce574640-5f20-4b8e-84f9-341fa102c0e6

December 1st 2023 live demo: (Chrome, Spotify, Firefox)

https://github.com/a-real-ai/pywinassistant/assets/18397328/7e0583d1-1c19-40fa-a750-a77fff98a6da

Currently supporting all generalized win32api apps, meaning:
Chrome, Firefox, OperaGX, Discord, Telegram, Spotify...

# Key Features
- Dynamic Case Generator: The assistant() function accepts a goal parameter, which is a natural language command, and intelligently maps it to a series of executable actions. This allows for a seamless translation of user intentions into effective actions on the computer.
1. Single Action Execution:
The act() function is a streamlined method for executing actions, enhancing the tool's efficiency and responsiveness.
2. Advanced Context Handling: The framework is adept at understanding context by analyzing the screen and the application, ensuring that actions are carried out with an awareness of the necessary prerequisites or steps.
3. Semantic router map: The framework has a database of a semantic router map to successfully execute generated test cases. This semantic maps can be created by other AI.
4. Wide Application Range: From multimedia control (like playing songs or pausing playback on Spotify and YouTube) to complex actions (like creating AI-generated text, sending emails, or managing applications like Telegram or Firefox), the framework covers a broad spectrum of tasks.
5. Customizable AI Identity: The write_action() function allows for a customizable assistant identity, enabling personalized interactions and responses that align with the user's preferences or the nature of the task.
6. Robust Error Handling and Feedback: The framework is designed to handle unexpected scenarios gracefully, providing clear feedback and ensuring reliability. (In Overview)
7. Projects for mood and personality: Generate or suggest now and then useful scenarios based on your mood and personality. (In Overview)


# Technical Innovations
1. Natural Language Processing (NLP): Employs advanced NLP techniques to parse and understand user commands in a natural, conversational manner.
2. Task Automation Algorithms: Utilizes sophisticated algorithms to break down complex tasks into executable steps.
3. Context-Aware Execution: Integrates contextual awareness for more nuanced and effective task execution.
4. Cross-Application Functionality: Seamlessly interfaces with various applications and web services, demonstrating extensive compatibility and integration capabilities.
5. Use Cases.
6. Automating repetitive tasks in a Windows environment.
7. Streamlining workflows for professionals and casual users alike.
8. Enhancing accessibility for users with different needs, enabling voice or simple text commands to control complex actions.
9. Assisting in learning and exploration by providing AI-driven guidance and execution of tasks.


# Conclusion
This Artificially Assisted User Interface Testing framework is a pioneering tool in the realm of desktop automation. Its ability to understand and execute a wide range of commands in a natural, intuitive manner makes it an invaluable asset for anyone looking to enhance their productivity and interaction with their Windows environment. It's not just a tool; it's a step towards a future where AI seamlessly integrates into our daily computing tasks, making technology more accessible and user-friendly.

# Installation
```
# Add your Chat-GPT API Keys to the project:
Create a .env file with your API Key in the project folder 
and add your key like this: OPENAI_API_KEY=sk-pr....


# Install requirements:
cd pywinassistant
pip install -r .\requirements.txt

# Execute the assistant:
cd .\core
python ./assistant.py
```

# Usage
Run "Assistant.py", say "Ok computer" to enable the assistant by voice commands or click to it or enable the chat to do a fast action. Use Right click above the Assistant to see the available options for the assistant.

For debugging mode execute "Driver.py". Inside it, you can debug and try easily the functions of "act" which is used alongside the assistant, "fast_act" and "assistant" by using the examples.
To run a JSON test case, modify the JSON path from the "assistant" function.

# Working cases (on cases.py)

```
assistant(goal=f"Play the song \'One More Time - Daft Punk\' on Spotify")  # Working 100%
assistant(goal=f"Open a new tab the song \'Wall Of Eyes - The Smile\', from google search results filter by videos then play it on Firefox")  # Working 100%
assistant(goal=f"Open a new tab the song \'Windows XP Error beat\', from google search results filter by videos then play it by clicking on the text on Firefox.")  # Working 100%
fast_act(goal=f"Click on the Like button") # Working 100%
assistant(goal=f"Pause the music on Spotify")  # Working 100%
write_action(goal="Comment about why IA is great for the current playing song", assistant_identity="You\'re an advanced music AI agent that specializes on music") # Working 100%
assistant(f"Create a long AI essay about an AI Starting to control a Windows computer on Notepad")  # Working 100%
fast_act(goal="Click on the button at the bottom in HueSync app")  # Working 100%
write_action(goal="Weird Fishes - Radiohead")  # Working 100%
assistant(f"Open Calc and press 4 x 4 - 4 * 4 + 1 =")  # Working 100%
assistant(goal=f"Open 3 new tabs on google chrome and in each of them search for 3 different types of funny dogs", keep_in_mind=" Filter the results by images.")  # Working 100%
assistant(goal=f"Stop the playback from Firefox app")  # Working 100%
assistant(f"Send a list of steps to make a joke about engineers whilist making it an essay to my friend Diana in Telegram")  # Working 100%
assistant(f"Send a list of steps to make a chocolate cake to my saved messages in Telegram")  # Working 100%
assistant(f"Create three new tabs on Firefox, in each of them search 3 different types of funny youtube bad tutorial videos, generate the titles to search.")  # Working 100%
assistant(f"Write an essay about an AI that a person created to use freely the computer, like you. Write it in notepad.exe") # Working 100%
assistant(f"Send an AI joke and say it's generated by an AI to my friend Diana on Discord")  # Working 100%
assistant(goal=f"Create a short greet text for the user using AI Automated Windows in notepad.exe") # Working 100%
assistant(goal=f"Open calc.exe and press 4 x 4 =")  # Working 100%
assistant(goal=f"Send a mail to \'testmail@gmail.com\' with the subject \'Hello\' and generate the message \'Generate a message about how an AI is helping everyone as an users\' on the Mail app",
          keep_in_mind="Press \'Tab\' tree times to navigate to the subject area. Do not combine steps.")  # Need to update the app semantic map to get it working 100%.
assistant(goal=f"Play the song \'The Smile - Wall Of Eyes\' on Spotify")  # Working 100%
assistant(goal=f"Play the song \'Panda Bear - Tropic of cancer\' on Spotify")  # Working 100%
assistant(goal="Pause the music on the Spotify app")  # Working 100%
assistant(goal=f"Open 3 new tabs with different Daft Punk songs on each of them on Firefox")  # Working 100%
fast_act("Open spotify and Search the album \'Grimes - Visions\'")  # Working 100%
write_action("Open spotify and Search the album \'Grimes - Visions\'")  # Working 100%
fast_act("Click on the first result on spotify")  # Working 100%
fast_act("Skip to the next song on Spotify")  # Working 100%
fast_act("Add the album to the library")  # Working 100%
fast_act("Go to Home on Spotify")  # Working 100%
fast_act("Save the song to my library on Spotify")  # Working 100%
```


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


### Notes:

This project is being updated as of start of 2024. The list of requirements is being updated.
