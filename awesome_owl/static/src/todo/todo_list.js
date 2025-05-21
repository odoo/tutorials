/** @odoo-module **/

import { Component, useRef, onMounted, onWillUnmount } from "@odoo/owl";
import { TodoItem } from "@awesome_owl/todo/todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };
    static props = { items: { type: Array } };
    static NEXT_ID = 0;

    setup() {
        this.newTaskInputRef = useRef("newTaskInputRef");

        this.addItemKeyup = (ev) => ev.key === "Enter" && this.addItem();
        onMounted(() => {
            this.newTaskInputRef.el.addEventListener("keyup", this.addItemKeyup);
        });

        onWillUnmount(() => {
            this.newTaskInputRef.el.removeEventListener("keyup", this.addItemKeyup);
        });
    }

    addItem() {
        const newTask = this.newTaskInputRef.el.value;
        if (!newTask) {
            return;
        }

        this.props.items.push({
            id: TodoList.NEXT_ID++,
            description: newTask,
            isCompleted: false,
        });
        this.newTaskInputRef.el.value = "";
        this.newTaskInputRef.el.focus();
    }

    deleteItem(id) {
        const index = this.props.items.findIndex((item) => item.id === id);
        if (index !== -1) {
            this.props.items.splice(index, 1);
        }
    }
}
