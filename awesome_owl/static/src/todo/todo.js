export class Todo {
    id
    description
    isCompleted
    constructor(id, description, isCompleted) {
        this.id = id
        this.description = description;
        this.isCompleted = isCompleted;
    }
}
