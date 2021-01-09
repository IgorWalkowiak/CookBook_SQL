<!DOCTYPE html>
<html>
   <head>
      <meta charset="utf-8">
      <title>Browse recipe</title>
      <link rel="stylesheet" href="../assets/style.css">
   </head>
   <body>
      <div class = 'searchPanel'>
         <form id = 'search' action='/recipes/browseRecipes.php' method='get'>
            Text: <input type="text" name="textSearch">
            Tag: <input type="text" name="tag">
            Sort by: 
            <select id="sort" name="sort">
               <option value="fromBest">From the best</option>
               <option value="fromWorst">From the worst</option>
               <option value="default">Default</option>
            </select>
            <input type="submit" value="Search">
         </form>
      </div>
      <div class = "recipes">
         <h3> Recipes! </h3>
         <?php
         $criteria = [
           [
             '$project' => [
               'title' => 1,
               'description' => 1,
               'owner' => 1,
               'tags' => 1,
               'posVotes' => ['$size' => '$positiveVoters'],
               'negVotes' => ['$size' => '$negativeVoters'],
               'rate' => ['$subtract' => [['$size' => '$positiveVoters'], ['$size' => '$negativeVoters']]],
             ],
           ],
         ];
         $match = [];
         if (isset($_GET['textSearch']) && $_GET['textSearch'] != '' && isset($_GET['tag']) && $_GET['tag'] != '') {
           $match = [
             '$match' => [
               '$and' => [
                 [
                   '$or' => [
                     [
                       'title' => ['$regex' => new MongoDB\BSON\Regex(preg_quote($_GET['textSearch']), 'i')],
                     ],
                     [
                       'description' => ['$regex' => new MongoDB\BSON\Regex(preg_quote($_GET['textSearch']), 'i')],
                     ],
                   ],
                 ],
                 ['tags' => ['$in' => [$_GET['tag']]]],
               ],
             ],
           ];
           array_push($criteria, $match);
         } elseif (isset($_GET['textSearch']) && $_GET['textSearch'] != '') {
           $match = [
             '$match' => [
               '$or' => [
                 [
                   'title' => ['$regex' => new MongoDB\BSON\Regex(preg_quote($_GET['textSearch']), 'i')],
                 ],
                 [
                   'description' => ['$regex' => new MongoDB\BSON\Regex(preg_quote($_GET['textSearch']), 'i')],
                 ],
               ],
             ],
           ];
           array_push($criteria, $match);
         } elseif (isset($_GET['tag']) && $_GET['tag'] != '') {
           $match = [
             '$match' => [
               'tags' => [
                 '$in' => [$_GET['tag']],
               ],
             ],
           ];
           array_push($criteria, $match);
         }

         if (isset($_GET['sort'])) {
           $sort = [];
           if ($_GET['sort'] == 'fromBest') {
             $sort = ['$sort' => ['rate' => -1]];
           } elseif ($_GET['sort'] == 'fromWorst') {
             $sort = ['$sort' => ['rate' => 1]];
           } else {
           }
           if (!empty($sort)) {
             array_push($criteria, $sort);
           }
         }
         require_once __DIR__ . '\..\phpmongodb\vendor\autoload.php';
         include dirname(__DIR__) . '../credentials.php';
         $client;
         if (isset($_SESSION["loggedIn"]) && $_SESSION["loggedIn"] == true) {
           $client = new MongoDB\Client('mongodb://' . $chefAccount . '@' . $serverAddress . '/?authSource=cook');
         } else {
           $client = new MongoDB\Client('mongodb://' . $guestAccount . '@' . $serverAddress . '/?authSource=cook');
         }
         $cookDb = $client->cook;
         $recipesColl = $cookDb->recipes;
         $users = $cookDb->users;
         $recipes = $recipesColl->aggregate($criteria);

         foreach ($recipes as $recipe) {
           $owner = $users->findOne(['_id' => $recipe['owner']]);

           echo "<div class = 'recipe'>";
           echo "<p class = 'title'>" . $recipe['title'] . "</p><br>";
           if (isset($owner["login"])) {
             echo "<p class = 'author'> Autor: " . $owner["login"] . "</p>";
           } else {
             echo "<p class = 'author'> Autor: Not found! </p>";
           }
           echo $recipe['description'] . "<br/>";
           echo "<p class = 'posVotes'> Positive votes: " . $recipe['posVotes'] . "</p>";
           echo "<p class = 'negVotes'> Negative votes: " . $recipe['negVotes'] . "</p>";
           echo "<p class = 'rate'> sum: " . $recipe['rate'] . "</p>";
           echo "<a class ='moreLink' href='/recipes/recipe.php?id=" . $recipe['_id'] . "'> Read more! </a>";
           echo "</div>";
         }
         ?>
      </div>
      <nav>
          <a href="/index.php">Home</a>
         <a href="/recipes/browseRecipes.php">Browse recipes</a>
         <?php
         if (!session_id()) {
           @session_start();
         }
         if (isset($_SESSION["loggedIn"]) && $_SESSION["loggedIn"] == true) {
           echo "<a href='/recipes/newRecipe.php'>Add new recipe</a>";
           echo "<a href='/loginSystem/logout.php'>Logout </a>";
         } else {
           echo "<a href='/loginSystem/login.php'>Log in</a>";
           echo "<a href='/loginSystem/register.php'>Register</a>";
         }
         ?>
      </nav>
   </body>
</html>