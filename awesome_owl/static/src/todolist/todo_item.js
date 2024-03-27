/** @odoo-module **/

import { Component, useState, xml } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        "todo": {
            type: "Object",
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
                delete: Function
            }
        }
    };
    setup() {
        this.o = useState({
            id: this.props.todo.id,
            description: this.props.todo.description,
            isCompleted: this.props.todo.isCompleted
        });
    }

    toggleTodo(ev) {
        this.o.isCompleted = !this.o.isCompleted;
    }

    deleteTodo() {
        this.props.todo.delete(this.props.todo.id)
    }

    static template = xml`
    <label class="">
        <p class="mt-2 mb-0 d-flex justify-content-between" t-att-class="{'text-muted text-decoration-line-through': o.isCompleted}">
            <span>
                <t t-out="props.todo.id"/><span>. </span>
                <t t-out="props.todo.description"/>
            </span>
            
            <span class="fa fa-remove" t-on-click="deleteTodo"/>
        </p>
        <input type="checkbox" class="d-none" t-on-change="toggleTodo" t-att-checked="o.isCompleted"/>
    </label>
    `;

}
