import { Component, useState } from '@odoo/owl'
import { TodoItems } from './todoitems';
import { useAutoFocus } from '../utils/utils';


export class TodoList extends Component {
    static template = "todolist";
    static components = {TodoItems}

    setup() {
        this.todo = useState([])
        this.nextVal = 0
        useAutoFocus("input")
    }

    addTodo(item) {
        if(item.keyCode === 13 && item.target.value != ""){
            this.todo.push({
                id: this.nextVal++,
                description: item.target.value,
                isCompleted: false
            })
            item.target.value = ""
        }
    }

    toggleItem(itemID) {
        const item = this.todo.find((item) => item.id === itemID)
        if(item){
            item.isCompleted = !item.isCompleted
        }
    }

    removeItem(itemID){
        const item = this.todo.find((item) => item.id === itemID)
        if(item){
            this.todo.splice(item, 1);
        }
    }
}
