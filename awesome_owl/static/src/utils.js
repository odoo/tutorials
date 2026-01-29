import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(name) {
    const inputRef = useRef(name);

    onMounted(() => {
        if (inputRef.el) {
            inputRef.el.focus();
        }
    });

    return inputRef;
}
