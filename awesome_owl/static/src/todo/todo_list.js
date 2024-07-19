/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component
{
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup()
    {
        this.todos = useState([]);
        this.nextId = 0;
    }

    addTodo(ev)
    {
        if (ev.keyCode === 13 /* hit return */
            && ev.target.value /* string exists */)
        {
            this.todos.push({ id: this.nextId++,
                              description: ev.target.value,
                              isCompleted: false });
            ev.target.value = null; /* reset input */
        }
    }

    toggle(id)
    {
        const todo = this.todos.find((todo) => todo.id === id);
        if (todo)
        {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    remove(id)
    {
        const index = this.todos.findIndex((todo) => todo.id === id);
        if (index >= 0)
        {
            this.todos.splice(index, 1);
        }
    }
}

