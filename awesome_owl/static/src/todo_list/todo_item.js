import { Component, useRef, onMounted } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        item: Object,
        callbackBox: Function,
        callbackDel: Function,
    };

    onCheck(ev) {
        const checked = ev.target.checked;
        this.props.callbackBox(this.props.item.id, checked);
    }
    onDelete(){
        this.props.callbackDel(this.props.item.id);
    }
}
