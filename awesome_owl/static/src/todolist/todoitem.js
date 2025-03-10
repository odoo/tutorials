import { Component } from "@odoo/owl";
import { Todo } from "./todomodel";

export class ToDoItem extends Component {
    static template = "awesome_owl.ToDoItem";
    static props = {
        todo: Todo,
    }
}
