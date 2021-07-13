var socket = io();

const $comments = $("#comments");

const MAX_COMMENTS = 50;

function renderComment(comment) {
  const $comment = $(`
  <div class="card my-1">
    <div class="card-header">
        <span class="username text-primary">u/${comment.author}</span> 
        from <span class="subreddit text-danger">r/${comment.subreddit}</span> 
        commented at <span class="datetime text-secondary">${new Date(
          comment.created_utc * 1000
        )}</span>
    </div>
    <div class="card-body">
      ${comment.body}     
    </div>
    </div>`);
  return $comment;
}

function processNewComment(comment) {
  comment = JSON.parse(comment);
  // console.log(comment);
  const $comment = renderComment(comment);
  const $comments = $("#comments");
  $comment.hide().prependTo($comments).fadeIn("slow");
  //   console.log("Current comment count is " + $comments.length);
  if ($comments.children().length > MAX_COMMENTS) {
    $comments.children().last().remove();
  }
}

socket.on("comment", processNewComment);
