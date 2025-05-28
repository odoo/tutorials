
import { Component, useState, xml } from "@odoo/owl";

export class TodoItem extends Component {
    static template = xml`
    <div t-att-id="'todo-' + this.todo.value.id" t-att-class="{'text-muted': this.todo.value.isCompleted, 'text-decoration-line-through': this.todo.value.isCompleted}">
        <input type="checkbox" t-att-checked="isCompleted" t-on-change="onChange"/><t t-esc="todo.value.id"/>. <t t-esc="todo.value.description"/>
    </div>`;
    static props = {
        todo : {
            id: { type: Number },
            description: { type: String },
            isCompleted: { type: Boolean }
        },
        toggleState: { type: Function }
    }

    setup() {
        this.todo = useState({ value: this.props.todo })
    }
    
    onChange() {
        this.props.toggleState(this.props.todo.id)
    }
}
