import { Component ,useState ,useRef ,onMounted} from "@odoo/owl";
import { TodoItem } from "./todo_item";
export class TodoList extends Component { 
    static template="awesome_owl.TodoList";
    static components = {TodoItem};
    
    setup(){
        this.todos = useState([
            { id: 1, description: "Buy groceries", isCompleted: false }
        ]);
        this.inputRef=useRef('input')
        onMounted(()=>{
            this.inputRef.el.focus();
        })
    }
    addTodo(ev){
        if(ev.keyCode==13){
            const description=ev.target.value;
            if(description){
                this.todos.push({id:this.todos.at(-1).id + 1,description,isCompleted : false})
                ev.target.value="";
            }
        }
    }
}
