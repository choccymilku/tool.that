// if html is getstuff.html, then the path is code/getstuff.js
if (window.location.href.indexOf('profiles') > -1) {
    var blocks = document.getElementsByClassName('block');

    for (var i = 0; i < blocks.length; i++) {
        blocks[i].addEventListener('click', function() {
          console.log(this.id + ' - left block');

          console.log('window.location.href = ./tools/' + this.id + '.html');

    
            window.location.href = './' + this.id + '.html';
        });
    }
} else {
/*     var blocks = document.getElementsByClassName('block');

    for (var i = 0; i < blocks.length; i++) {
        blocks[i].addEventListener('click', function() {
          console.log(this.id + ' - left block');
    
    if (this.id === 'compress') {
        window.location.href = './tools/compressor/templates/' + this.id + '.html';
    } else if (this.id === 'profiles') {
        window.location.href = './tools/profiles/' + this.id + '_index' + '.html';
    } else {
        window.location.href = './' + this.id + '.html';
    }
        });
    } */
}