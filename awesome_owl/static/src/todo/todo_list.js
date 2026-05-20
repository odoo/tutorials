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
}
