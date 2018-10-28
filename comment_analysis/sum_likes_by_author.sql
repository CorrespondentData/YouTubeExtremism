SELECT author_display_name, author_channel_url, author_channel_id, 
SUM(comment_like_count) as likes_sum, COUNT(*) as comments_sum,
AVG(comment_like_count) as likes_avg
FROM nl_comments_right
GROUP BY author_display_name, author_channel_url, author_channel_id
ORDER BY likes_sum DESC
