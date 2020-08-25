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

function main() {
  convert_date();
  const tab_list = document.getElementById('admin-tabs');
  if (tab_list) switch_tabs();
}

main();
