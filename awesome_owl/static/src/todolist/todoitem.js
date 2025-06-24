import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "my_module.TodoItem";

    static props = {
        todo: { type: Object,
            shape: {
                id: { type: Number, default: 0 },
                description: { type: String, default: "" },
                isCompleted: { type: Boolean, default: false },
            }
        },
        toggleState: { type: Function, optional: true },
        removeTodo: { type: Function, optional: true },
        
    }
    
    onChange() {
        this.props.toggleState(this.props.todo.id);
    }

    onRemove() {
        this.props.removeTodo(this.props.todo.id);
    }
    
    

}