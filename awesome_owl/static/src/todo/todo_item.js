import { Component, useState, useRef, onMounted } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: { type: Number },
                description: { type: String },
                isCompleted: { type: Boolean }
            }
        }
    }
    setup() {
        this.inputRef = useRef('id')
        onMounted(() => {
            this.inputRef.el.focus();
        })
    }
    toggleCheck() {
        this.inputRef.el.classList.add("text-decoration-line-through");
    }
}
