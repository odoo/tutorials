import { whenReady } from "@odoo/owl";
import { mountComponent } from "@web/env";
import { Playground } from "./playground";
import { TodoList } from "./components/todolist/todolist";

const config = {
    dev: true,
    name: "Owl Tutorial",
};

// Mount the Playground component when the document.body is ready
whenReady(() => mountComponent(TodoList, document.body, config));
