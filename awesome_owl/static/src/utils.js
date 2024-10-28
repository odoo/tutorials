import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(ref) {
    let inputRef = useRef(ref);
    onMounted(() => {
        if (inputRef) inputRef.el.focus();
    });
}
