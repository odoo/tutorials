import { Component } from "@odoo/owl";
import { Todo } from "./todo_model";

// Component for individual todo items
export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: Todo,
    };
}
