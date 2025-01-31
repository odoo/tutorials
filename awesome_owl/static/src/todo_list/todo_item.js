import { Component, markup, useState } from "@odoo/owl";



export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";

    static props = {
        todo: {
            type: Object,
            shape: { id: Number, description: String, isCompleted: Boolean }
        },
        toggleState: Function,
        removeTodo: Function
    };

    onChange() {
        this.props.toggleState(this.props.todo.id);
    }

    onRemove(){
        this.props.removeTodo(this.props.todo.id)
    }


}
