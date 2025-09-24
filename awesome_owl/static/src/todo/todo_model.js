export class Todo {
    constructor(model, id, title) {
        this.id = id;
        this.title = title;
        this.done = false;
        this._model = model;
    }

    toggle() {
        this.done ^= 1;
    }
}

export class TodoList {
    constructor() {
        this.todos = [];
        this._nextId = 1;
    }

    addTodo(title) {
        this.todos.push(new Todo(this, this._nextId++, title));
    }

    removeTodo(index) {
        this.todos.splice(index, 1);
    }
}
