import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";

    static components = { TodoItem };

    setup() {
        this.todos = useState([])
    }

    addTodo(ev) {
        if (ev.keyCode == '13') {
            console.log(ev.target.value)
            if (ev.target.value != ""){
                this.todos.push({
                    id: this.todos.length + 1,
                    description: ev.target.value,
                    isCompleted: false
                })
                ev.target.value = ''
            }
        }
    }
}
