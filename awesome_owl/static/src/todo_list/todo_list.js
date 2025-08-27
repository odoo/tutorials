import { Component, useState, useRef ,onMounted} from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "./util";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };
    static props = {
        onChangeIncrease: { type: Function, optional: true },
    }
    setup() {
        this.todos = useState({value: []});
        this.counter = useState({ value: 0 });
        this.input = useRef("input");
        onMounted(() => {
            this.input.el.focus();
        })
    }
    toggleState = (todo) => {
        todo.isCompleted = !todo.isCompleted;
    }
    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value != "") {
            const newTodo = {
                id: this.counter.value++, description: ev.target.value, isCompleted: false
            }
            this.todos.value = [...this.todos.value, newTodo]
            ev.target.value = ""
        }
    }
    removeTodo = (id) => {
        this.todos.value = this.todos.value.filter((todo) => todo.id != id);
    }
}
