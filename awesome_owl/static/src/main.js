import { whenReady } from "@odoo/owl";
import { mountComponent } from "@web/env";
import { Playground } from "./playground";
import { TodoList } from "./todo_list/todo_list";

const config = {
    dev: true,
    name: "Owl Tutorial",
};

// Mount the Playground component when the document.body is ready
// whenReady(() => mountComponent(Playground, document.body, config));
whenReady(() => mountComponent(TodoList, document.body, config));
