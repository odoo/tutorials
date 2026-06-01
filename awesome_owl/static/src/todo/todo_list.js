import {Component, useState, useRef, onMounted, useAutofocus} from "@odoo/owl";
import { TodoItem } from "@awesome_owl/todo/todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = {TodoItem};

    setup(){
        this.nextID = 1;
        this.state = useState({todos:[]});
        this.myRef = useRef('inputTaskBox');
        
        onMounted(() => {
            console.log(this.myRef.el);
            this.myRef.el.focus;
        })
        

    }

    addTodo(ev){
        if (ev.keyCode === 13) {

            const inputElement = ev.target;
            const descriptionText = inputElement.value.trim();

            if (descriptionText){
                this.state.todos.push({
                    id: this.nextID,
                    description: descriptionText,
                    active: true,
                    onToggle: this.toggleActive,
                })
                this.nextID++;
                inputElement.value = "";
            }
        }
    }

    toggleActive(){
        this.state.todos.active = !this.state.todos.active;
        console.log("Changing active!");
    }

}
