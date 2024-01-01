import uiautomation as auto


def walk_control(control, indent=0, control_type=None, search_strings=None):
    matched = []
    unmatched = []
    if control is None:
        return matched, unmatched
    if control_type is None or control.ControlType == control_type:
        try:
            rect = control.BoundingRectangle
            area = (rect.right - rect.left) * (rect.bottom - rect.top)
            control_tuple = (control, area)
            if search_strings and any(s.lower() in control.Name.lower() for s in search_strings):
                matched.append(control_tuple)
            else:
                unmatched.append(control_tuple)
        except Exception as e:
            print(f"{' ' * indent}Error getting properties: {e}")

    for child in control.GetChildren():
        child_matched, child_unmatched = walk_control(child, indent + 2, control_type=control_type, search_strings=search_strings)
        matched.extend(child_matched)
        unmatched.extend(child_unmatched)
    return matched, unmatched


def sort_and_categorize_rects(controls_with_rects, size_category_to_print=None):
    sorted_by_area = sorted(controls_with_rects, key=lambda x: x[1], reverse=True)
    categorized = {'Bigger': [], 'Medium': [], 'Small': []}

    for control, area in sorted_by_area:
        if area >= 1000000:
            categorized['Bigger'].append(control)
        elif area >= 100000:
            categorized['Medium'].append(control)
        else:
            categorized['Small'].append(control)

    output = []
    for category, controls in categorized.items():
        output.append(f"{category} elements:")
        for control in controls[:150]:
            output.append(f"{control}")
        output.append("")  # For an empty line between categories

    return "\n".join(output).strip()


def analyze_app(application_name_contains=None, size_category=None, additional_search_options=None):
    root = auto.GetRootControl()

    control = None
    if application_name_contains:
        for win in root.GetChildren():
            if application_name_contains.lower() in win.Name.lower():
                control = win
                break
        if not control:
            return f'Window containing "{application_name_contains}" not found.'
    else:
        control = root

    if not control.Exists(0, 0):
        return f'Application with title containing "{application_name_contains}" is not running or window not found.'

    search_strings = additional_search_options.lower().split(',') if additional_search_options else []
    search_strings = [s.strip() for s in search_strings if s.strip()]

    matched_controls_with_rects, unmatched_controls_with_rects = walk_control(control, control_type=None, search_strings=search_strings)

    output = "Matched controls:\n"
    output += sort_and_categorize_rects(matched_controls_with_rects, size_category_to_print=size_category)
    output += "\nUnmatched controls:\n"
    output += sort_and_categorize_rects(unmatched_controls_with_rects, size_category_to_print=size_category)
    return output


# Usage example
if __name__ == '__main__':
    search_options = "contenteditable"
    search_terms = search_options.replace('', '').strip()
    print(search_terms)
    print(analyze_app(application_name_contains='Firefox', additional_search_options=search_terms))