export class ToDoModel {
    constructor() {
        this.ids = 1;
        this.todos = [];
    }

    getTodo(id){
        return this.todos.find((t) => t.id === id);
    }

    add(description) {
        this.todos.push({
            id: this.ids++,
            description,
            isCompleted: false,
        });
    }

    remove(id) {
        const todo = this.todos.findIndex((t) => t.id === id);
        if (todo >= 0) {
          this.todos.splice(todo, 1);
        }
    }
}   
