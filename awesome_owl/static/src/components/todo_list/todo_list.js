import { Component, useState, useRef, onMounted} from "@odoo/owl"
import { TodoItem } from "./todo_item"
import { useAutoFocus } from "../../lib/utils";

export class TodoList extends Component {
    static template = "awsome_owl.todo_list";
    static components = { TodoItem };

    setup(){
        this.todos = useState([])
        this.state = useState({nextId:1})
        this.inputRef = useAutoFocus("add-input");
    }

    addTodo(e){
        if(e.keyCode === 13){
            const todoDesc = e.target.value.trim();
            e.target.value = "";
            if(todoDesc){
                const newTodo = {
                    id: this.state.nextId++,
                    description: todoDesc,
                    isCompleted: false
                }
                this.todos.push(newTodo);
            }
        }
    }

    deleteTodo(id){
        const index = this.todos.findIndex(t=>t.id == id)
        
        if(index>=0){
            this.todos.splice(index,1)
        }
    }


    toggleTodoState(id) {
    const todo = this.todos.find(t => t.id == id);
    if (todo) {
        todo.isCompleted = !todo.isCompleted;
    }
}

}
