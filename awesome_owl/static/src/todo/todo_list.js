import { Component, useState, useRef, useEffect } from "@odoo/owl";
import { TodoItem } from "./todo_item";

function useAutofocus(name) {
    let ref = useRef(name);
    useEffect(
        (el) => el && el.focus(),
        () => [ref.el]
    );
}

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };
    static props = {
        callback: Function,
    };

    setup () {
        this.todos = useState([]);
        this.id = 1;
        useAutofocus("myinput");
    }

    getLength () {
        this.props.callback(this.todos.length);
    }

    newTask(event) {
        if (event.keyCode === 13) {
            const description = event.target.value.trim();
            if (!description) return alert("Empty task, please add a description");
            this.todos.push({
                id: this.id,
                description: description,
                isCompleted: false,
            })
            this.id++;
            event.target.value = "";
            console.log(this.todos.length);
            this.getLength();
        }
    }

    toggleStatus(id) {
        for (let i=0; i<this.todos.length; i++) {
            if (this.todos[i].id === id) {
                console.log("Before check it was: " + this.todos[i].isCompleted);
                if (!this.todos[i].isCompleted) {
                    this.todos[i].isCompleted = true;
                    console.log("After check it was: " + this.todos[i].isCompleted);
                } else {
                    this.todos[i].isCompleted = false;
                    console.log("After check it was: " + this.todos[i].isCompleted);
                }
                break
            }
        }
    }

    deleteTodo(id) {
        const index = this.todos.findIndex((elem) => elem.id === id);
        console.log(index);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
