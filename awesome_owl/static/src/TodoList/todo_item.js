import {Component} from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        toggleState: { type: Function },
        removeTodo: { type: Function },
        todo: {
            type: Object, shape: { id: Number, description: String, isCompleted: Boolean }
        }
    }

}
