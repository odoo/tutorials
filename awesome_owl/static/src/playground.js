/** @odoo-module **/

import { Component,markup, useState,useRef,onMounted } from "@odoo/owl";


export class Counter extends Component{
    setup(){
        this.state=useState({value:1});
        }
    increment(){
        this.state.value++;
        if (this.props.onChange){
            this.props.onChange();
        }
    }

    static props=["onChange?"]
    static template = "awesome_owl.counter";
}

export class Card extends Component{
    setup(){
        this.state=useState({open:true});
    }
    toggle(){
        this.state.open=!this.state.open
        console.log(this.state.open)
        console.log("TOGGLED")

    }
static template = "awesome_owl.card"
static props = ['title','slots?']
}


export class TodoItem extends Component{
    static template = "awesome_owl.TodoItem"
    static props=['todo', "onChange?","removeTodo?"]
    setup(){
      
    }
    checked(event){
    if(this.props.onChange){
        console.log(this.props.todo)
        this.props.onChange(event.target.id);
    }
    }
    removeTodo(event){
        console.log("removed function called")
        console.log(this.props.removeTodo)
        console.log(event.target)
       if (this.props.removeTodo){
        console.log(event.target.id)
        this.props.removeTodo(event.target.id)
       }
    }
}

export class TodoList extends Component{
    static template = "awesome_owl.TodoList";
    unique_id=0
    setup() {
        this.state = useState([]);
        this.inputRef = useRef("input");
        this.removeTodo = this.removeTodo.bind(this)
        onMounted(() => {
            if (this.inputRef.el) {
                this.inputRef.el.focus();
            }
            else{
                console.log("No Element found!!")
            }
        });
    }
        static components = {TodoItem}
    addTodo(event){
        if (event.keyCode===13){
            this.state.push({id:this.unique_id,description:event.target.value,isCompleted:false})
            this.unique_id++
            event.target.value=""
            console.log("Added vals")

        }
    
    }
    toggleState(todoId){
        console.log("This is checked!")
        console.log(todoId)
        const todo = this.state.find(todo => todo.id == todoId);
        console.log(todo)
        if (todo) {
            todo.isCompleted = !todo.isCompleted
    }

}
    removeTodo(todoId){
        console.log("THIS FUNCTION IS CALLED!!!")
        const todoIndex = this.state.findIndex(todo => todo.id == todoId);
        console.log("Todo index:", todoIndex);  // Log the index to verify
    
        if (todoIndex !== -1) {
            // Remove the todo from the state array using `splice`
            this.state.splice(todoIndex, 1);
            console.log("Todo removed:", this.state);
        } else {
            console.error("Todo not found with id:", todoId);
        }
    }
    }
    


export class Playground extends Component {
    static template = "awesome_owl.playground";;
    text1="<div class='text-primary'> some content</div>";
    text2 = markup("<div class='text-primary'> some content</div>");
    setup(){ this.state=useState({sum:2});}
   
    incrementSum(CounterValue){
        this.state.sum++;

    }
    static components={Counter,Card,TodoItem,TodoList}
    }



