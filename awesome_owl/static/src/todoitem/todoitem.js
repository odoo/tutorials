import { Component,useState } from "@odoo/owl";

export class ToDoItem extends Component {
    static template = "awesome_owl.todoitem";

    static props = {
        todo : {type: Object, optional: true},
        todo_index : {type: Number, optional: true},
    }

    removeTodo() {
        this.props.todo.splice("props.todo_index", 1);
    }

}
