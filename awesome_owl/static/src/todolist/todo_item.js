import { Component } from '@odoo/owl';

export class TodoItem extends Component {
    static template = 'awesome_owl.TodoItem';
    static props = { 
        todo: {
            type: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            }, 
            optional: false,
        },
        toggleTodo: {
            type: Function,
            optional: false,
        },
    };
}