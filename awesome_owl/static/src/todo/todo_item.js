import { Component, markup, useState } from "@odoo/owl";
import { Card } from "../card/card"

export class TodoItem extends Component {
    static props = {
        todo: {
            type: Object, 
            shape: {
                id: {type: Number},
                description: {type: String},
                isCompleted: {type: Boolean},
            }
        },
        toggleState: {type: Function},
        handleDeleteTodo: {type: Function},
    };

    static components = {
        Card,
    };

    static template = "awesome_owl.todo_item";

    onToggleChange = () => {
        this.props.toggleState(this.props.todo.id);
    }

    onDelete = () => {
        this.props.handleDeleteTodo(this.props.todo.id);
    }
}
