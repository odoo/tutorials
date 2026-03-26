import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        todo: { 
            type: Object,
            shape: { 
                id: {type: Number, optional: false},
                description: {type: String, optional: false}, 
                isCompleted: {type: Boolean, optional: false}, 
            },
        },
    };


}
