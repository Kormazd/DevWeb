// Configuration des personnages pour les animations de fond
export const characters = [
  'mega-knight',
  'prince'
]

// Mapping des questions vers les personnages
export const questionCharacterMapping = (questionIndex) => {
  // Force l'image Méga Chevalier pour le fond
  return 'mega-knight'
}

// Informations sur les personnages
export const characterInfo = {
  'mega-knight': {
    name: 'Méga Chevalier',
    description: 'Carte légendaire qui saute et écrase les troupes en zone'
  },
  'prince': {
    name: 'Prince',
    description: 'Troupe qui charge et inflige des dégâts doublés'
  }
}
