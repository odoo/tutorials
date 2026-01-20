import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(name) {
    let inputRef = useRef(name);
    onMounted(() => {
        inputRef.el.focus();
    });
}
