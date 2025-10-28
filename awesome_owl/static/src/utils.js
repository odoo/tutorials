import { useRef, onMounted } from "@odoo/owl";


export function useAutofocus(input) {
    const inputRef = useRef(input);
    onMounted(() => {
        inputRef.el.focus();
        console.log(inputRef.el);
    });
}
