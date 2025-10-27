import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(name) {
    const addTodoInputRef = useRef(name);
    onMounted(() => {
        addTodoInputRef.el.focus();
        console.log(addTodoInputRef.el);
    });
}
