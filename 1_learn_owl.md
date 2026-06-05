# Module 1: Learn Owl 🦉

This chapter introduces the Owl framework, a tailor-made component system for
Odoo. The main building blocks of Owl are components and templates. In Owl,
every part of the user interface is managed by a component: they hold the logic
and define the templates that are used to render the user interface. In
practice, a component is represented by a small JavaScript class subclassing the
Component class.

To get started, you need a running Odoo server and a development environment
setup. Before getting into the exercises, make sure you have a working setup.

Start your development environment with a new database, on the `master` branch,
and make sure to add this repository in the addons path. Then, install the
`awesome_owl` addon. Once it is done, you can open the `/awesome_owl` route
(typically on `localhost:8069/awesome_owl`). If you see the `hello world`
message, you are ready to start!

The `awesome_owl addon` provides a simplified environment that only contains Owl
and a few other files. The goal is to learn Owl itself, without relying on Odoo
web client code.

## Content

- [Resources](#resources)
- [Example: a Counter component](#example-a-counter-component)
- [1. Displaying a Counter](#1-displaying-a-counter)
- [2. Extract Counter in a sub component](#2-extract-counter-in-a-sub-component)
- [3. A simple Card component](#3-a-simple-card-component)
- [4. Using markup to display html](#4-using-markup-to-display-html)
- [5. Props validation](#5-props-validation)
- [6. The sum of two Counter](#6-the-sum-of-two-counter)
- [6B. Bonus Project](#6b-bonus-project)
- [7. A todo list](#7-a-todo-list)
- [8. Use dynamic attributes](#8-use-dynamic-attributes)
- [9. Adding a todo](#9-adding-a-todo)
- [10. Focusing the input](#10-focusing-the-input)
- [11. Toggling todos](#11-toggling-todos)
- [12. Deleting todos](#12-deleting-todos)
- [13. Improved state management](#13-improved-state-management)
- [13B. Bonus Project: Todo class](#13b-bonus-project-todo-class)
- [14. Generic Card with slots](#14-generic-card-with-slots)
- [15. Minimizing card content](#15-minimizing-card-content)

## Resources

- [Owl repository](https://github.com/odoo/owl)
- [Owl documentation](https://github.com/odoo/owl#documentation)

## Example: a Counter component

First, let us have a look at a simple example. The Counter component shown below
is a component that maintains an internal number value, displays it, and updates
it whenever the user clicks on the button.

```js
import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
  static template = "my_module.Counter";

  setup() {
    this.state = useState({ value: 0 });
  }

  increment() {
    this.state.value++;
  }
}
```

The Counter component specifies the name of a template that represents its html.
It is written in XML using the QWeb language:

```xml
<templates xml:space="preserve">
   <t t-name="my_module.Counter">
      <p>Counter: <t t-esc="state.value"/></p>
      <button class="btn btn-primary" t-on-click="increment">Increment</button>
   </t>
</templates>
```

## 1. Displaying a counter

![A Counter component](_images/counter.png)

As a first exercise, let us modify the `Playground` component located in
`awesome_owl/static/src/` to turn it into a counter. To see the result, you can
go to the `/awesome_owl` route with your browser.

1. Modify `playground.js` so that it acts as a counter like in the example
   above. Keep `Playground` for the class name. You will need to use the
   `useState` hook so that the component is updated whenever the button is
   clicked.
2. In the same component, create an increment method.
3. Modify the template in `playground.xml` so that it displays your counter
   variable. Use
   [`t-esc`](https://github.com/odoo/owl/blob/master/doc/reference/templates.md#outputting-data)
   to output the data.
4. Add a button in the template and specify a
   [`t-on-click`](https://github.com/odoo/owl/blob/master/doc/reference/event_handling.md#event-handling)
   attribute in the button to trigger the increment method whenever the button
   is clicked.

This exercise showcases an important feature of Owl: the reactivity system. The
`useState` function wraps a value in a proxy so Owl can keep track of which
component needs which part of the state, so it can be updated whenever a value
has been changed. Try removing the `useState` function and see what happens.

**Tip:** the Odoo JavaScript files downloaded by the browser are minified. For
debugging purpose, it’s easier when the files are not minified. Switch to debug
mode with assets so that the files are not minified.

## 2. Extract Counter in a sub component

For now we have the logic of a counter in the `Playground` component, but it is
not reusable. Let us see how to create a
[sub-component](https://github.com/odoo/owl/blob/master/doc/reference/component.md#sub-components)
from it:

1. Extract the counter code from the `Playground` component into a new `Counter`
   component.
2. You can do it in the same file first, but once it’s done, update your code to
   move the `Counter` in its own folder and file. Import it relatively from
   ./counter/counter.
3. Make sure the template is in its own file, with the same name.
4. Use <Counter/> in the template of the Playground component to add two
   counters in your playground.

![Double Counter](_images/double_counter.png)

**Tip:** by convention, most components code, template and css should have the
same snake-cased name as the component. For example, if we have a `TodoList`
component, its code should be in `todo_list.js`, `todo_list.xml` and if
necessary, `todo_list.scss`

## 3. A simple Card component

Components are really the most natural way to divide a complicated user
interface into multiple reusable pieces. But to make them truly useful, it is
necessary to be able to communicate some information between them. Let us see
how a parent component can provide information to a sub component by using
attributes (most commonly known as
[props](https://github.com/odoo/owl/blob/master/doc/reference/props.md)).

The goal of this exercise is to create a `Card` component, that takes two props:
`title` and `content`. For example, here is how it could be used:

```xml
<Card title="'my title'" content="'some content'"/>
```

The above example should produce some html using bootstrap that look like this:

```html
<div class="card d-inline-block m-2" style="width: 18rem;">
  <div class="card-body">
    <h5 class="card-title">my title</h5>
    <p class="card-text">some content</p>
  </div>
</div>
```

1. Create a `Card` component
2. Import it in `Playground` and display a few cards in its template

![Simple Card](_images/simple_card.png)

## 4. Using markup to display html

If you used `t-esc` in the previous exercise, then you may have noticed that Owl
automatically escapes its content. For example, if you try to display some html
like this: `<Card title="'my title'" content="this.html"/>` with
`this.html = "<div>some content</div>""`, the resulting output will simply
display the html as a string.

In this case, since the `Card` component may be used to display any kind of
content, it makes sense to allow the user to display some html. This is done
with the
[`t-out`](https://github.com/odoo/owl/blob/master/doc/reference/templates.md#outputting-data)
directive.

However, displaying arbitrary content as html is dangerous, it could be used to
inject malicious code, so by default, Owl will always escape a string unless it
has been explicitely marked as safe with the `markup` function.

1. Update `Card` to use `t-out`,
2. Update `Playground` to import `markup`, and use it on some html values
3. Make sure that you see that normal strings are always escaped, unlike
   markuped strings.

![Markup](_images/markup.png)

**Note:** the `t-esc` directive can still be used in Owl templates. It is
slightly faster than `t-out`.

## 5. Props validation

The `Card` component has an implicit API. It expects to receive two strings in
its props object: the `title` and the `content`. Let us make that API more
explicit. We can add a props definition that will let Owl perform a validation
step in
[dev mode](https://github.com/odoo/owl/blob/master/doc/reference/app.md#dev-mode).
You can activate the dev mode in the
[App configuration](https://github.com/odoo/owl/blob/master/doc/reference/app.md#configuration)
(but it is activated by default on the `awesome_owl` playground).

It is a good practice to do props validation for every component.

1. Add
   [props validation](https://github.com/odoo/owl/blob/master/doc/reference/props.md#props-validation)
   to the Card component.
2. Rename the `title` props into something else in the playground template, then
   check in the Console tab of your browser’s dev tools that you can see an
   error.

## 6. The sum of two Counter

We saw in a previous exercise that `props` can be used to provide information
from a parent to a child component. Now, let us see how we can communicate
information in the opposite direction: in this exercise, we want to display two
`Counter` components, and below them, the sum of their values. So, the parent
component (`Playground`) need to be informed whenever one of the `Counter` value
is changed.

This can be done by using a
[callback prop](https://github.com/odoo/owl/blob/master/doc/reference/props.md#binding-function-props):
a prop that is a function meant to be called back. The child component can
choose to call that function with any argument. In our case, we will simply add
an optional `onChange` prop that will be called whenever the `Counter` component
is incremented.

1. Add prop validation to the `Counter` component: it should accept an optional
   `onChange` function prop.
2. Update the `Counter` component to call the `onChange` prop (if it exists)
   whenever it is incremented.
3. Modify the `Playground` component to maintain a local state value (`sum`),
   initially set to 2, and display it in its template
4. Implement an `incrementSum` method in `Playground`
5. Give that method as a prop to two (or more!) sub `Counter` components.

![Sum of counters](_images/sum_counter.png)

**Important:** there is a subtlety with callback props: they usually should be
defined with the .bind suffix. See the
[documentation](https://github.com/odoo/owl/blob/master/doc/reference/props.md#binding-function-props).

## 6B. Bonus Project

The code for the previous exercise is designed from a pedagogical perspective,
but the design is actually somewhat strange/fragile. This is because we are in a
situation where a parent component need to compute some value that are actually
owned by its children. So, we end up with a fragile design, where we use events
to coordinate components.

A better solution would be to reorganize the code so that the playground hold a
list of values, and give them to each `Counter`.

1. Move the state from each `Counter` component to the `Playground` component
2. Use a getter to define the sum of each value as a derived state

## 7. A todo list

Let us now discover various features of Owl by creating a todo list. We need two
components: a `TodoList` component that will display a list of `TodoItem`
components. The list of todos is a state that should be maintained by the
`TodoList`.

For this tutorial, a `todo` is an object that contains three values:

- an `id` (number),
- a `description` (string),
- and a flag `isCompleted` (boolean):

```js
{ id: 3, description: "buy milk", isCompleted: false }
```

1. Create a `TodoList` and a `TodoItem` components.
2. The `TodoItem` component should receive a `todo` as a prop, and display its
   `id` and `description` in a `div`.
3. For now, hardcode the list of todos:

   ```js
   // in TodoList
   this.todos = useState([
     { id: 3, description: "buy milk", isCompleted: false },
   ]);
   ```

4. Use
   [t-foreach](https://github.com/odoo/owl/blob/master/doc/reference/templates.md#loops)
   to display each todo in a `TodoItem`.
5. Display a `TodoList` in the playground.
6. Add props validation to `TodoItem`.

![Todo List](_images/todo_list.png)

**Tip:** since the `TodoList` and `TodoItem` components are so tightly coupled,
it makes sense to put them in the same folder.

**Note:** the `t-foreach` directive is not exactly the same in Owl as the QWeb
python implementation: it requires a `t-key` unique value, so that Owl can
properly reconcile each element.

## 8. Use dynamic attributes

For now, the `TodoItem` component does not visually show if the todo is
completed. Let us do that by using a
[dynamic attributes](https://github.com/odoo/owl/blob/master/doc/reference/templates.md#dynamic-attributes).

1. Add the Bootstrap classes `text-muted` and `text-decoration-line-through` on
   the `TodoItem` root element if it is completed.
2. Change the hardcoded `this.todos` value to check that it is properly
   displayed.

Even though the directive is named `t-att` (for attribute), it can be used to
set a class value (and other html properties such as the value of an input).

![Muted Todo](_images/muted_todo.png)

**Tip:** Owl let you combine static class values with dynamic values. The
following example will work as expected:

```xml
<div class="a" t-att-class="someExpression"/>
```

See also:
[Owl: Dynamic class attributes](https://github.com/odoo/owl/blob/master/doc/reference/templates.md#dynamic-class-attribute)

## 9. Adding a todo

So far, the todos in our list are hard-coded. Let us make it more useful by
allowing the user to add a todo to the list.

![Creating a todo](_images/create_todo.png)

1. Remove the hardcoded values in the `TodoList` component:

```js
this.todos = useState([]);
```

2. Add an input above the task list with placeholder _Enter a new task_.
3. Add an
   [event handler](https://github.com/odoo/owl/blob/master/doc/reference/event_handling.md)
   on the keyup event named addTodo.
4. Implement `addTodo` to check if enter was pressed (`ev.keyCode === 13`), and
   in that case, create a new todo with the current content of the input as the
   description and clear the input of all content.
5. Make sure the todo has a unique id. It can be just a counter that increments
   at each todo.
6. Bonus point: don’t do anything if the input is empty.

See also:
[Owl reactivity](https://github.com/odoo/owl/blob/master/doc/reference/reactivity.md)

## 10. Focusing the input

Let’s see how we can access the DOM with
[t-ref](https://github.com/odoo/owl/blob/master/doc/reference/refs.md) and
[useRef](https://github.com/odoo/owl/blob/master/doc/reference/refs.md). The
main idea is that you need to mark the target element in the component template
with a `t-ref`:

```xml
<div t-ref="some_name">hello</div>
```

Then you can access it in the JS with the
[useRef](https://github.com/odoo/owl/blob/master/doc/reference/hooks.md#useref)
hook. However, there is a problem if you think about it: the actual html element
for a component does not exist when the component is created. It only exists
when the component is mounted. But hooks have to be called in the setup method.
So, `useRef` returns an object that contains a `el` (for element) key that is
only defined when the component is mounted.

```js
setup() {
   this.myRef = useRef('some_name');
   onMounted(() => {
      console.log(this.myRef.el);
   });
}
```

1. Focus the `input` from the previous exercise. This should be done from the
   `TodoList` component (note that there is a `focus` method on the input html
   element).
2. Bonus point: extract the code into a specialized hook `useAutofocus` in a new
   `utils.js` file.

![Autofocus](_images/autofocus.png)

**Tip:** Refs are usually suffixed by `Ref` to make it obvious that they are
special objects:

```js
this.inputRef = useRef("input");
```

## 11. Toggling todos

Now, let’s add a new feature: mark a todo as completed. This is actually
trickier than one might think. The owner of the state is not the same as the
component that displays it. So, the `TodoItem` component needs to communicate to
its parent that the todo state needs to be toggled. One classic way to do this
is by adding a
[callback prop](https://github.com/odoo/owl/blob/master/doc/reference/props.md#binding-function-props)
`toggleState`.

1. Add an input with the attribute `type="checkbox"` before the id of the task,
   which must be checked if the state `isCompleted` is true.
2. Add a callback props `toggleState` to `TodoItem`.
3. Add a `change` event handler on the input in the `TodoItem` component and
   make sure it calls the `toggleState` function with the todo `id`.
4. Make it work!

![Toggling a todo](_images/toggle_todo.png)

**Tip:** Owl does not create attributes computed with the `t-att` directive if
its expression evaluates to a falsy value.

## 12. Deleting todos

The final touch is to let the user delete a todo.

1. Add a new callback prop `removeTodo` in `TodoItem`.
2. Insert `<span class="fa fa-trash ms-3 text-danger"/>` in the template of the
   `TodoItem` component.
3. Whenever the user clicks on it, it should call the `removeTodo` method.
4. Make it work!

![Deleting a todo](_images/delete_todo.png)

**Tip:** If you’re using an array to store your todo list, you can use the
JavaScript `splice` function to remove a todo from it.

```js
// find the index of the element to delete
const index = list.findIndex((elem) => elem.id === elemId);
if (index >= 0) {
  // remove the element at index from list
  list.splice(index, 1);
}
```

## 13. Improved state management

Note: this exercise (and the next one) is more advanced. Feel free to skip it.

So far, the `TodoList` has a simple architecture: a parent component `TodoList`
that holds the state and the update methods (add/remove/toggle), and a child
component `TodoItem`. This is fine for most situations, but at some point, if we
expect more and more complex features to be implemented, it is useful to
separate the _state management_ (or _model_) code from the UI code.

1. Define a `TodoModel` class. It should have a list of todos, and four methods:
   `getTodo`, `add`, `remove`, `toggle`.
2. Move all state related code from `TodoList` to `TodoModel`
3. Modify `TodoList` to instantiate a `TodoModel` in a `useState`:

   ```js
   // useState is here to make the model reactive
   this.model = useState(new TodoModel());
   ```

4. Update `TodoItem` to take 2 props: `model` and `id`
5. Make it work!

Congratulation, your state management code is now separate from your UI code!

**Tip:** it is often useful to use a `t-set` directive in a template to compute
once an important value. For example, in the template for `TodoItem`, we can do
this:

```xml
<t t-set="todo" t-value="props.model.getTodo(props.id)"/>
```

## 13B. Bonus Project: Todo class

The previous exercise successfully refactored the code to make it easier to
maintain. However, there is still something quite awkward: the `TodoItem`
receive two props, the model and the id for the todo. It is necessary to allow
the `TodoItem` to toggle and to remove the todo.

It would be nicer if we could package the state and its update function in one
convenient object. That's what OOP is for! It turns out that using simple
classes work well with Owl and the reactivity system (as long as you stay away
from private fields).

1. In `todo_model.js`, define the following `Todo` class:

   ```js
   export class Todo {
     static nextId = 1;

     constructor(model, description) {
       this._model = model;
       this.id = Todo.nextId++;
       this.description = description;
       this.isCompleted = false;
     }

     toggle() {
       this.isCompleted = !this.isCompleted;
     }

     remove() {
       this._model.remove(this.id);
     }
   }
   ```

2. Adapt `TodoModel` to use it
3. Remove `toggle` method from `TodoModel` (no longer necessary)
4. adapt `TodoItem` component to only receive a `Todo` instance as props
5. make it work!

This is a very useful pattern when working with complicated objects.

## 14. Generic Card with slots

In a previous exercise, we built a simple `Card` component. But it is honestly
quite limited. What if we want to display some arbitrary content inside a card,
such as a sub-component? Well, it does not work, since the content of the card
is described by a string. It would however be very convenient if we could
describe the content as a piece of template.

This is exactly what Owl’s
[slot](https://github.com/odoo/owl/blob/master/doc/reference/slots.md) system is
designed for: allowing to write generic components.

Let us modify the `Card` component to use slots:

1. Remove the `content` prop.
2. Use the default slot to define the body.
3. Insert a few cards with arbitrary content, such as a `Counter` component.
4. (bonus) Add prop validation.

![Generic card](_images/generic_card.png)

**See also:**
[Bootstrap: documentation on cards](https://getbootstrap.com/docs/5.2/components/card/)

## 15. Minimizing card content

Finally, let’s add a feature to the `Card` component, to make it more
interesting: we want a button to toggle its content (show it or hide it).

1. Add a state to the `Card` component to track if it is open (the default) or
   not
2. Add a `t-if` in the template to conditionally render the content
3. Add a button in the header, and modify the code to flip the state when the
   button is clicked

![Toggling a card](_images/toggle_card.png)
