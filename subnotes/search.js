const search = document.querySelector('#search');
const category = document.querySelector('#category');
const scope = document.querySelector('#scope');
const cards = [...document.querySelectorAll('.note-card')];
function filter() {
  const terms = search.value.trim().toLocaleLowerCase('ko').split(/\s+/).filter(Boolean);
  let count = 0;
  cards.forEach(card => {
    const visible = (!category.value || card.dataset.category === category.value) &&
      (!scope.value || card.dataset.scope === scope.value) &&
      terms.every(term => card.dataset.search.includes(term));
    card.hidden = !visible;
    count += Number(visible);
  });
  document.querySelector('#results').textContent = `${cards.length}개 중 ${count}개의 노트`;
  document.querySelector('#empty').hidden = count !== 0;
}
search.addEventListener('input', filter);
category.addEventListener('change', filter);
scope.addEventListener('change', filter);
document.querySelector('#reset').addEventListener('click', () => {
  search.value = '';
  category.value = '';
  scope.value = '';
  filter();
  search.focus();
});
