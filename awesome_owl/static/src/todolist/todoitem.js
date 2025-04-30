import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "TodoItem";
    static props = ["todo"];
}
