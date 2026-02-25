import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        id: Number,
        description: String,
        isCompleted: Boolean,
        switchIsCompleted: Function,
        deleteTodo: Function,
    }

    onChange() {
        this.props.switchIsCompleted(this.props.id);
    }

    onDelete() {
        console.log("delete", this.props.id)
        this.props.deleteTodo(this.props.id);
    }
    
}