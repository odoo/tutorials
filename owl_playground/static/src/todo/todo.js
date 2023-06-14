/** @odoo-module **/

//
//  Excercise 7.2 is not complated yet (Custom Hook for input focus)
//
import { Component, useState, useRef, onMounted } from "@odoo/owl";

export class Todo extends Component {}

Todo.template = "owl_playground.todo";
Todo.props = {
    id : {type: Number},
    description : {type: String},
    done : {type: Boolean},
    toggleState: {type: Function},
    removeTodo: {type: Function},
};

export class TodoList extends Component {
    setup() {
        this.todo_input = useRef("todo_input");

        onMounted(() => {
            this.todo_input.el.focus();
        });
    }

    toggleState(toDoId) {
        for(const todo of this.props.list) {
            if(todo.id == toDoId) {
                todo.done = todo.done ? false : true;
            }
        }

        //updating the local storage
        localStorage.setItem('todo_list', JSON.stringify(this.props.list));
    }

    removeTodo(toDoId) {
        const index = this.props.list.findIndex((elem) => elem.id === toDoId);
        if (index >= 0) {
            this.props.list.splice(index, 1);
        }

        //updating the local storage
        localStorage.setItem('todo_list', JSON.stringify(this.props.list));
    }

    addTodo(ev) {
        const desc = this.todo_input.el.value;
        if (ev.keyCode === 13 && desc != '') {

            //get values for ToDo
            this.props.count++;

            //push new Todo to in the list
            this.props.list.push({id: this.props.count, description: desc, done: false });

            //clear input
            this.todo_input.el.value = '';

            //updating the local storage
            localStorage.setItem('todo_list', JSON.stringify(this.props.list));
            localStorage.setItem('todo_count', JSON.stringify(this.props.count));
        }
    }
}

TodoList.components = { Todo }
TodoList.template = "owl_playground.todolist";
TodoList.props = {
    list: {
        type: Array,
        element: {type: Object, id : {type: Number}, description : {type: String}, done : {type: Boolean}},
    },
    count: { type: Number},
};