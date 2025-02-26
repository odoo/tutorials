import { Component } from "@odoo/owl";
import { ToDoModel } from "./todomodel";

export class ToDoItem extends Component {
    static template = "awesome_owl.ToDoItem";
    static props = {
        model: ToDoModel,
        id: Number,
    }
}
