import { Component, useState, useRef } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        todo: Object,
        onDelete: { type: Function, optional: true },
        toggleState: Function,
    };

    setup() {
        this.isEditable = useState({value: false})
        this.inputRef = useRef("input")
    }
 

    deleteTodo() {
        this.props.onDelete(this.props.todo.id);
    }

    toggle() {
        this.props.toggleState(this.props.todo.id);
    }

    toggleEdit() {
        this.isEditable.value = true
    }

    addEditTodo() {
        const value = this.inputRef.el.value;

        this.props.todo.description = value;
        this.isEditable.value = false;
        
    }
}
