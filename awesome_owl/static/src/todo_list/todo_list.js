import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item/todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    static components = { TodoItem };

    setup() {
        this.state = useState({
            todos: [],
        });
        this.addTodo = this.addTodo.bind(this);
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value.trim() !== "") {
            const newId =
                this.state.todos.length > 0
                    ? Math.max(...this.state.todos.map((todo) => todo.id)) + 1
                    : 1;
            this.state.todos.push({
                id: newId,
                description: ev.target.value,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }
}
