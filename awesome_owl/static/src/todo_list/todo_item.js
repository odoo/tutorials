import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo :{
            id : Number,
            description: String,
            isCompleted: Boolean
        },
        toggleTodo : Function,
        removeTodo : Function
    }
    setup() {
        
    }

    toggleTodo() {
        this.props.toggleTodo(this.props.todo.id);
    }

    removeTodo() {
        this.props.removeTodo(this.props.todo.id);
    }
}
