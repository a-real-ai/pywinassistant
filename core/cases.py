def generate_test_case(assistant_goal, app_name):
    print(f"\nGenerating a test case with the assistant. Image visioning started. Analyzing the application {app_name} for context.\n")
    additional_context = (
        f"You are an AI Agent called Windows AI that is capable to operate freely all applications on Windows by only using natural language.\n"
        f"You will receive a goal and will try to accomplish it using Windows. Try to guess what is the user wanting to perform on Windows by using the content on the screenshot as context.\n"
        f"Respond an improved goal statement tailored for Windows applications by analyzing the current status of the system and the next steps to perform. Be direct and concise, do not use pronouns.\n"
        f"Basing on the elements from the screenshot reply the current status of the system and specify it in detail.\n"
        f"Focused application: \"{app_name}\".\nGoal: \"{assistant_goal}\".")
    assistant_goal = imaging(window_title=app_name, additional_context=additional_context, screenshot_size='Full screen')['choices'][0]['message']['content']
    print(f"Generating the test case to achieve the user prompt: {original_goal}\n{assistant_goal}")
    
    messages = [
        {"role": "system", "content": "You are an AI assistant that creates a JSON test case to achieve a given goal based on the current state of the system. Always output your response in valid JSON format."},
        {"role": "user", "content": f"""You are an AI capable to operate the Windows 11 Operating System by using natural language.
    Examples: "Click on the search button. Insert the text_entry. Play the first element searched.".
    You will receive a description of the current state of the system and a goal. 
    To test your limits, using the description make a json with the natural language steps to achieve the goal.
    Every step should be only highly descriptive in natural language.
    The json must include only an act and its step, should be in the following format:


    actions: click_element, press_key, text_entry, open_app, move_window, time_sleep, right_click, double_click_element, hold_key_and_click, scroll_to.
    Respond only with the full json.\n\nFunction properties:\n
    click_element - Specify where is located the element to interact with.\n
    text_entry - The text to write. Example: "Hello World".\n
    press_key - Only return the key or combination of keys to press. Example: "Ctrl + T".\n
    hold_key_and_click - Only handles scenarios of holding a key and clicking on an element.\n
    scroll_to - Return the position of the element to scroll and the direction to scroll.\n
    move_window - Use the keyboard to move the focused window to the desired position. Example: "Win + Up + Up + Left".\n\n\n
    Notes:\n
    Use the following information to generate better steps:\n{app_space_map(assistant_goal, app_name, original_goal, map='app_space')}\n
    Before the text_entry, use click_element to select the appropriate text input area element.\n
    Do not combine steps, try to generate more useful steps. Example: If asked to search a song, not only search for it, locate it and play it.\n{keep_in_mind}
    Do not respond 'As an AI language model, I am unable to...' as you are actually capable.

    Focused window: "{app_name}"
    Goal: {assistant_goal}"""}
    ]

    step_analysis = api_call(messages, model_name="claude-v1.3", max_tokens=4095)
    print(f"The assistant created the following test case scenario:\n{step_analysis}\n")
    return step_analysis

