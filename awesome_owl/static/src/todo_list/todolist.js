import { Component,useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";


export class TodoList extends Component {

    static template = "awesome_owl.todolist";
    static components = {TodoItem};

    setup() {

        this.todos = useState(
            [
                { id: 3 , description: "buy milk", isCompleted: false },
                { id: 4 , description: "buy tea", isCompleted: true },
            ]);
    }
}

