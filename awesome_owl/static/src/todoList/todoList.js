/** @odoo-module **/

import {Component, useState} from "@odoo/owl";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static props = {};

    next_id = 3;

    setup() {
        this.todos = useState(
            [
                { id: 1, description: "buy milk", isCompleted: false },
                { id: 2, description: "step 2", isCompleted: false }
            ]
        );
    };

    addTodo(desc){
        this.todos.push({id:this.next_id++, description: desc, isCompleted: false});
    };

    deleteTodo(id) {
        this.todos.splice(id, 1);
    };

}