// Configuration des personnages pour les animations de fond
export const characters = [
  'mega-knight',
  'prince', 
  'dark-prince',
  'golem'
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
  },
  'dark-prince': {
    name: 'Prince Ténébreux',
    description: 'Version sombre du Prince avec des capacités spéciales'
  },
  'golem': {
    name: 'Golem',
    description: 'Tank puissant qui se divise en petits golems'
  }
}
