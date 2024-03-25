/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {TodoItem};

    setup(){
        this.todos = useState([
            {id: 0, description: "foo", isCompleted: false},
            {id: 1, description: "bar", isCompleted: true},
            {id: 2, description: "baz", isCompleted: false}
        ]);
    }
}
