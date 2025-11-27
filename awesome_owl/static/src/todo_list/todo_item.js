import { Component } from "@odoo/owl";

class TodoItem extends Component {
    static template = "awesome_owl.todo_item"
    static props = {
        item: { optional: true },
        toggleState: { type: Function },
        removeTodo: { type: Function },
    }
}

export default TodoItem;
