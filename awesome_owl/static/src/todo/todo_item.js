import { Component } from "@odoo/owl";

export class ToDoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        todo_item: { type: Object },
        removeTodo: { type: Function }
    }

    toggleState() {
        this.props.todo_item.isCompleted = !this.props.todo_item.isCompleted;
    }

}
