import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        todo: {
            type: Object,
            shape: {
                id : Number,
                description : String,
                isCompleted : Boolean,
            },
        },
        toggleState: {
            type: Function,
            optional: true,
        },
        removeTodo: {
            type: Function,
            optional: true,
        }
    };
    
    onToggleState() {
        this.props.toggleState?.(this.props.todo.id);
    }

    onDeleteTodo() {
        this.props.removeTodo?.(this.props.todo.id);
    }
}

