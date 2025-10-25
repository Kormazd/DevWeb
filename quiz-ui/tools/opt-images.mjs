// Simple image optimizer: generates webp versions into src/assets-optimized
// Requires: npm i -D sharp fast-glob
import fg from 'fast-glob'
import path from 'node:path'
import fs from 'node:fs/promises'
import sharp from 'sharp'

const SRC_DIR = path.resolve(process.cwd(), 'src/assets')
const OUT_DIR = path.resolve(process.cwd(), 'src/assets-optimized')

const MAX_WIDTH = 900
const QUALITY = 72

async function ensureDir(dir){
  await fs.mkdir(dir, { recursive: true })
}

async function main(){
  await ensureDir(OUT_DIR)
  const patterns = ['**/*.png', '**/*.jpg', '**/*.jpeg']
  const files = await fg(patterns, { cwd: SRC_DIR, onlyFiles: true })
  console.log(`Found ${files.length} images to optimize`)
  let converted = 0
  for (const rel of files){
    const src = path.join(SRC_DIR, rel)
    const dstRel = rel.replace(/\.[^.]+$/, '.webp')
    const dst = path.join(OUT_DIR, dstRel)
    await ensureDir(path.dirname(dst))
    try {
      // Skip if already exists
      await fs.access(dst).then(() => { throw new Error('exists') }).catch(e => { if(e.message==='exists') throw e })
      const img = sharp(src)
      const meta = await img.metadata()
      const width = meta.width || MAX_WIDTH
      const targetWidth = Math.min(width, MAX_WIDTH)
      await img.resize({ width: targetWidth }).webp({ quality: QUALITY }).toFile(dst)
      converted++
      console.log(`Optimized: ${rel} -> ${path.relative(process.cwd(), dst)}`)
    } catch(e){
      if(e.message === 'exists'){
        // already present
      } else {
        console.warn(`Failed to optimize ${rel}:`, e.message)
      }
    }
  }
  console.log(`Done. Converted ${converted}/${files.length}. Output: src/assets-optimized`)
}

main().catch(err => {
  console.error(err)
  process.exit(1)
})

