import { Component,useState, useRef, onMounted } from "@odoo/owl";
import { ToDoItem } from "../todoitem/todoitem";
import { useAutofocus } from '../utils.js';


export class ToDoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { ToDoItem };

    setup (){
        this.todos = useState({todos_list:[], current_input: ""});
        useAutofocus('focus')
        // alternative way
        // this.focusRef = useRef('focus');
        // onMounted(() => {
        //     this.focus.el.focus()
        // })
    }

    addTodo (ev){
        if (ev.keyCode === 13 && this.todos.current_input){
            this.todos.todos_list.push({ description: this.todos.current_input , isCompleted: false})
            this.todos.current_input = ''
        }
    }

}
