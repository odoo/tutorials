import { Component } from "@odoo/owl";


export class TodoItem extends Component {
    static template = "my_module.TodoItem";

    static props = {
        todo: {type: Object, shape: {id: Number, description: String, isCompleted: Boolean}},
        toggleState: {type: Function},
        removeTodo: {type: Function}
    }
}
