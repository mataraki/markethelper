document.addEventListener('DOMContentLoaded', function() {

  paginate(pagecount, pagenumber);

  if (newpost === "False") {
    document.querySelector('#newpost-form').style.display = 'none';
  }
  else {
    document.querySelector('#newpost-form').style.display = 'block';
  }
  
  if (document.querySelector('#follow-button') != null) {
    document.querySelector('#follow-button').addEventListener('click', () => follow());
  }

  // Submit a post
  document.querySelector('#newpost-form').onsubmit = function(event) {
    // Prevent page from reloading
    event.preventDefault();

    // Save the email
    fetch('/newpost', {
      method: 'POST',
      body: JSON.stringify({
          body: document.querySelector('#newpost-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });

    document.querySelector('#newpost-body').value = ""

    setTimeout(function(){load_posts(pagecount, pagenumber);}, 100);
  }
});

function follow() {
  fetch(`${username}/follow`, {
    method: 'POST'
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      document.querySelector('#follow-button').innerHTML = result.status;
      document.querySelector('#followers').innerHTML = result.followers;
      console.log(result);
  });
}

function load_posts(pagecount, pagenumber) {

  document.querySelector('#posts-view').innerHTML = ""

  // Populate the main page with posts
  fetch(`${apipath}${pagenumber}`)
  .then(response => response.json())
  .then(posts => {

      // Create the divs with posts
      posts.body.forEach(function(post) {
        const feedpost = document.createElement('div');
        feedpost.className = "feedpost";
        feedpost.id = `feedpost${post.id}`;
        feedpost.innerHTML = `<div class="postitself${post.id}"><h5><a href="/user/${post.user}">${post.user}</a></h5>`
        if (viewer === post.user) {
          feedpost.innerHTML += `<a class="edit" onClick="edit(${post.id})">Edit</a>`
        }
        feedpost.innerHTML += `<p class="body">${post.body}</p><p class="timestamp">${post.timestamp}</p><div class="likes"><img src="/static/network/like-icon.png" width="16px"><div class="likes-count">${post.likes}</div></div></div>`;
        feedpost.querySelector('.likes').querySelector('img').addEventListener('click', function() {
          fetch(`/like/${post.id}`, {
            method: 'POST'
          })
          .then(response => response.json())
          .then(result => {
              // Change the like count
              feedpost.querySelector('.likes').querySelector('.likes-count').innerHTML = result.likes;
          });
        })
            feedpost.style.animationPlayState = "running";
        document.querySelector('#posts-view').append(feedpost);

        if (viewer === post.user) {
          const editpost = document.createElement('form');
          editpost.className = "editpost";
          editpost.style.display = "none";
          editpost.id = `${post.id}`;
          editpost.innerHTML = `<div class="feedpost"><h5>Edit</h5><div class="form-group"><textarea id="editpost${post.id}-body" class="form-control">${post.body}</textarea></div><input class="btn btn-primary" type="submit" value="Edit"></div>`;
          editpost.onsubmit = function(event) {
            event.preventDefault();
            editbody = document.querySelector(`#editpost${post.id}-body`).value;
            fetch(`edit/${post.id}`, {
              method: 'POST',
              body: JSON.stringify({
                  body: editbody
              })
            })
            document.getElementById(`${post.id}`).style.display = "none";
            document.getElementById(`feedpost${post.id}`).querySelector('.body').innerHTML = editbody;
            document.getElementById(`feedpost${post.id}`).style.display = "block";
          }
          document.querySelector('#posts-view').append(editpost);
        }
      });
  });
};

function load_navigation(pagecount, pagenumber) {

  document.querySelector('#navigation-view').innerHTML = ""
  
  // Previous button
  const previous = document.createElement('li');
  if (pagenumber.toString() === '1') {
    previous.className = "page-item disabled";
    const prevbutton = document.createElement('a');
    prevbutton.className = "page-link";
      ;
    prevbutton.setAttribute('tabindex', "-1");
    prevbutton.setAttribute('aria-disabled', "true");
    prevbutton.innerHTML = "Previous"
    previous.appendChild(prevbutton);
  }
  else {
    previous.className = "page-item";
    const prevbutton = document.createElement('a');
    prevbutton.className = "page-link";
    prevbutton.setAttribute('onClick', `paginate(${pagecount}, ${parseInt(pagenumber)-1})`);
    prevbutton.setAttribute('tabindex', "0");
    prevbutton.setAttribute('aria-disabled', "false");
    prevbutton.innerHTML = "Previous"
    previous.appendChild(prevbutton);
  }
  document.querySelector('#navigation-view').append(previous);

  // Page buttons
  for (let i = 1; i <= pagecount; i++) {
    const page = document.createElement('li');
    page.className = "page-item";
    const pagebutton = document.createElement('a');
    pagebutton.className = "page-link";
    pagebutton.id = `page${i}`;
    pagebutton.setAttribute('onClick', `paginate(${pagecount}, ${i})`);
    pagebutton.innerHTML = `${i}`
    page.appendChild(pagebutton);
    document.querySelector('#navigation-view').append(page);
  }

  // Next button
  const next = document.createElement('li');
  if (!(pagenumber < pagecount)) {
    next.className = "page-item disabled";
    const nextbutton = document.createElement('a');
    nextbutton.className = "page-link";
    nextbutton.setAttribute('href', "#");
    nextbutton.setAttribute('tabindex', "-1");
    nextbutton.setAttribute('aria-disabled', "true");
    nextbutton.innerHTML = "Next"
    next.appendChild(nextbutton);
  }
  else {
    next.className = "page-item";
    const nextbutton = document.createElement('a');
    nextbutton.className = "page-link";
    nextbutton.setAttribute('onClick', `paginate(${pagecount}, ${parseInt(pagenumber)+1})`);
    nextbutton.setAttribute('tabindex', "0");
    nextbutton.setAttribute('aria-disabled', "false");
    nextbutton.innerHTML = "Next"
    next.appendChild(nextbutton);
  }
  document.querySelector('#navigation-view').append(next);
};

function paginate(pagecount, pagenumber) {
  load_posts(pagecount, pagenumber);
  load_navigation(pagecount, pagenumber);
  document.querySelector(`#page${pagenumber}`).parentElement.className = "page-item active";
  document.querySelector(`#page${pagenumber}`).parentElement.parentElement.style.animationPlayState = "running";
}

function edit(id) {
  document.querySelectorAll('.editpost').forEach(function(item){
    item.style.display = "none";  
  })
  document.querySelectorAll('.feedpost').forEach(function(item){
    item.style.animationPlayState = "paused";
    item.style.display = "block";  
  })
  document.getElementById(`feedpost${id}`).style.display = "none";
  document.getElementById(`${id}`).style.display = "block";
}