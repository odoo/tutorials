import { Component , useState , useRef , onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

function useAutoFocus(refName){
   let inputRef = useRef(refName);
   onMounted(()=>{
     inputRef.el.focus()
   })
}

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    static components = { TodoItem }

    setup(){
      this.todos = useState([]);
      this.idCount = 1;

      useAutoFocus('todo_input');
    }

    addTodo(e){
        const value = e.target.value;
        if(value){
            if(e.key === "Enter"){
             
               this.todos.unshift({
                    id:this.idCount++,
                    description:value,
                    isCompleted:false
               });

               e.target.value = ""
            }
        }

    }

    removeItem(id){
        const itmIndex = this.todos.findIndex( itm => itm.id == id);
        if(itmIndex+1){
            this.todos.splice(itmIndex,1);
        }
    }

    toggleState(id){
        const item = this.todos.find( x => x.id == id);
        if(item){
            item.isCompleted = !item.isCompleted;
        }
    }
}
