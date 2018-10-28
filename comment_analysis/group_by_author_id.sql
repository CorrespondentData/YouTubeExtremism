SELECT author_display_name, author_channel_url, author_channel_id, COUNT() as freq
FROM nl_comments_right
GROUP BY author_display_name, author_channel_url, author_channel_id
ORDER BY freq DESC;
