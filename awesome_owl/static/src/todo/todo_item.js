/** @odoo-module **/

import { Component, xml } from "@odoo/owl";

export class TodoItem extends Component {
    static props = {
        todo: {
            type: Object
        },
        toggleState: {
            type: Function
        },
        remove: {
            type: Function
        }
    };

    static template = xml`
        <tr t-att-class="{'text-muted text-decoration-line-through': props.todo.isCompleted}">
            <td><input type="checkbox" t-att-checked="props.todo.isCompleted" t-on-change="toggleState" /></td>
            <td><t t-out="props.todo.id + 1" /></td>
            <td><t t-out="props.todo.description" /></td>
            <td><span class="fa fa-remove" t-on-click="remove" /></td>
        </tr>
    `;

    toggleState() {
        this.props.toggleState(this.props.todo.id);
    }

    remove() {
        this.props.remove(this.props.todo.id);
    }
}
