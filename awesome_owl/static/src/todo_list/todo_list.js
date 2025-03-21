import { Component, useState } from "@odoo/owl";
import { TodoItem } from "@awesome_owl/todo_list/todo_item";
import { useAutofocus } from "@awesome_owl/utils";
import { TodoModel } from "@awesome_owl/todo_list/todo_model";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.model = useState(new TodoModel());
        useAutofocus("input");
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value != "") {
            this.model.add(ev.target.value);
            ev.target.value = "";
        }
    }
}
