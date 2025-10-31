/** @odoo-module **/

import { Component, useState, onMounted } from '@odoo/owl'
import { ToDoItem } from './to_do_item'
import { useAutoFocus } from '../utils'

export class ToDoList extends Component {
    static template = "awesome_owl.to_do_list"
    static props = {
        removeTodo: {
            type: Function,
            optional: true
        }
    }
    setup(){
        this.state = useState({value: 1});
        this.todos = useState([]);
        useAutoFocus('task');
        this.deleteToDo = this.deleteToDo.bind(this);
    }

    addToDo(event) {
        if(event.keyCode===13 && event.target.value){
            this.todos.push({id: this.state.value, description: event.target.value, isComplete: false});
            this.state.value++;
            event.target.value = ""
        }
    }

    deleteToDo(id){
        const index = this.todos.findIndex((elem) => elem.id === id)
        if(index >= 0){
            this.todos.splice(index,1)
        }
    }

    static components = { ToDoItem };
}
