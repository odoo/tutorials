import {Component} from "@odoo/owl";
import {Todo} from "./todo_model";


export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        model: { type: Todo },
        toggle: { type: Function },
        removeTodo: { type: Function },
    };
}
