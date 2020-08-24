function add_comment(expand_text) {
  expand_text.addEventListener('click', (e) => {
    if (expand_text.id == 'comment_section' && e.target.id == 'add-comment') {
      expand_text.id = 'comment_section_active';

      // Get post_id
      const url = document.location.href;
      const id = url.replace(/.*\//g, '').replace(/[^\d]*/g, '');

      // Create form
      const form = document.createElement('form');
      form.method = 'POST';
      form.action = `/post/${id}`;

      // Construct comment text box
      const comment = document.createElement('input');
      comment.type = 'text';
      comment.className = 'comment-text-box';
      comment.id = 'content';
      comment.name = 'content';
      form.appendChild(comment);

      // Assign post id to the form
      const post_id = document.createElement('input');
      post_id.type = 'hidden';
      post_id.id = 'post-id';
      post_id.name = 'post-id';
      post_id.value = id;
      form.appendChild(post_id);

      // Construc submit button
      const submit = document.createElement('input');
      submit.id = 'comment-submit';
      submit.type = 'submit';
      submit.value = 'Comment';
      form.appendChild(submit);

      expand_text.insertBefore(form, expand_text.children[2]);
      console.log('Creating comment');
    }
  });
}

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
    date.innerHTML = `Posted on: ${month} ${day} ${year} ${time}`;
  }
}

function main() {
  convert_date();
  const expand_text = document.getElementById('comment_section');
  if (expand_text) add_comment(expand_text);
}

main();
