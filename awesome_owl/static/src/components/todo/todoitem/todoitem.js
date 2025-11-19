import { Component, onMounted, useRef } from "@odoo/owl"
import { Card } from "../../card/card"

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem"
    static components = { Card }
    static props = {
        id: { type: Number },
        description: { type: String },
        isCompleted: { type: Boolean, default: false },
        markTodocallback: { type: Function },
        deleteTodocallback: { type: Function }
    }

    setup() {
        super.setup();
        this.todo_ref = useRef("todo_ref");
        this.todo_togglestatus = useRef("todo_togglestatus");

        onMounted(() => {
            requestAnimationFrame(() => {
                this.todo_ref.el.classList.add("show");
            });

            this.todo_togglestatus.el.addEventListener("change", () => {
                this.props.markTodocallback(this.props.id);
                
            })
        });

    }
    
    deleteTodo() {
        this.props.deleteTodocallback(this.props.id)
    }
}
