import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "TodoItem";
    static props = ["todo","onDelete"];

    setup(){
        this.toggleState = this.toggleState.bind(this);
    }

    toggleState(){
        this.props.todo.isCompleted = !this.props.todo.isCompleted;
    }

    deleteTodo(){
        this.props.onDelete(this.props.todo.id);
    }
}
