import { Component, useState, onMounted, useRef} from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component{
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup(){
        this.state = useState({ todos : [] });
        this.nextID = 1;
        this.inputref = useRef("add-input");
        onMounted(() =>{
            if(this.inputref.el){
                this.inputref.el.focus();
            }
        });
    }
    removeTodo(todoId){
        const index = this.state.todos.findIndex((todo) => todo.id === todoId);
        if(index >= 0){
            this.state.todos.splice(index, 1);
        }
    }
    addTodo(ev){
        if(ev.keyCode === 13 ){
            const text = ev.target.value.trim();
            if(text.length >0){
                const newTodo = {
                    id: this.nextID++,
                    description: text,
                    isCompleted: false
                };
                this.state.todos.push(newTodo);
                ev.target.value = "";
            }
        }
    }
}
