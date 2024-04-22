/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    
    static components = { TodoItem };

    counter = 0;
    todos = useState([]);

    setup() {
        // this.inputRef = useRef("todo-input");
        // onMounted(() => {
        //     this.inputRef.el.focus();
        // });
        useAutofocus('todo-input');
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.srcElement.value) {
            this.todos.push({
                id: this.counter,
                description: ev.srcElement.value,
                isCompleted: false
            });
            ev.srcElement.value = "";
            this.counter++;
        }
    }

    toggleState(_ev, id) {
        for (const todo of this.todos)
            if (todo.id === id)
                todo.isCompleted = !todo.isCompleted
    }

    removeTodo(_ev, id) {
        // find the index of the element to delete
        const index = this.todos.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            // remove the element at index from list
            this.todos.splice(index, 1);
        }
    }
}