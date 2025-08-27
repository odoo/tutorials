import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item_template";

    static props = {
        todo: { type: Object, shape: { id: Number, description: String, isCompleted: Boolean } },
        removeTodo: Function
    };

    toggleCompleted(){
        this.props.todo.isCompleted = !this.props.todo.isCompleted; 
    }

    deleteTodo() {
        this.props.removeTodo(this.props.todo.id);
    }
}
