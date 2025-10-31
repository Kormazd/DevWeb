// List of illustration filenames available under public/images/
export const sideImageNames = [
  'ArcherQueen_LNY_2025_Skin.png',
  'BK_CosmicCurse_f11_4k.png',
  'Grand_Warden_LNY2025_Skin_01.png',
  'GW_CosmicCurse_f01_4k.png',
  'hero_hall_lvl_06.png',
  'Hero_Minion_Prince_03_withShadow.png',
  'LNY25_Monk_Statue_Marketing.png',
  'Mega_Knight_03.png',
  'Pekka_12.png',
  'Prince_03.png',
  'Reine_archer_pekka.png',
  'TH17_HV_04.png',
  'Troop_HV_Golem_14.png',
  'Troop_HV_Hog_Rider_levell_14.png',
]

export function resolvePublicImage(name) {
  if (!name) return ''
  return name.startsWith('/') ? name : `/images/${name}`
}

export function pickTwoRandom(prevLeftUrl = '', prevRightUrl = '') {
  if (!Array.isArray(sideImageNames) || sideImageNames.length === 0) {
    return ['', '']
  }
  const toUrl = (n) => resolvePublicImage(n)

  // Filter out last picks if possible
  let pool = sideImageNames.filter(n => {
    const u = toUrl(n)
    return u !== prevLeftUrl && u !== prevRightUrl
  })
  if (pool.length < 2) pool = [...sideImageNames]

  const pick = () => pool[Math.floor(Math.random() * pool.length)]
  let lName = pick()
  let rName = pick()
  let guard = 0
  while (rName === lName && guard < 5) { rName = pick(); guard++ }
  return [toUrl(lName), toUrl(rName)]
}


