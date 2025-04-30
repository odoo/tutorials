import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";

    setup() {
        this.state = useState({
            todos: [],
            idCounter: 0
        });
    };

    addTodo(ev) {
        if (ev.keyCode === 13) {
            this.state.idCounter++
            console.log(this.state.idCounter);
            this.state.todos.push({
                'id': this.state.idCounter, 'description': ev.target.value, 'isCompleted': false
            });
            ev.target.value = "";
        }
    }
}
