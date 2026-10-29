import { Component, useProps, t } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item"; 
    
    props = useProps ({
        todo: t.object({
            id: t.number(),
            text: t.string(),
            completed: t.boolean()
        }),
    });

}