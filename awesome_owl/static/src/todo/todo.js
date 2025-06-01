import { Component, useState } from "@odoo/owl";


export class Todo extends Component {
    static template = "awesome_owl.Todo";
    static props = {
        id: { type: Number },
        description: { type: String },
        isCompleted: { type: Boolean },
        toggleCompletionState: { type: Function },
        removeTodo: { type: Function },
    };

    setup() {
        this.state = useState({});
    };
};
