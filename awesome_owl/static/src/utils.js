import { onMounted, useRef } from "@odoo/owl";

export function useAutoFocus() {
    const ref = useRef("add-todo-input");
    
    onMounted(() => {
        if (ref.el) {
            ref.el.focus();
        }
    });
    
    return ref;
}
