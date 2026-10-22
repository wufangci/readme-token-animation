const fs = require('fs');
const { encode } = require('gpt-tokenizer/encoding/o200k_base');
const ranks = require(require('path').join(__dirname,'..','node_modules/gpt-tokenizer/cjs/bpeRanks/o200k_base.js')).default;
const src = fs.readFileSync(process.argv[2], 'utf8');
// AI 讀到的是整份檔案；去掉第一行的語言切換連結
const text = src.replace(/^\*\[.*?\]\(.*?\)\*\s*\n/, '');
const ids = encode(text);
const out = ids.map(id => {
  const r = ranks[id];
  const bytes = typeof r === 'string' ? [...Buffer.from(r, 'utf8')] : r;
  let str = null;
  try { str = new TextDecoder('utf-8', { fatal: true }).decode(Uint8Array.from(bytes)); } catch (e) { str = null; }
  return { id, bytes, str };
});
fs.writeFileSync(process.argv[3], JSON.stringify(out));
const frag = out.filter(t => t.str === null).length;
console.log('chars', [...text].length, 'tokens', ids.length, 'fragments', frag);
