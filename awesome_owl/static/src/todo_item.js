import { Component } from "@odoo/owl"
import { Todo } from "./todo";

export class TodoItem extends Component {
    static props = {
        todo : Todo,
    }
    static template = "awesome_owl.TodoItem";
}