import { Component, useState } from "@odoo/owl"

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";

    static props = {
        todo : {
            id: Number,
            description: String,
            isCompleted: Boolean },
        onClick : { Type: Function, optional : true }
    };

    toggleState() {
        this.props.todo.isCompleted = !this.props.todo.isCompleted;
    }

    removeTodo() {
        this.props.onClick(this.props.todo.id);
    }
}