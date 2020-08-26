function convert_date() {
  const dates = document.getElementsByClassName('publish-date');
  for (date of dates) {
    months_name = [
      'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December',
    ];
    const year = date.textContent.match(/\d{4}/).join();
    let month = date.textContent
      .match(/-\d{2}/)
      .join()
      .match(/\d{2}/)
      .join();
    month = months_name[+month];
    const day = date.textContent
      .match(/-\d{2} /)
      .join()
      .match(/\d{2}/)
      .join();
    const time = date.textContent.match(/\d{2}:\d{2}:\d{2}/).join();
    date.innerHTML = `${month} ${day} ${year} ${time}`;
  }
}

function switch_tabs() {
  const tab_list = document.getElementById('admin-tabs');
  tab_list.addEventListener('click', (e) => {
    if (e.target.className == 'nav-link') {
      const posts = document.getElementById('posts-tab');
      const users = document.getElementById('users-tab');
      if (e.target.id == 'tab-2') {
        const old_tab = document.getElementById('tab-1');
        old_tab.className = 'nav-link';
        e.target.className = 'nav-link active';
        users.style.display = 'block';
        posts.style.display = 'none';
        console.log(posts.style.display);
      } else {
        const old_tab = document.getElementById('tab-2');
        old_tab.className = 'nav-link';
        e.target.className = 'nav-link active';
        users.style.display = 'none';
        posts.style.display = 'block';
      }
    }
  });
}

async function fetch_likes(like_bar, e, i) {
  const vote_class = e.target.className;
  const post_id = like_bar[i].parentElement.id;
  let data = await fetch(`/post/votes/${post_id}`);
  data = await data.json();

  // Case where user is first voting to upvote
  if (vote_class == 'upvote') {
    console.log(1);
    e.target.className = `${vote_class} voted`;
    // Case where user is changing votes
    if (like_bar[i].childNodes[3].className == 'devote voted') {
      console.log('devoted');
      like_bar[i].childNodes[3].className = 'devote';
      data.dislikes--;
    }
    data.likes++;
  }
  // Case where user is first voting to devote
  else if (vote_class == 'devote') {
    console.log(2);
    e.target.className = `${vote_class} voted`;
    // Case where user is changing votes
    if (like_bar[i].childNodes[1].className == 'upvote voted') {
      console.log('upvoted');
      like_bar[i].childNodes[1].className = 'upvote';
      data.likes--;
    }
    data.dislikes++;
  }
  // Case where user is first voting to remove their vote
  else {
    if (vote_class == 'upvote voted') {
      console.log('devoted for upvote');
      like_bar[i].childNodes[1].className = 'upvote';
      // data.likes--;
    } else if (vote_class == 'devote voted') {
      console.log('devoted for devote');
      like_bar[i].childNodes[3].className = 'devote';
      // data.dislikes--;
    }
  }
  // console.log(like_bar[i].childNodes);
  console.log(data);
  return data;
}

function like_bar() {
  const like_bar = document.getElementsByClassName('like-bar');
  if (like_bar) {
    for (let i = 0; i < like_bar.length; i++) {
      like_bar[i].addEventListener('click', (e) => {
        fetch_likes(like_bar, e, i).then((r) => console.log(r));
      });
    }
  }
}

function main() {
  convert_date();
  const tab_list = document.getElementById('admin-tabs');
  if (tab_list) switch_tabs();
  like_bar();
}

main();
