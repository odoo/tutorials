import { Component , useState} from '@odoo/owl';
import { TodoItem } from './todo_item';
import { useAutofocus } from "./utils";


export class TodoList extends Component {
    static template = 'awesome_owl.TodoList';
    static components = { TodoItem };
    setup(){
        this.todoID = 1;
        this.todos = useState([]);
        useAutofocus("input")
    }
    addTodo(ev){
        if (ev.keyCode === 13 && ev.target.value.trim() !== ""){
            this.todos.push({
                id: this.todoID++,
                description: ev.target.value,
                isCompleted: false
            });
            ev.target.value = "";
        }
    }
}
