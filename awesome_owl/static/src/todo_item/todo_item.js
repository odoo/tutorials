import { Component, useState } from "@odoo/owl";
import { Card } from "../card/card"

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static components = { Card }
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean
            }
        },
        removeTodo: {
            Function, optional: true
        }
    }

    toggleState(id) {

    }

    removeTodo(id) {
        this.props.removeTodo(id);
    }
}