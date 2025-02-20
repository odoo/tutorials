import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: {
            type: Object,
            optional: true,
        },
        toggleTodo : Function,
        removeTodo : Function
    };

    onChange() {
        this.props.toggleTodo(this.props.todo.id);
    }
    
    onRemove() {
        this.props.removeTodo(this.props.todo.id)
    }
    
}
