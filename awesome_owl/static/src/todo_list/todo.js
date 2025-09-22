export class Todo {
    constructor(id, description) {
        this.id = id;
        this.description = description;
        this.isCompleted = false;
    }

    setIsCompleted(isCompleted) {
        this.isCompleted = isCompleted;
    }
}
