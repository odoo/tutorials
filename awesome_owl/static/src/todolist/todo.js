import { Component, onMounted, useRef } from "@odoo/owl";

export class Todo extends Component {
  static template = "awesome_owl.todo";
  static props = {
    todo: {
      id: Number,
      description: String,
      isCompleted: Boolean,
    },
    toggleState: Function,
  };
  setup() {
    this.stateRef = useRef("todo_item_ref");
    onMounted(() => {
      if (this.props.todo.isCompleted) {
        this.stateRef.el.checked = true;
      }
    });
  }
  toggleState() {
    this.props.toggleState(this.props.todo.id);
  }
}
