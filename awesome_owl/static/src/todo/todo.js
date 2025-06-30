export class Todo {
    static nextId = 1;

    constructor(description) {
        this.id = Todo.nextId;
        Todo.nextId++;
        this.description = description;
        this.isCompleted = false;
    }

    toggle() {
        this.isCompleted = !this.isCompleted;
    }
}
