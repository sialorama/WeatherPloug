# weatherPloug 

J'ai mis en place une application web avec Streamlit pour afficher des informations météorologiques.  

Voici comment l'application fonctionne :

1. **Configuration des clés API :** Dans la barre latérale, vous pouvez entrer vos clés API pour OpenAI et OpenWeatherMap. Ces clés sont nécessaires pour accéder aux services de l'API OpenWeatherMap et générer les descriptions météorologiques.

2. **Informations météo :** Vous pouvez également spécifier le nom de la ville pour laquelle vous souhaitez obtenir les informations météorologiques. Une fois que vous avez entré la ville et cliqué sur le bouton "Afficher la météo", l'application récupère les données météorologiques de la ville spécifiée à partir de l'API OpenWeatherMap.

3. **Affichage des données météo actuelles :** Les données météorologiques actuelles, telles que la température, l'humidité, la pression et la vitesse du vent, sont affichées dans des widgets de type "metric" dans la colonne principale de l'application. De plus, une carte est affichée pour montrer l'emplacement de la ville sur une carte.

4. **Génération de descriptions météo :** Utilisant la température et la description météorologique actuelle obtenues à partir d'OpenWeatherMap, l'application génère une description météorologique plus détaillée à l'aide du modèle GPT d'OpenAI. Cette description est affichée sous les informations météorologiques actuelles.

5. **Prévisions météo hebdomadaires :** En plus des données météorologiques actuelles, l'application récupère également les prévisions météorologiques pour les sept prochains jours à partir de l'API OpenWeatherMap. Ces prévisions sont affichées dans un tableau avec les descriptions météorologiques, les températures minimales et maximales pour chaque jour.

6. **Gestion des erreurs :** L'application gère les cas où la ville spécifiée n'est pas trouvée ou lorsque les services météorologiques ne sont pas disponibles. Dans de tels cas, un message d'erreur est affiché à l'utilisateur.

Cette application offre une expérience conviviale pour obtenir des informations météorologiques actuelles et des prévisions pour une ville spécifique, ainsi que des descriptions météorologiques générées automatiquement pour enrichir les données météorologiques affichées.


