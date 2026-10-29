import { Component, useProps, t } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card"; 
    
    props = useProps ({
        title: t.string(),
        content: t.string()
    });

    // setup() {
    // }
}