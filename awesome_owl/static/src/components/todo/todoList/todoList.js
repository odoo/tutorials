import { Component, useState } from '@odoo/owl';
import { TodoItem } from '../todoItem/todoItem';

export class TodoList extends Component {
    static template = "awesome_owl.TodoList"
    static props = {
        todos: {
            type: Array
        }
    }
    static components = { TodoItem }
}
