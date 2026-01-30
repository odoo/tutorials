/** @odoo-module **/
import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static props = {};
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
//        this.state = useState({
//            todos: [
//                { id: 1, description: "buy milk", isCompleted: false },
//                { id: 2, description: "write report", isCompleted: true },
//                { id: 3, description: "call friend", isCompleted: false },
//            ]
//        });
         this.state = useState({
                    todos: [],
                    nextId: 1,
                });
         this.inputRef = useRef("input");
         onMounted(() => {
            this.inputRef.el.focus();
        });

        }
         addTodo(ev) {
                if (ev.keyCode === 13) {
                    const value = ev.target.value.trim();
                    if (!value) {
                        return;
                    }
                    this.state.todos.push({
                        id: this.state.nextId++,
                        description: value,
                        isCompleted: false,
                    });
                    ev.target.value = "";
                }
         }

         toggleTodo(id) {
                const todo = this.state.todos.find(t => t.id === id);
                if (todo) {
                    todo.isCompleted = !todo.isCompleted;
                }
         }

         removeTodo(id) {
                const index = this.state.todos.findIndex(t => t.id === id);
                if (index >= 0) {
                    this.state.todos.splice(index, 1);
                }
}
}
