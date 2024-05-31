/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {TodoItem};

    setup(){
        this.todo = useState([{ id: 3, description: "buy milk2", isComplete: false },
        { id: 2, description: "buy milk2", isComplete: true },
        { id: 1, description: "buy milk1", isComplete: false }]);
    }

}
