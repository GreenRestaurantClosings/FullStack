var myHeading = document.querySelector('h1');
myHeading.textContent = 'Restaurants Most Likely to Close on Green Street';
var mostRecentRatings = {};
mostRecentRatings["Cravings"] = "55, 59, 60, 62";
mostRecentRatings["Jimmy John's"] = "65, 61, 74, 87";
mostRecentRatings["McDonalds"] = "67, 54, 73, 30";
var restaurant = prompt("Type in your favorite restaurant on Green Street!")
if (restaurant.toLowerCase()== "cravings") {
  alert("Most Recent Inspection Scores: " + mostRecentRatings["Cravings"]);
}
if (restaurant.toLowerCase()== "jimmy john's") {
  alert("Most Recent Inspection Scores: " + mostRecentRatings["Jimmy John's"]);
}
if (restaurant.toLowerCase()== "mcdonalds") {
  alert("Most Recent Inspection Scores: " + mostRecentRatings["McDonalds"]);
}

