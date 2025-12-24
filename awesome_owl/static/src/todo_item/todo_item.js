import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        id: Number,
        text: String,
        isCompleted: Boolean,
        onToggle: { type: Function, optional: true },
        onRemove: { type: Function, optional: true },
    };

    toggleCompletion() {
        console.log("Toggling completion for todo id:", this.props.id);
        if (this.props.onToggle) {
            console.log("Calling onToggle for todo id:", this.props.id);
            this.props.onToggle(this.props.id);
        }
    }
    removeItem(){
        if (this.props.onRemove) {
            this.props.onRemove(this.props.id);
        }
    }
}