/** @odoo-module **/

import { Component, xml } from "@odoo/owl";

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
    }

    static template = xml`
    <p>
    <t t-out="props.todo.id"/><span>. </span>
    <t t-out="props.todo.description"/><s> </s>
    <t t-out="props.todo.isCompleted"/>
    </p>
    `;

    // &emsp; &ensp;

}
