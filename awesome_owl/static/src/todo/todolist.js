import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "./todoitem"
import { useAutofocus } from "@awesome_owl/utils"


export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 0;
        this.description_inputRef = useRef("todo_input");
        useAutofocus(this.description_inputRef);
    }

    addTodo(ev) {
        const description = this.description_inputRef.el.value.trim();
        if (ev.keyCode === 13 && description) {
            this.todos.push({ id: this.nextId, description: description, isCompleted: false });
            this.nextId++;
            this.description_inputRef.el.value = "";
        }
    }

    toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex(t => t.id === id);
        if (index >= 0) {
              this.todos.splice(index, 1);
        }
    }
}
