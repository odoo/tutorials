import { Component } from "@odoo/owl";
import { Todo } from "@awesome_owl/todo_list/todo_model";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: Todo,
    };
}
