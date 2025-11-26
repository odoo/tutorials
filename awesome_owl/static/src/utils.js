import { useRef, onMounted } from '@odoo/owl';

function useAutoFocus(refName) {
    const inputRef = useRef(refName);
    onMounted(() => {
        inputRef.el.focus();
    });
}

export { useAutoFocus };
