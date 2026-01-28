import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.nextId = 1;
        this.todos = useState([]);
    };

    addTodo(ev) {
        if(ev.keyCode === 13) {
            const taskName = ev.target.value.trim();

            if(taskName !== ""){
                this.todos.push({
                    id: this.nextId++,
                    description: taskName,
                    isCompleted: false,
                });

                ev.target.value = "";
            }
        }
    }
}
