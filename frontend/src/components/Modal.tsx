export function Modal({ open, onClose, children }) {
	return (
    <div onClick={onClose}  className={ `fixed inset-0 flex justify-center items-end md:items-center ${open ? "visible bg-black/20": "hidden"}`}>
      <div onClick={e => e.stopPropagation()}>
        { children }
      </div>
		</div>
	);
}

export default Modal;
