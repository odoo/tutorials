/** @odoo-module **/

import {useState,Component} from "@odoo/owl"
import { Todo } from "../Todo/Todo";
import { useAutofocus } from "../utils";

export class Todolist extends Component
{
    static template = "owl_playground.Todolist";
    static components = {Todo};
    
    setup()
    {
        this.todol = useState([]);
        this.count =0;
        useAutofocus("todoinput");    
    }   
    addTodo(eh) {
        if (eh.keyCode === 13 && eh.target.value != "") {
            this.todol.push({ id: ++this.count, description: eh.target.value, done: false });
            eh.target.value = "";
        }
        let count =0;
        for(let i of this.todol)
        {
            i.id=++count;
        }
    }
    
    toggleTodo(todoId) {
        const todo = this.todol.find((todo) => todo.id === todoId);
        if (todo) {
            todo.done = !todo.done;
        }
    }
    removetodo(elemId)
    {
        // for(let i of this.todol)
        // {
        //    if(i.id===todoId)
        //    {
        //     this.todol.pop(i);
        //    }
        // }
        const index = this.todol.findIndex((elem) => elem.id === elemId);
        if (index >= 0) {
            // remove the element at index from list
            this.todol.splice(index, 1);
        }
        let count =0;
        for(let i of this.todol)
        {
            i.id=++count;
        }
    }
}