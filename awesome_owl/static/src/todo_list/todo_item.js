import { Component } from "@odoo/owl"

export class TodoItem extends Component{
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: {
            type: Object,
            shape: { id: Number, description: String, isCompleted: Boolean }
        },
        toggleTodo: { type: Function },
        removeTodo: { type: Function },
    };

    onChange(){
        this.props.toggleTodo(this.props.todo.id);
    }

    onDelete(){
        this.props.removeTodo(this.props.todo.id);
    }
}
