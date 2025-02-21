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
static template = "awesome_owl.card"
static props = ['title','text']
}


export class TodoItem extends Component{
    static template = "awesome_owl.TodoItem"
    static props=['todo']
    
    }

export class TodoList extends Component{
    static template = "awesome_owl.TodoList";
    unique_id=0
    setup() {
        this.state = useState([]);
        this.inputRef = useRef("input");

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

        }
    toggleState()
    {
        this.state.isCompleted=true;
    
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



