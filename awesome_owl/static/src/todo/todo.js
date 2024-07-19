/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component
{
    static template = "awesome_owl.TodoItem";
    static props = { todo: { type: Object,
                             shape: { id: Number,
                                      description: String,
                                      isCompleted: Boolean } } };
}

export class TodoList extends Component
{
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup()
    {
        this.state = useState([{ id: 3, description: "buy milk", isCompleted: false }]);
    }
}

