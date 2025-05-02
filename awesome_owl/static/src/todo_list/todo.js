export class Todo {
    static nextId = 1;

    constructor(description) {
        this.id = Todo.nextId++;
        this.description = description;
        this.isCompleted = false;
    }

    toggleState() {
        this.isCompleted = !this.isCompleted
    }
}
