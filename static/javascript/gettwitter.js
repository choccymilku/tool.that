var twitter_input = document.getElementById('search_input');
var twitter_url = 'https://api.choccymilk.uk/twitter/';

twitter_input.addEventListener('keyup', function(event) {
  if (event.keyCode === 13) {
    // Disable input and show "Searching..."
    twitter_input.disabled = true;
    // remove spaces from input
    var searchText = twitter_input.value.replace(/\s/g, '');
    console.log(`searching for ${searchText}`);
    twitter_input.value = 'searching...';

    document.querySelector('.back').style.display = 'none';
    document.querySelector('.searching').style.display = 'block';

    // fetch the twitter api
    fetch(twitter_url + searchText)
      .then(response => response.json())
      .then(data => {
        console.log(data);
        twitter_input.value = 'found!';

        document.querySelector('.back').style.display = 'block';
        document.querySelector('.searching').style.display = 'none';

        document.getElementById('pfp').src = data.profile.picture;

        if (data.profile.banner == null) {
          document.getElementById('banner').src = '../styles/blankbanner.png';
        } else {
        document.getElementById('banner').src = data.profile.banner;
        }

        document.getElementById('display').innerHTML = data.profile.handle;
        document.getElementById('handle').innerHTML = data.profile.username;
        document.getElementById('bio').innerHTML = data.profile.about;

        setTimeout (function() {
          twitter_input.disabled = false;
          twitter_input.value = '';
        }, 750);
      });
  }
});
