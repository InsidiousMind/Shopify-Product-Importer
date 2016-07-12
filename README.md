# Shopify-Product-Importer
Formats CSV file into correct format to be imported into Shopify

Currently is a bit spaghetti coded because I needed this out by a close deadline.

Optimization Checklist:
 Edit Variants, cells, etc in ParseItem at once instead of only editing one item and iterating over every row n times. 
      editCell method time is currently at O(n)
        needs to be better
 Delete trailing whitespace after handle
 Take Grey and Brown out of Title
  IE brown werewolf, Grey werewolf
 make Lg Sm etc Large Small etc. for readability
 Recognize Lg Sm etc with regex instead of hardcoded lists
 find a better way to do things instead of rand file name gens

