import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";

    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                title: String,
                isCompleted: Boolean,
            }
        },
        toggleTodo: Function, 
        deleteTodo: Function
    };

    onToggle() {
        this.props.toggleTodo(this.props.todo.id);
    }

    onDelete() {
        this.props.deleteTodo(this.props.todo.id);
    }

}
