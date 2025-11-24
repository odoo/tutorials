import { Component, useState } from "@odoo/owl";
import TodoItem from "./todo_item";

class TodoList extends Component {
    static template = "awesome_owl.todo_list"
    static components = { TodoItem };
    static props = {}

    setup() {
        this.todos = useState([
            { id: 1, description: "Todo 1", isCompleted: false },
            { id: 2, description: "Todo 2", isCompleted: false },
            { id: 3, description: "Todo 3", isCompleted: true },
        ]);
    }
}

export default TodoList;
