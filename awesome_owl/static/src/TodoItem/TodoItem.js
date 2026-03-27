import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";

    static props = {
        todo: { type: Object, 
                shape: { id: Number, description: String, isComplete: Boolean } 
            },
        toggleState: { type: Function, optional: true },
        remove: { type: Function, optional: true },
    };

    onChange() {
        if (this.props.toggleState) {
            this.props.toggleState(this.props.todo.id);
        }
    }

    onRemove() {
        if (this.props.remove) {
            this.props.remove(this.props.todo.id);
        }
    }
}