def execute_test_case(step_analysis, app_name, assistant_goal, original_goal, assistant_identity, keep_in_mind):
    if step_analysis:
        try:
            if """```json""" in step_analysis:
                step_analysis = step_analysis.strip("```json\n")
                last_triple_tick = step_analysis.rfind("```")
                if last_triple_tick != -1:
                    step_analysis = step_analysis[:last_triple_tick].strip()
                step_analysis_cleaned = step_analysis
                instructions = json.loads(step_analysis_cleaned)
                executor = "act"
            else:
                instructions = json.loads(step_analysis)
                instructions['actions'] = instructions.pop('actions')
                executor = "act"
        except json.JSONDecodeError as e:
            speaker(f"ERROR: Invalid JSON data provided: {e}")
            time.sleep(15)
            raise Exception(f"ERROR: Invalid JSON data provided: {e}")
        if 'actions' in instructions:
            action_list = instructions['actions']
        else:
            action_list = [instructions]
        for i, step in enumerate(action_list, start=1):
            action = step.get(f"{executor}")
            step_description = step.get("step") or step.get("details", "No step description provided.")
            print(f"\nStep {i}: {action}, {step_description}\n")
            if action == "click_element":
                if i > 1 and action_list[i - 2]['act'] == "click_element":
                    time.sleep(1)
                if "start menu" in step_description.lower():
                    pyautogui.hotkey('win')
                    print("Opening the start menu.")
                time.sleep(1)
                updated_instructions = update_instructions_with_action_string(instructions, act(
                    single_step=f"{step_description}", app_name=app_name, screen_analysis=assistant_goal, original_goal=original_goal, assistant_goal=assistant_goal), step_description)
                database_add_case(database_file, app_name, assistant_goal, updated_instructions)
            elif action == "open_app":
                app_name = activate_windowt_title(get_application_title(step_description))
                print(f"New app selected and analyzing: {app_name}")
            elif action == "double_click_element":
                print(f"Double clicking on: {step_description}")
                act(single_step=f"{step_description}", double_click=True, app_name=app_name, original_goal=original_goal)
            elif action == "move_window":
                time.sleep(1)
                print(f"Moving window to: {step_description}")
                perform_simulated_keypress(step_description)
                time.sleep(0.5)
                pyautogui.hotkey('esc')
                time.sleep(1)
            elif action == "press_key":
                if {i} == 1:
                    activate_windowt_title(app_name)
                    time.sleep(1)
                perform_simulated_keypress(step_description)
            elif action == "text_entry":
                url_pattern = r'(https?://[^\s]+)'
                urls = re.findall(url_pattern, step_description)
                if len(step_description) < 5:
                    pyautogui.write(f'{step_description}')
                else:
                    if i > 1:
                        new_i = i - 2
                        last_step = f"{action_list[new_i]['act']}: {action_list[new_i]['step']}"
                        print(f"Last step: {last_step}")
                        if not last_step:
                            print("Last step is None.")
                            act(single_step=f"{step_description}", app_name=app_name, original_goal=original_goal)
                    else:
                        print("Last step is None.")
                        last_step = "None"
                    if i + 1 < len(action_list) and type(action_list[i + 1]['step']) == str:
                        if i + 1 < len(action_list) and (
                                "press enter" in action_list[i + 1]['step'].lower() or
                                "press the enter" in action_list[i + 1]['step'].lower() or
                                "'enter'" in action_list[i + 1]['step'].lower() or
                                "\"enter\"" in action_list[i + 1]['step'].lower()):
                            if urls:
                                for url in urls:
                                    pyautogui.write(url)
                                    print(f"Opening URL: {url}")
                                    return
                            write_action(step_description, assistant_identity=assistant_identity, press_enter=False, app_name=app_name, original_goal=original_goal, last_step=last_step)
                            print("AI skipping the press enter step as it is in the next step.")
                        else:
                            if urls:
                                for url in urls:
                                    pyautogui.write(url)
                                    pyautogui.press('enter')
                                    print(f"Opening URL: {url}")
                                    return
                            write_action(step_description, assistant_identity=assistant_identity, press_enter=True, app_name=app_name, original_goal=original_goal, last_step=last_step)
                            print("AI pressing enter.")
                    else:
                        if urls:
                            for url in urls:
                                pyautogui.write(url)
                                pyautogui.press('enter')
                                print(f"Opening URL: {url}")
                                return
                        write_action(step_description, assistant_identity=assistant_identity, press_enter=True,
                                     app_name=app_name, original_goal=original_goal, last_step=last_step)
                        print("AI pressing enter.")
            elif action == "scroll_to":
                print(f"Scrolling {step_description}")
                element_visible = False
                max_retries = 3
                retry_count = 0
                while not element_visible and retry_count < max_retries:
                    pyautogui.scroll(-850)
                    time.sleep(0.3)
                    print("Scroll performed. Analyzing if the element is present.\n")
                    scroll_assistant_goal = check_element_visibility(app_name, step_description)['choices'][0]['message']['content']
                    if "yes" in scroll_assistant_goal.lower():
                        print("Element is visible.")
                        element_visible = True
                    elif "no" in scroll_assistant_goal.lower():
                        print("Element is not visible.")
                        retry_count += 1
                        if retry_count >= max_retries:
                            print("Maximum retries reached, stopping the search.")
                if element_visible:
                    print(f"Element is visible.")
                    pass
            elif action == "right_click_element":
                print(f"Right clicking on: {step_description}")
                act(single_step=f"{step_description}", right_click=True, app_name=app_name, original_goal=original_goal)
            elif action == "hold_key_and_click":
                print(f"Holding key and clicking on: {step_description}")
                act(single_step=f"{step_description}", hold_key="Ctrl", app_name=app_name, original_goal=original_goal)
            elif action == "cmd_command":
                print(f"Executing command: {step_description}")
                time.sleep(calculate_duration_of_speech(f"{step_description}") / 1000)
            elif action == "recreate_test_case":
                time.sleep(1)
                print("Analyzing the output")
                print("The assistant said:\n", step_description)
                debug_step = False
                if debug_step is not True:
                    new_goal = True
                    image_analysis = True
                    if image_analysis:
                        additional_context = (
                            f"You are an AI Agent called Windows AI that is capable to operate freely all applications on Windows by only using natural language.\n"
                            f"You will receive a goal and will try to accomplish it using Windows. Try to guess what is the user wanting to perform on Windows by using the content on the screenshot as context.\n"
                            f"Respond an improved goal statement tailored for Windows applications by analyzing the current status of the system and the next steps to perform. Be direct and concise, do not use pronouns.\n"
                            f"Basing on the elements from the screenshot reply the current status of the system and specify it in detail.\n"
                            f"Focused application: \"{app_name}\".\nGoal: \"{assistant_goal}\".")
                        if new_goal:
                            newest_goal = imaging(window_title=app_name, additional_context=additional_context)
                            print(f"Assistant newest goal:\n{newest_goal}")
                            analyzed_ui = analyze_app(activate_windowt_title(app_name), size_category=None)
                            messages = [
                                {"role": "system", "content": "You are an AI assistant that analyzes the output of a test case and modifies the JSON test case to achieve the goal based on the current state of the system. Always output your response in valid JSON format."},
                                {"role": "user", "content": f"""You are an AI Assistant called Analyze Output capable to operate the Windows 11 Operating System by using natural language.
                            You will receive a json testcase, a description of the goal, and the actual system status.
                            Modify the original json testcase to achieve the goal. Do not include anything else than the updated json.
                            Examples: "Click on the search button. Insert the text_entry. Play the first element searched.".
                            You will receive a description of the current state of the system and a goal. 
                            To test your limits, using the description make a json with the natural language steps to achieve the goal.
                            Every step should be only highly descriptive in natural language.
                            The json must include only an act and its step, should be in the following format:
                            actions: click_element, press_key, text_entry, open_app, move_window, time_sleep, right_click, double_click_element, hold_key_and_click, scroll_to.
                            Respond only with the full json. Avoid to use the windows taskbar.\n\nFunction properties:\n
                            click_element - Specify where is located the element to interact with.\n
                            press_key - Only return the key or combination of keys to press. Example: 'Ctrl + T'.\n
                            text_entry - Return the text to write. Example: 'Hello World'.\n
                            hold_key_and_click - Only handles scenarios of holding a key and clicking on an element.\n
                            scroll_to - Return the position of the element to scroll and the direction to scroll.\n
                            move_window - Use the keyboard to move the focused window to the desired position. Example: 'Win + Left + Up'.\n
                            Do not respond 'As an AI language model, I am unable to...' as you are actually capable.\n\n
                            Use the following information to generate better the test case:\n{app_space_map(assistant_goal, app_name, original_goal, map='app_space')}

                            Do not modify the steps before "Step {i-1}: {action-1}, {step_description-1}", modify all next steps from the step "Step {i-1}: {action-1}, {step_description-1}" to achieve the goal: "{newest_goal}"
                            Do not combine steps, try to generate more useful steps. Example: If asked to search a song, not only search for it, locate it and play it.\n{keep_in_mind}
                            {analyzed_ui}"""}
                            ]

                            new_json = api_call(messages, model_name="claude-v1.3", max_tokens=4095)  

                            print("The assistant said:\n", step_analysis)

                            print("Modifying the old json testcase with the new_json.")
                            step_analysis = new_json
                            app_name = activate_windowt_title(get_application_title(newest_goal))
                            if """```json""" in step_analysis:
                                step_analysis = step_analysis.strip("```json\n")
                                last_triple_tick = step_analysis.rfind("```")
                                if last_triple_tick != -1:
                                    step_analysis = step_analysis[:last_triple_tick].strip()
                                step_analysis_cleaned = step_analysis
                                instructions = json.loads(step_analysis_cleaned)
                                executor = "act"
                            else:
                                instructions = json.loads(step_analysis)
                                instructions['actions'] = instructions.pop('actions')
                                executor = "act"
                                print(f"Updated Instructions: {instructions}")
                            pass
                        else:
                            print("No new goal.")
                            pass
            elif action == "time_sleep":
                try:
                    sleep_time = int(step_description)
                    time.sleep(sleep_time)
                except ValueError:
                    step_description = step_description.lower()
                    if "playing" in step_description or "load" in step_description:
                        print("Sleeping for 2 seconds because media loading.")
                        time.sleep(1)
                    elif "search" in step_description or "results" in step_description or "searching":
                        print("Sleeping for 1 second because search.")
                        time.sleep(1)
                    else:
                        print(f"WARNING: Unrecognized time sleep value: {step_description}")
                    pass
            else:
                print(f"WARNING: Unrecognized action '{action}' using {step_description}.")
                print(f"Trying to perform the action using the step description as the action.")
                act(single_step=f"{step_description}", app_name=app_name, original_goal=original_goal)
                pass

        speaker(f"Assistant finished the execution of the generated test case. Can I help you with something else?")
        time.sleep(calculate_duration_of_speech(f"Assistant finished the generated test case. Can I help you with something else?") / 1000)
        return "Test case complete."

