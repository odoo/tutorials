import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
  static template = "awesome_owl.Todolist";

  setup() {
    useAutofocus("inputRef");
    this.todoItem = useState([
      {
        id: 1,
        description: "SA",
        isCompleted: true,
      },
      {
        id: 2,
        description: "SA",
        isCompleted: false,
      },
    ]);
  }

  addTodo(e) {
    if (e.keyCode === 13 && e.target.value != "") {
      this.todoItem.push({
        id: this.todoItem.length + 1,
        description: e.target.value,
        isCompleted: false,
      });
      e.target.value = "";
    }
  }
  toggleTodo(id) {
    this.todoItem
      .filter((k) => k.id === id)
      .map((k, v) => {
        k.isCompleted = !k.isCompleted;
      });
  }

  removeTodo(id) {
    const index = this.todoItem.filter((k) => k.id === id);
    if (index !== -1) {
      this.todoItem.splice(index, 1)[0];
    } else {
      console.log("Item not found");
    }
  }
  static components = { TodoItem };
}
