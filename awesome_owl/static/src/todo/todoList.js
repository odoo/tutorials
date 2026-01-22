import { Component, useState } from "@odoo/owl";
import { useAutofocus } from "@web/core/utils/hooks";
import { Todo } from "./todo";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { Todo };
    currenId = 0;

    setup() {
        this.todoAddInputRef = useAutofocus({
            refName: "todoAddInputRef"
        });

        this.state = useState({
            todos: [],
        });
    };

    addTodo(event) {
        if (event.keyCode === 13 && event.target.value !== "") {
            this.currentId++;
            this.state.todos.push({ description: event.target.value, id: this.currenId, isCompleted: false });
            event.target.value = "";
        };
    };

    toggleCompletionState(todoId) {
        const todo = this.state.todos.find((todo) => todo.id == todoId);
        const initialState = todo.isCompleted;

        todo.isCompleted = !initialState;
    };

    removeTodo(todoId) {
        this.state.todos = this.state.todos.filter((todo) => todo.id != todoId);
    };
};
