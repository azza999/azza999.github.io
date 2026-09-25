import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
// Import the browser module independently of the parent Jekyll package's module type.
const source = await readFile(new URL('../layout.js', import.meta.url), 'utf8');
const { paginate, drawing } = await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`);
const base = { columns: 12, mode: 'trace-only', content: '가나다', spaces: true, size: 70, opacity: 20, color: '#b77770', guide: 'cross', title: '연습' };
const characters = (page, state) => drawing(page, state, 0, 1, 'Pen').filter(op => op.type === 'text' && op.font === 'Pen');

test('trace-only writes each character once, on consecutive faint rows', () => {
  const state = { ...base, content: '가나\n다라' };
  const page = paginate(state)[0];
  const chars = characters(page, state);
  assert.equal(chars.map(op => op.value).join(''), '가나다라');
  assert.ok(chars.every(op => op.color === '#d6d6d6'));
  assert.ok(Math.abs(chars[2].y - chars[0].y - page.cell) < 1e-9);
});

test('trace-only preserves every character across A4 pages at all column counts', () => {
  for (const columns of [10, 12, 14, 16, 20]) {
    const state = { ...base, columns, content: '가나다라마바사'.repeat(100) };
    const pages = paginate(state);
    assert.equal(pages.flatMap(p => characters(p, state)).map(op => op.value).join(''), state.content);
    assert.ok(pages.every(p => p.repeat === 1 && p.groups * p.cell <= 220));
    assert.ok(pages.length < paginate({ ...state, mode: 'trace' }).length);
  }
});

test('opacity changes trace-only text; the original-plus-trace layout remains unchanged', () => {
  const state = { ...base, content: '한', opacity: 50 };
  assert.equal(characters(paginate(state)[0], state)[0].color, '#989898');
  const old = { ...state, mode: 'trace' };
  const chars = characters(paginate(old)[0], old);
  assert.equal(chars.length, 2);
  assert.equal(chars[0].color, '#30352f');
  assert.equal(chars[1].color, '#989898');
});
