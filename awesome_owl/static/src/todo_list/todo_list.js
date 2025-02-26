import { Component, useState } from "@odoo/owl"
import { TodoItem } from "@awesome_owl/todo_item";
import { useAutofocus } from "@awesome_owl/utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem }
    setup() {
        this.id = 0;
        this.todos = useState([]);
        useAutofocus("input");
    }
    addTodo(ev) {
        if (ev.keyCode == 13 && ev.target.value != "") {
            this.todos.push ({
                id : this.id++,
                description : ev.target.value,
                isCompleted : false
            });
            ev.target.value = "";
        }
    }
    toggleTodo(todoId) {
        const todo = this.todos.find((todo) => todo.id === todoId);

        if(todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }
    removeTodo(todoId) {
        const index = this.todos.findIndex((todo) => todo.id === todoId);
        if ( index >= 0 ) {
            this.todos.splice(index, 1);
        }

    }
}
