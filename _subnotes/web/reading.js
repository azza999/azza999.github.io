// Include answer explanations in print/PDF, then restore the reading state.
let answerStates = [];
window.addEventListener('beforeprint', () => {
  answerStates = [...document.querySelectorAll('details.answer')].map(node => [node, node.open]);
  answerStates.forEach(([node]) => { node.open = true; });
});
window.addEventListener('afterprint', () => {
  answerStates.forEach(([node, wasOpen]) => { node.open = wasOpen; });
  answerStates = [];
});
