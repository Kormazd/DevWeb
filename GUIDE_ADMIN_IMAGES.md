# 🎨 Guide Admin - Comment ajouter des images aux questions

## ✅ Problème résolu

L'admin ne peut plus créer de questions car l'upload d'images a été retiré. Voici comment procéder maintenant :

---

## 📋 Étapes pour créer une question avec image

### 1️⃣ Ajouter l'image dans le projet

**Option A : Image déjà disponible**

Les images suivantes sont déjà dans `public/images/` :
- `Mega_Knight_03.png`
- `Prince_03.png`
- `Pekka_12.png`
- `Reine_archer_pekka.png`
- `ArcherQueen_LNY_2025_Skin.png`
- `BK_CosmicCurse_f11_4k.png`
- `Grand_Warden_LNY2025_Skin_01.png`
- `GW_CosmicCurse_f01_4k.png`
- `hero_hall_lvl_06.png`
- `Hero_Minion_Prince_03_withShadow.png`
- `LNY25_Monk_Statue_Marketing.png`
- `TH17_HV_04.png`
- `Troop_HV_Golem_14.png`
- `Troop_HV_Hog_Rider_levell_14.png`

**Option B : Nouvelle image**

```bash
# Copier votre nouvelle image dans le dossier public/images
cp mon-image.png quiz-ui/public/images/
```

---

### 2️⃣ Créer la question dans l'admin

1. **Se connecter à l'admin** : `http://localhost:5173/admin`

2. **Créer une nouvelle question**

3. **Remplir les champs** :
   - **Titre** : Ex. "Quelle carte est la plus résistante ?"
   - **Texte** : Description de la question
   - **Jeu** : Clash of Clans / Clash Royale / etc.
   - **Position** : Ordre d'affichage
   - **Image** : **Saisir simplement le nom du fichier**
     ```
     Pekka_12.png
     ```
     ou le chemin complet :
     ```
     /images/Pekka_12.png
     ```

4. **Ajouter les 4 réponses** :
   - Remplir le texte de chaque réponse
   - Cocher **une seule** réponse comme correcte

5. **Sauvegarder**

✅ **Résultat** : L'image s'affiche dans l'aperçu et dans le quiz !

---

## 🖼️ Formats d'image acceptés

| Format saisi | Exemple | Résolution |
|--------------|---------|-----------|
| Nom simple | `Pekka_12.png` | `/images/Pekka_12.png` |
| Chemin absolu | `/images/Prince_03.png` | `/images/Prince_03.png` |
| URL externe | `https://example.com/img.jpg` | `https://example.com/img.jpg` |

---

## 🎯 Ce qui a changé

### ❌ Avant (ne fonctionne plus)
- Bouton "Choisir un fichier" pour uploader
- Upload automatique vers le backend
- Stockage dans `/uploads/`

### ✅ Maintenant (simplifié)
- Champ texte pour saisir le nom du fichier
- Images servies depuis `public/images/`
- Pas d'upload, tout est statique

---

## 🧪 Tester

### Test 1 : Créer une question avec image existante

1. Admin > Créer une question
2. Saisir dans **Image** : `Pekka_12.png`
3. Ajouter 4 réponses
4. Sauvegarder
5. ✅ Aller dans le quiz → l'image s'affiche

### Test 2 : Créer une question avec nouvelle image

1. Copier `ma-nouvelle-image.png` dans `public/images/`
2. Admin > Créer une question
3. Saisir dans **Image** : `ma-nouvelle-image.png`
4. Ajouter 4 réponses
5. Sauvegarder
6. ✅ Aller dans le quiz → l'image s'affiche

### Test 3 : Aperçu dans l'admin

1. Admin > Créer une question
2. Saisir dans **Image** : `Prince_03.png`
3. ✅ L'aperçu s'affiche immédiatement sous le champ

---

## 🐛 Dépannage

### L'aperçu ne s'affiche pas dans l'admin

**Cause** : L'image n'existe pas dans `public/images/`

