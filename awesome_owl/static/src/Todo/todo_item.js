/** @odoo-module **/
import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        slots:Object,  
        todo: {
            type: Object,
            shape: {
                id: Number, 
                description: String, 
                isCompleted: Boolean
            },
        },
        toggleTodoState: Function,
        removeTodo: Function,
    };

    toggleTodo(){
        this.props.toggleTodoState(this.props.todo.id)
    }
    deleteTodo() {
        this.props.removeTodo(this.props.todo.id);
    }
}
