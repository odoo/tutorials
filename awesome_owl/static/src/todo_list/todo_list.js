/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item"

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem }

    setup() {
        this.state = useState({
            todos: [
                {
                    id: 3,
                    description: "Buy Milk",
                    isCompleted: true,
                },

                {
                    id: 5,
                    description: "Study",
                    isCompleted: false,
                },
            ],
        })
    }
}
