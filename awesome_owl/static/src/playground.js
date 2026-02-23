import { Component } from "@odoo/owl";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = { TodoList };
}