import { Component, useState } from "@odoo/owl";


export class TodoItem extends Component {
    static template = "todo_item.todo_item";
    static props = {
        "todo": JSON,
        "clickOnCheckBox": Function,
        "clickOnCross": Function,
        "id": Number
    }
}
