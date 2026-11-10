import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoItem";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            },
        },
        toggleTodo: Function,
        removeTodo: Function
    };


    onToggleState() {
    this.props.toggleTodo(this.props.todo.id);
    }

    onDelete(){
    this.props.removeTodo(this.props.todo.id)
    }
}
