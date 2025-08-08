import {Component,useState,useRef,onMounted} from "@odoo/owl";
import { TodoItem  } from "./todoItem";

export class TodoList extends Component {

    static template = "awesome_owl.TodoList";
    static components = {TodoItem};
    setup(){
        this.todos = useState([]);
        this.inputRef= useRef("myInput");
        this.nextId=1;
        this.changed_checkbox=this.changed_checkbox.bind(this);
        this.removeTodo=this.removeTodo.bind(this);
        onMounted(()=>{
            this.inputRef.el.focus();
        }); 
    }
    addTask(ev){
        if(ev.keyCode === 13){
            const input= ev.target;
            const description= input.value.trim();
            
            if(description){
                this.todos.push({
                    id : this.nextId++,
                    description : description,
                    isCompleted: false,
                });
                input.value="";
            }

        }
    }

    changed_checkbox(id){
        const curr_todo_item= this.todos.find(
            curr_todo_item => curr_todo_item.id === id
        );
        if(curr_todo_item){
            curr_todo_item.isCompleted = !curr_todo_item.isCompleted;
        }
    }

    removeTodo(id){
        const curr_todo_item=this.todos.find(
            curr_todo_item => curr_todo_item.id === id
        );
        this.todos.splice(curr_todo_item,1);
    }
}