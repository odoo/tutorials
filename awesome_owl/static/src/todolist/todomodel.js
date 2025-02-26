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
  
    remove() {
        this._model.remove(this.id);
    }
}

export class ToDoModel {
    constructor() {
        this.todos = [];
    }

    add(description) {
        const todo = new Todo(this, description);
        this.todos.push(todo);
    }

    remove(id) {
        const todo = this.todos.findIndex((t) => t.id === id);
        if (todo >= 0) {
          this.todos.splice(todo, 1);
        }
    }
}   
