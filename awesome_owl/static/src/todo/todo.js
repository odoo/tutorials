import { Component, useState, useRef } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem_template"
    static props = {
        todo: 
        {type: Object,
        shape: {
            id: Number,
            description: String,
            isCompleted: Boolean,
        },
        required: true},
        toggleState: Function,
        removeTodo: Function,
    }

    toggle() {
        this.props.toggleState(this.props.todo.id);
    }

    removeTodo() {
        this.props.removeTodo(this.props.todo.id);
    }
}

export class TodoList extends Component {
    static template = "awesome_owl.todolist_template"
    static components = { TodoItem }
    setup(){
        this.todos = useState([]);
        this.taskNum = useState({'count':0})
        this.inputRef = useRef("input");
    }

    addTodo(ev){
        if(ev.keyCode === 13 && ev.target.value){
            this.todos.push({id:this.taskNum.count, description:ev.target.value, isCompleted:false});
            this.taskNum.count++;
            ev.target.value="";
        }
    }

    deleteTodo(todoID){
        this.todos.splice(this.todos.findIndex(todo => todo.id === todoID), 1); 
    }

    inputFocus(){
        this.inputRef.el.focus();
    }

    toggleTodo(todoID){
        console.log(this.todos)
        const todo = this.todos.find(todo => todo.id === todoID);
        if (todo)
            todo.isCompleted = !todo.isCompleted;
    }
}
