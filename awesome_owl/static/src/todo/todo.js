import { Component, useState } from "@odoo/owl";

export class TodoList extends Component {
    static template = awesome_owl.todolist_template
    setup(){
        this.todos = useState([
            { id: 1, description: "buy milk", isCompleted: true },
            { id: 2, description: "buy cake", isCompleted: false },
            { id: 3, description: "buy coldrike", isCompleted: false }
        ]);
    }
}

export class TodoItem extends Component {
    static template = awesome_owl.todo_template
    static props = {
        todo: 
        {type: Object,
        shape: {
            id: Number,
            description: String,
            isCompleted: Boolean,
        },
        required: true}
    }
}
