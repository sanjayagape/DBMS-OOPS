// Run with Node. Uses the bundled sharp runtime when SHARP_PATH is provided.
const fs = require('node:fs/promises'); const path = require('node:path');
const sharp = require(process.env.SHARP_PATH || 'sharp');
async function main() {
  const source = await fs.readFile(path.join(__dirname, '../public/favicon.svg'));
  const dir = path.join(__dirname, '../public/icons'); await fs.mkdir(dir, { recursive:true });
  for (const size of [192,512]) await sharp(source).resize(size,size).png().toFile(path.join(dir,`icon-${size}.png`));
  const centered = await sharp(source).resize(300,300).png().toBuffer();
  await sharp({ create:{ width:512,height:512,channels:4,background:'#246B45' } }).composite([{ input:centered,gravity:'center' }]).png().toFile(path.join(dir,'maskable-512.png'));
}
main().catch(e => { console.error(e); process.exitCode = 1 });
