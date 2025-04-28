/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };
    // static props = {
    //     onChange: { type: Function, optional: true }
    // };

    setup() {
        this.todos = useState([{ id: 3, description: "buy milk", isCompleted: false }]);
    }

    // increment() {
    //     this.state.value++;
    //     if (this.props.onChange) this.props.onChange()
    // }
}
