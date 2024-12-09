import toasteventbus from 'primevue/toasteventbus'

export function info(summary, detail, life= 3000) {
  toasteventbus.emit('add', { severity: 'info', summary, detail, life })
}

export  function warn(summary, detail, life= 3000) {
  toasteventbus.emit('add', { severity: 'warn', summary, detail, life })
}

export  function success(summary, detail, life= 3000) {
  toasteventbus.emit('add', { severity: 'success', summary, detail, life })
}

export function error(summary, detail, life= 3000) {
  toasteventbus.emit('add', { severity: 'error', summary, detail, life })
}