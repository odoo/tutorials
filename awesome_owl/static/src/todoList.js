import {Component,useState,useRef,onMounted} from "@odoo/owl";
import { TodoItem  } from "./todoItem";

export class TodoList extends Component {

    static template = "awesome_owl.TodoList";
    static components = {TodoItem};
    setup(){
        this.todos = useState([]);
        this.inputRef= useRef("myInput");
        this.nextId=1;
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
}