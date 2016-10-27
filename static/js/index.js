function showRating(rating){
  $('#user-score').html("Your User Score: " + rating);
}

function updateRating(evt){
  evt.preventDefault();

  var formInputs = {
    'update_rating': $("input:radio[name=update_rating]:checked").val(),
    'user_id': $("#update-user").val(),
    'movie_id': $("#update-movie").val()
  };
    
$.post("/rate_movie", formInputs, showRating);
}

$('#update-rating-form').on('submit', updateRating);

function showNewRating(rating) {
  console.log(rating);
  $('#new-user-score').html("Your User Score: " + rating);
}

function newRating(evt) {
  evt.preventDefault();

  var formInputs = {
    'rating': $("input:radio[name=rating]:checked").val(),
    'user_id': $("#new-user").val(),
    'movie_id': $("#new-movie").val()
  };
  console.log(formInputs);

  $.post("/rate_movie", formInputs, showNewRating);
}

$('#new-rating-form').on('submit', newRating);
