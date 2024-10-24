export class Todo {
    static nId = 1;

    constructor(todoList, desc, isDone = false) {
        this.todoList = todoList;
        this.id = Todo.nId++;
        this.desc = desc;
        this.isDone = isDone;
    }

    markTodo() {
        console.log("Item " + this.desc + " was " + this.isDone);
        this.isDone = !this.isDone;
        this.todoList.reorder();
    }

    remove() {
        let item = document.getElementById('list_item_' + this.id);
        let line = this.todoList;
        let line_id = this.id;
        item.classList.add('fade-out');
        item.addEventListener('transitionend', function () {
            line.remove(line_id);
        });


    }


}

export class Todos {

    constructor(name = "Todo List") {
        this.name = name;
        this.todos = [];
    }

    add(desc, isDone = false) {
        this.todos.push(new Todo(this, desc, isDone));
    }

    remove(id) {
        const to_remove = this.todos.findIndex((todo) => todo.id === id);
        if (to_remove >= 0) {
            this.todos.splice(to_remove, 1);
        }
    }

    reorder() {
        this.todos.sort((a, b) => {
                if (a.isDone === b.isDone) {
                    return a.id - b.id;
                }
                return a.isDone - b.isDone;
            }
        );
    }

}
