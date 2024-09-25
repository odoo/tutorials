# Module 4: Customize Fields and Views

starting situation:

A shelter application
models:
    animal
    animal_type 
        - name
        - pictogram (optional)
    animal_race
        - name
    contact

# 1. Add a ribbon Adopted on cat image when stage = adopted

Exercice so they understand how to add a view widget into the view
Add it on the form view and the kanban card

# 2. Displaying a custom view banner

Exercice to now create and add a view widget
view widget: if animal is there > 6month and not adopted => message

# 3. Subclass A char field  to generate a name

subclass char field
add button [GENERATE NAME] (static list of names for simplicity)
only visible if name is not set

# 4. customize status bar widget to add a rainbow man

There is a statusBarField on the form view, for the state of the animal
Create an extension of the field widget so that a rainbowman appears when the state is set to adopted.

# 5. Pictogram/type in list view

Animals have a type (cat, dog, etc). Those types can have a pictogram.
We want an extension of a one2many field widget to display the name and the pictogram a little bit like the one2many_avatar.

# 6. view extension

Extend the kanban view to reload it's data every 10 seconds or so.
Business case is that the kanban view is shown on a screen somewhere in the shelter.

