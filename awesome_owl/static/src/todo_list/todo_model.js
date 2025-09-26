export class Todo {
    static nextId = 1;

    constructor(model, description) {
        this._model = model;
        this.id = Todo.nextId++;
        this.description = description;
        this.isCompleted = false;
    }

    toggle() {
        this.isCompleted = !this.isCompleted;
    }

    delete() {
        this._model.delete(this.id);
    }
}

export class TodoModel {
    constructor() {
        this.todoList = [];
    }

    add(description) {
        this.todoList.push(new Todo(this, description));
    }

    delete(id) {
        const index = this.todoList.findIndex((todo) => todo.id === id);
        if (index == -1) return;
        this.todoList.splice(index, 1);
    }
}
