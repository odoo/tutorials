import { Component, onMounted, useRef, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    static components = { 
        TodoItem,
    };

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        // t-ref="input"  ←→  useRef("input") . Naming our JavaScript variable: this.inputRef. Ref suffix is just a naming convention.
        // useRef() gives reference object, not directly the HTML element. el means element. this.inputRef = Owl's reference object and this.inputRef.el = actual HTML <input> element.
        // Why onMounted() ? Because setup() happens before the component is mounted.
        // Component created -> setup() -> render -> mounted -> HTML element exists in DOM
        // When setup() runs, the actual <input> element hasn't been mounted into the DOM yet. So, this.inputRef.el is not available yet. After the component has been mounted, get the actual input element and focus it.
        this.inputRef = useRef("input");
        onMounted(() => {
            this.inputRef.el.focus();
        });
    }

    addTodo(ev) {
        if(ev.keyCode === 13 && ev.target.value.trim()){
            this.todos.push({
                id: this.nextId++,
                description: ev.target.value,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }

    toggleState(id) {
        const todo = this.todos.find((todo) => todo.id === id);
        todo.isCompleted = !todo.isCompleted;
    }

    removeTodo(id) {
        const index = this.todos.findIndex((todo) => todo.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
