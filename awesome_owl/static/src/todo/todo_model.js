export class Todo {
    constructor(id, description, isCompleted) {
        this.id = id;
        this.description = description;
        this.isCompleted = isCompleted;
    }

    toggle() {
        this.isCompleted = !this.isCompleted;
    }
}
