/** @odoo-module **/

import {Component, useState} from "@odoo/owl";

export class ToDoItem extends Component {
    static template = "awesome_owl.todoitem";
    static props = {
        todo: {
            type: Object,
            shape: {id: Number, description: String, isCompleted: Boolean}
        },
        toggleState : {
            type: Function
        },
        removeTodo : {
            type: Function
        }
    };

    onRemove() {
        this.props.removeTodo(this.props.todo.id);
    }

}
