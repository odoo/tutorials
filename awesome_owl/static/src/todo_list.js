import { Component, useState, xml, useRef, onMounted } from "@odoo/owl";

function useAutoFocus(ref = "autofocus") {
  const inputRef = useRef(ref);

  onMounted(() => {
    inputRef.el.focus();
  });

  return inputRef;
}

export class Todo extends Component {
  static template = xml`
    <li class="o_todo_item d-flex align-items-center gap-2 py-2" t-att-class="props.done ? 'done' : ''">
      <input
        class="o_todo_control form-check-input m-0"
        type="checkbox"
        t-att-checked="props.done"
        t-att-aria-label="'Toggle completion for ' + props.label"
        t-on-change="() => props.markDone(props.id)"
      />
      <span class="flex-grow-1" t-att-class="props.done ? 'text-decoration-line-through text-muted' : ''">
        <t t-esc="props.label" />
      </span>
      <button
        class="o_todo_control btn btn-sm btn-link text-danger p-0"
        type="button"
        t-att-aria-label="'Delete ' + props.label"
        t-on-click="() => props.deleteTodo(props.id)">
        <i class="fa fa-trash" aria-hidden="true" />
      </button>
    </li>
  `;

  static props = {
    id: Number,
    label: String,
    done: Boolean,
    markDone: Function,
    deleteTodo: Function,
  };
}

export class TodoList extends Component {
  static components = { Todo };

  static props = {
    todos: Array,
    markDone: Function,
    deleteTodo: Function,
  };

  static template = xml`
    <ul class="list-unstyled">
      <t t-foreach="props.todos.slice().reverse()" t-as="todo" t-key="todo.id">
        <Todo
          id="todo.id"
          label="todo.label"
          done="todo.done"
          markDone="props.markDone"
          deleteTodo="props.deleteTodo"
        />
      </t>
    </ul>
  `;
}

export class TodoApp extends Component {
  static components = { TodoList };

  setup() {
    this.state = useState({
      newTodo: "",
      todos: [
        { id: 1, label: "Learn OWL", done: false },
        { id: 2, label: "Build a Todo app", done: true },
      ],
    });
    this.nextId = this.state.todos.reduce((maxId, todo) => Math.max(maxId, todo.id), 0) + 1;

    useAutoFocus()
  }

  addTodo() {
    const label = this.state.newTodo.trim();
    if (!label) {
      return;
    }

    this.state.todos.push({ id: this.nextId++, label, done: false });
    this.state.newTodo = "";
  }

  markDone(id) {
    const todo = this.state.todos.find((todo) => todo.id === id);
    todo.done = !todo.done;
  }

  deleteTodo(id) {
    this.state.todos = this.state.todos.filter((todo) => todo.id !== id);
  }

  static template = xml`
    <div class="o_todo_page">
      <a class="position-fixed top-0 end-0 m-1" style="font-size: 0.65rem;" href="/awesome_owl">
        Counter
      </a>
      <form class="o_todo_input_bar" t-on-submit.prevent="addTodo">
        <input
          class="form-control"
          type="text"
          placeholder="Type a Task and press Enter"
          aria-label="New Todo"
          t-model="state.newTodo"
          t-ref="autofocus"
        />
      </form>
      <div class="o_todo_list_container">
        <TodoList
          todos="state.todos"
          markDone.bind="markDone"
          deleteTodo.bind="deleteTodo"
        />
      </div>
    </div>
  `;
}