**Solution** :
```bash
# Vérifier que l'image existe
ls quiz-ui/public/images/Prince_03.png

# Si non, la copier
cp src/assets/Prince_03.png quiz-ui/public/images/
```

### L'image ne s'affiche pas dans le quiz

**Causes possibles** :
1. Nom de fichier incorrect (respecter la casse : `Pekka_12.png` ≠ `pekka_12.png`)
2. Extension oubliée (écrire `Pekka_12.png` et non `Pekka_12`)
3. Image pas dans `public/images/`

**Solution** :
```bash
# Vérifier l'existence
ls quiz-ui/public/images/

# Vérifier le nom exact
ls quiz-ui/public/images/ | grep -i pekka
```

### Erreur "Upload failed" ou similaire

**Cause** : Le code essaie toujours d'uploader (ancien code non mis à jour)

**Solution** : Le composant `AdminQuestionEdit.vue` a été corrigé, vider le cache du navigateur :
- Chrome/Edge : `Ctrl+Shift+R` (Windows) ou `Cmd+Shift+R` (Mac)
- Firefox : `Ctrl+F5` (Windows) ou `Cmd+Shift+R` (Mac)

---

## 📝 Messages d'aide dans l'interface

Le champ **Image** affiche maintenant un message d'aide :

> 💡 Les images doivent être dans `public/images/`.  
> Saisissez simplement le nom du fichier (ex: "Pekka_12.png") ou le chemin complet (ex: "/images/Pekka_12.png").

---

## 🎨 Aperçu automatique

Dès que vous saisissez un nom de fichier dans le champ **Image**, un aperçu s'affiche automatiquement en dessous (si l'image existe).

**Exemple** :
1. Saisir : `Mega_Knight_03.png`
2. ✅ L'aperçu apparaît instantanément

Si l'aperçu n'apparaît pas → l'image n'existe pas dans `public/images/`

---

## 🚀 Workflow recommandé

```bash
# 1. Ajouter toutes vos images dans public/images/
cp *.png quiz-ui/public/images/

# 2. Lister les images disponibles
ls quiz-ui/public/images/

# 3. Créer les questions dans l'admin en utilisant les noms de fichiers

# 4. Tester dans le quiz
```

---

## ✅ Modifications apportées à `AdminQuestionEdit.vue`

### Retiré
- ❌ Bouton `<input type="file">` (upload)
- ❌ Fonction `onFileChange()`
- ❌ Fonction `uploadIfNeeded()`
- ❌ Variables `previewUrl` et `apiBase`

### Ajouté
- ✅ Message d'aide explicatif
- ✅ Aperçu automatique basé sur le nom saisi
- ✅ Gestion d'erreur si l'image n'existe pas (@error sur l'img)

---

## 📊 Comparaison

| Aspect | Avant | Maintenant |
|--------|-------|------------|
| Upload | Bouton + backend | ❌ Supprimé |
| Stockage | `/uploads/` (backend) | `public/images/` (frontend) |
| Saisie | Sélection de fichier | Nom de fichier en texte |
| Aperçu | Après upload | Instantané (dès saisie) |
| Complexité | Upload + validation backend | Simple : juste un nom |

---

## 🎉 Avantages

1. **Simplicité** : Plus besoin d'uploader, juste saisir un nom
2. **Rapidité** : Aperçu instantané sans attendre l'upload
3. **Fiabilité** : Les images sont versionnées avec le code
4. **Performance** : Vite optimise et sert les images très rapidement
5. **Prévisibilité** : Les noms de fichiers sont stables

---

## 📞 Aide rapide

**Comment ajouter une image ?**
```bash
cp mon-image.png quiz-ui/public/images/
```

**Comment la référencer dans l'admin ?**
```
mon-image.png
```

**Comment vérifier qu'elle existe ?**
```bash
ls quiz-ui/public/images/mon-image.png
```

**L'aperçu ne marche pas ?**
- Vérifier le nom exact (casse comprise)
- Vérifier l'extension (.png, .jpg, etc.)
- Vérifier que l'image est bien dans `public/images/`

---

✅ **Prêt à créer des questions avec images !** 🚀

