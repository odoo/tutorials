import { Component } from "@odoo/owl";

export class TodoItem extends Component{
    static template = "awesome_owl.TodoItem"

    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            },
        },
        onChange: {
            type: Function,
        },
        onRemove: {
            type: Function,
        },
    }

    change(){
        this.props.onChange();
    }

    remove(){
        this.props.onRemove();
    }
};