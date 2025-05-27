
import { Component, useState, xml } from "@odoo/owl";

export class TodoItem extends Component {
    static template = xml`<div t-att-class="{'text-muted': this.todo.value.isCompleted, 'text-decoration-line-through': this.todo.value.isCompleted}">
        <t t-esc="todo.value.id"/>. <t t-esc="todo.value.description"/></div>`;
    static props = {
        todo : {
            id: { type: Number },
            description: { type: String },
            isCompleted: { type: Boolean }
        }
    }

    setup() {
        this.todo = useState({ value: this.props.todo })
    }
}
