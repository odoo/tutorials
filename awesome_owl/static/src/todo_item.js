/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        todo : {type : Object, 
                shape: {
                    id: Number,
                    description: String,
                    isCompleted: Boolean }},
        removeTodo : Function
    };

    setup() {
        this.state = useState({ value: this.props.todo.isCompleted });
    }

    toggleState() {
        this.props.todo.isCompleted = !this.props.todo.isCompleted;
    }
}
