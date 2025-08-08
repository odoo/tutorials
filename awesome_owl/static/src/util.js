import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(refName) {
    const inputRef = useRef("inputAddTodo");

    onMounted(() => {
        inputRef.el.focus();
    })
}