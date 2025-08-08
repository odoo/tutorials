import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
// import { useAutofocus } from "../utils";
// import { TodoModel } from "./todo_model";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([
            { id: 1, description: "buy milk", isCompleted: false },
            { id: 2, description: "do laundry", isCompleted: true },
            { id: 3, description: "write Owl todo list", isCompleted: false },
        ]);
    }

    // setup() {
    //     this.model = useState(new TodoModel());
    //     useAutofocus("input")
    // }
    //
    // addTodo(ev) {
    //     if (ev.keyCode === 13 && ev.target.value != "") {
    //         this.model.add(ev.target.value);
    //         ev.target.value = "";
    //     }
    // }
}