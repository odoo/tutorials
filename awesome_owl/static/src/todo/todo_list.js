/** @odoo-module **/

import { Component, useState, onMounted, useRef } from "@odoo/owl";
import { Todoitem } from "./todo_item";
export class Todolist extends Component {
    static template = "awesome_owl.todolist";
    static props ={
        
    }
    setup() {
        this.inputRef = useRef('input');
        onMounted(() => {
            this.inputRef.el.focus()
        });
    this.todo= useState([{
        id:1,
        name:"ch1-owl",
        isCompleted: false 
    },
    {
        id:2,
        name:"ch2-owl",
        isCompleted: false 
    },
    {
        id:3,
        name:"estate",
        isCompleted: true 
    }])
    }
   
    addtodo = (e) => {
        if(e.key=="Enter" && e.target.value){
                this.todo.push({
                    id: this.todo.length +2,
                    name: e.target.value,
                    isCompleted: false 

                })
                e.target.value=""
        
        }
    }

    delete=(e)=>{        
        const index = this.todo.findIndex((todo) => todo.id === e.id);
        if (index >= 0) {
              this.todo.splice(index, 1);
        }    
    }

   static components = {Todoitem}
    
}
