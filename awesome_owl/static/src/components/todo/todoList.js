import {Component, useState} from '@odoo/owl';
import { TodoItem } from './todoItem';

export class TodoList extends Component{
    static template = 'awesome_owl.todoList'
    static components = {TodoItem}

    setup(){
        this.todos = useState([
            { id: 3, description: "buy milk", isCompleted: false },
            { id: 4, description: "write tutorial", isCompleted: true}
        ]);
    }

}