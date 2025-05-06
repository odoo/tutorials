export class Todo {
    static id = 1;

    constructor(description, index) {
        this.id = Todo.id++;
        this.index = index;
        this.description = description;
        this.isCompleted = false;
    }

    toggleState() {
        this.isCompleted = !this.isCompleted;
    }
}
