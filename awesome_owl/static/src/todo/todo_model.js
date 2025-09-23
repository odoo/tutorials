export class Todo {
    constructor(model, id, title) {
        this.id = id;
        this.title = title;
        this.done = false;
        this._model = model;
    }

    toggle() {
        this.done = !this.done;
    }

    remove() {
        this._model.removeTodo(this);
    }
}

export class TodoModel {
    constructor() {
        this.todos = [];
        this._nextId = 1;
    }

    addTodo(title) {
        const todo = new Todo(this, this._nextId++, title);
        this.todos.push(todo);
    }

    removeTodo(todo) {
        this.todos = this.todos.filter((t) => t !== todo);
    }
}
