import { Component, useState } from "@odoo/owl";
import { TodoItem } from "../todoItem/todoItem";

export class TodoList extends Component {
    static template = "awesome_owl.todoList";
    static components = { TodoItem };
    static props = { model: Object }
}
