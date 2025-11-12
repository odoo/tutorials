import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(refName) {
    const inputRef = useRef(refName);
    onMounted(() => {
        if (inputRef.el) {
            inputRef.el.focus();
        }
    });
}
