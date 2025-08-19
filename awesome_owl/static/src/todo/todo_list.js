import { Component, useState, useRef, onMounted } from "@odoo/owl"
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        // this.todos = useState([
        //     { id: 1, description: " Buy milk", isCompleted: false },
        //     { id: 2, description: " Walk the dog", isCompleted: true },
        //     { id: 3, description: " Finish Odoo project", isCompleted: false },
        // ]);

        this.todos = useState([]);
        this.nextID = 1;
        // this.inputRef = useRef("input");

        // onMounted(() => {
        //     // console.log("onMounted called!!!!");
        //     if(this.inputRef.el){
        //         this.inputRef.el.focus();
        //     }
        // });

        this.inputRef = useAutofocus("input");
    }

    addTodo(ev){
        if(ev.keyCode === 13){
            const description = ev.target.value.trim();

            if(description){
                this.todos.push({id: this.nextID++, description, isCompleted: false});
                ev.target.value = "";
            }
        }
    }

    toggleTodoState(todoID){
        const todo = this.todos.find(t => t.id === todoID)
        if(todo){
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId){
        const index = this.todos.findIndex(t => t.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
