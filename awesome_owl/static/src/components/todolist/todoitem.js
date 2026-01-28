import { Component, useState } from "@odoo/owl";


export class Todoitem extends Component {
    static template = "my_module.Todoitem";
    static props = {
        id: {type: Number, required: true},
        description: {type: String, required: true},
        isCompleted: {type: Boolean, optional: true, default: false},
        toggleState: {type: Function, optional: true},
        removeTodo: {type: Function, optional: true}
        };

    setup() {
        this.todo = useState({
            id: this.props.id,
            description: this.props.description,
            isCompleted: this.props.isCompleted,
        });
    }
    toggleState(ev) {
        this.todo.isCompleted = ev.target.checked;
        this.props.toggleState?.(this.todo.id, this.todo.isCompleted);
    }
    removeTodo() {
        console.log("Removing todo", this.todo.id);
        this.props.removeTodo?.(this.todo.id);
    }
}
