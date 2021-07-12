import praw
import praw.models

def comment_to_json(comment):
    '''Convert reddit comment object to python dict (json)'''
    if not isinstance(comment, praw.models.Comment):
        raise ValueError('Input arg in not of type praw.models.Comment')
    return {
        'author': str(comment.author),
        'body': str(comment.body),
        'created_utc': comment.created_utc,
        'id': comment.id,
        'score': comment.score,
        'subreddit': str(comment.subreddit)
    }