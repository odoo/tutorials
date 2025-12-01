
import { Component, useState , useRef,onMounted} from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../../utils";
export class TodoList extends Component {
  static template = "awesome_owl.todo_list";
  static components = { TodoItem };
  setup() {
    this.todos = useState([]);
    this.nextId = 1;
    this.inputRef = useAutofocus("inputRef");
  }
  
  addTodo(e) {
    if (e.key !== "Enter") {
      return;
    }
    const description = e.target.value.trim();
    if (!description) {
      return;
    }
    this.todos.push({
      id: this.nextId++,
      description,
      isCompleted: false,
    })
    e.target.value = "";
  }
  
  toggleState = (todoId) => {
    const todo = this.todos.find((t) => t.id === todoId);
    if (todo) {
      todo.isCompleted = !todo.isCompleted;
    }
  };
  removeTodoItem = (todoId) => {
    const index = this.todos.findIndex((t) => t.id === todoId);
    if (index >= 0) {
      this.todos.splice(index, 1)
    }
  };
}
