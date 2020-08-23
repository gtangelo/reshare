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

const expand_text = document.getElementById('comment_section');
if (expand_text) add_comment(expand_text);
