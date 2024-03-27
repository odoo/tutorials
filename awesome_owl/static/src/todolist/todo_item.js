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
                isCompleted: Boolean
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

    static template = xml`
    <label class="pt-3">
        <p  t-att-class="{'text-muted text-decoration-line-through': o.isCompleted}">
            <t t-out="props.todo.id"/><span>. </span>
            <t t-out="props.todo.description"/>
        </p>
        <input type="checkbox" class="d-none" t-on-change="toggleTodo" t-att-checked="o.isCompleted"/>
    </label>
    `;

}
