export class Todo {
    static id = 1;

    constructor(description) {
        this.id = Todo.id++;
        this.description = description;
        this.isCompleted = false;
    }
    toggleState() {
        this.isCompleted = !this.isCompleted;
    }
}
