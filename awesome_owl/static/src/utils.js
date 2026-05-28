import { onMounted, useRef } from '@odoo/owl';

function useAutoFocus(refName) {
  const ref = useRef(refName);

  onMounted(() => {
    if (ref.el && ref.el.focus) {
      ref.el.focus();
    }
  });

  return ref;
}

export { useAutoFocus };
