import uiautomation as auto

#not used

def walk_control(control, indent=0, control_type=None):
    if control is None:
        return
    try:
        if (control_type is None) or (control.ControlType == auto.ControlType[control_type]):
            # Print control info with indentation
            print(' ' * indent + str(control))
            # ... print additional properties if needed ...
    except Exception as e:
        print(' ' * (indent + 2) + 'Error getting properties: ' + str(e))
    # Recursively walk the tree
    for child in control.GetChildren():
        walk_control(child, indent + 4, control_type=control_type)


def analyze_app(application_name=None, control_type=None):
    if application_name:
        # Find the application window by name
        control = auto.WindowControl(searchDepth=1, Name=application_name)
        if not control.Exists(0, 0):
            print(f'Application "{application_name}" is not running or window not found.')
            return
        print(f'Inspecting UI elements for application "{application_name}":')
    else:
        control = auto.GetRootControl()
        print('Inspecting UI elements for the entire desktop:')

    # If a specific control type is given, filter by that control type
    if control_type and control:
        # Walking the control tree and checking for the control type in the walk_control function
        walk_control(control)
    else:
        # Walk the entire UI tree from the control
        walk_control(control)

if __name__ == '__main__':
    analyze_app(application_name='Untitled - Paint', control_type='Edit')
