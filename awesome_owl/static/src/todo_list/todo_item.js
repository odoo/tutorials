import { Component, useState } from "@odoo/owl";


export class ToDoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        todo: {
            id: Number,
            description: String,
            isCompleted: Boolean,
        },
        onChange: { type: Function, optional: true },
        removeTodo: { type: Function, optional: true },
    };
}
