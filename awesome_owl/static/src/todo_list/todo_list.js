import { Component, useState } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";
import { useAutofocus } from "../util";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    counter = 1;

    static components = {
        TodoItem
    }

    setup() {
        this.todos = useState([]);
        useAutofocus("input");
    }

    change(id) {
        let found = this.todos.findIndex(t => t.id === id);
        if(found >= 0) this.todos[found] = {...this.todos[found], isCompleted: !this.todos[found].isCompleted};
    }

    remove(id) {
        let found = this.todos.findIndex(t => t.id === id);
        if(found >= 0) this.todos.splice(found, 1);
    }

    tryAdd(ev) {
        if(ev.keyCode != 13) return;

        let txt = ev.srcElement.value;
        if(txt === "") return;

        this.todos.push({id: this.counter++, description: txt, isCompleted: false});
        ev.srcElement.value = "";
    }
}
