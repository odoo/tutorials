import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
                isEditing: Boolean,
                editText: String,
            }
        },
        toggleState: Function,
        deleteTodo: Function,
        editTodo: Function,
        saveTodo: Function,
        updateEditText: Function,
    };
}
