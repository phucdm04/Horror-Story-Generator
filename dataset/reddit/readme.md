# Analyze Subreddit

Subreddit: 
- creepypasta -> {'Trollpasta Story', nan, nan, nan, 'Audio Narration', 'Video', None, nan, 'Creepypasta', 'Text Story', 'Very Short Story', 'Podcast', 'Discussion', 'Creepypasta Story', 'Images & Comics', 'Images &amp; Comics', 'Iconpasta Story', 'Meta'} -> remain flair: ['Creepypasta', 'Text Story', 'Very Short Story']
- Creepypastastories -> {'Story', 'Discussion'} -> remnain flair: ['Story']
- Horror_stories -> {nan, None, nan} -> remain all
- nosleep -> {'', 'Child Abuse', 'Animal Abuse', None, nan, 'Series', nan, 'Spooktober', 'Sexual Violence', 'Beyond Belief', 'Self Harm', nan} -> drop: ["Series"]
- RedditHorrorStories -> {nan, 'Fictional Horror Story (Original story from different subreddit)', 'Video', None, nan, 'True Horror Story', 'Story (True)', 'Discussion', 'Story (Fiction)', 'Request', 'Fictional Horror Story'} -> remain flair: ['True Horror Story', 'Story (True)', 'Story (Fiction)', 'Fictional Horror Story']

## Filtering
- Story's in a serie -> not acceptable
- No more than 2048 tokens