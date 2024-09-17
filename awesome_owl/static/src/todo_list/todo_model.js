

export class TodoModel {
    constructor() {
        this.todos = [];
        this.nextId = 1;
    }

    getTodo(id) {
        return this.todos.find((todo) => todo.id === id);
    }

    add(description) {
        const todo = {
            id: this.nextId++,
            description,
            isCompleted: false,
        }
        this.todos.push(todo);
    }

    remove(id) {
        const todoIndex = this.todos.findIndex((todo) => todo.id === id);
        if (todoIndex >= 0) {
            this.todos.splice(todoIndex, 1);
        }
    }

    toggle(id) {
        const todo = this.getTodo(id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }
}