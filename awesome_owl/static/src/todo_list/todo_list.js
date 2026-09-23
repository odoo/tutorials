import {Component, useState} from "@odoo/owl"
import { TodoItem } from "../todo_item/todo_item";


const ENTER_KEY = 13;

export class TodoList extends Component {
    static template = 'awesome_owl.todo_list';
    static components = { TodoItem };



    setup(){
        this.todos = useState([]);
        this.idCount = 0;
        this.userInput = useState({text: ""});
    }

    addTodo(event){
        if(event.keyCode === ENTER_KEY){
            if(this.userInput.text.length > 0) {
                this.todos.push(
                    {
                        id: this.idCount,
                        description: this.userInput.text,
                    }
                );
                this.idCount++;
                this.clearUserInput();
            }
        }
    }

    clearUserInput(){
        this.userInput.text = '';
    }

}
