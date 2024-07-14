
CALL apoc.load.json("file:///stackoverflow.json") YIELD value
UNWIND value.items AS q

MERGE (question:Question {uuid:q.question_id})
  ON CREATE SET question.title = q.title, 
  	question.link = q.share_link, 
  	question.creation_date = q.creation_date, 
  	question.accepted_answer_id=q.accepted_answer_id, 
  	question.view_count=q.view_count,
   	question.answer_count=q.answer_count,
   	question.body_markdown=q.body_markdown

MERGE (owner:User {uuid:coalesce(q.owner.user_id,'deleted')})
  ON CREATE SET owner.display_name = q.owner.display_name
MERGE (owner)-[:ASKED]->(question)

FOREACH (tagName IN q.tags | 
  MERGE (tag:Tag {name:tagName}) 
    ON CREATE SET tag.link = "https://stackoverflow.com/questions/tagged/" + tag.name
  MERGE (question)-[:TAGGED]->(tag))

FOREACH (a IN q.answers |
   MERGE (question)<-[:ANSWERED]-(answer:Answer {uuid:a.answer_id})
    ON CREATE SET answer.is_accepted = a.is_accepted,
    answer.link=a.share_link,
    answer.title=a.title,
    answer.body_markdown=a.body_markdown,
    answer.score=a.score,
   	answer.favorite_score=a.favorite_score,
   	answer.view_count=a.view_count
   MERGE (answerer:User {uuid:coalesce(a.owner.user_id,'deleted')}) 
    ON CREATE SET answerer.display_name = a.owner.display_name
   MERGE (answer)<-[:PROVIDED]-(answerer)
)
FOREACH (c in q.comments |
  MERGE (question)<-[:COMMENTED_ON]-(comment:Comment {uuid:c.comment_id})
    ON CREATE SET comment.link=c.link, comment.score=c.score
  MERGE (commenter:User {uuid:coalesce(c.owner.user_id,'deleted')}) 
    ON CREATE SET commenter.display_name = c.owner.display_name
  MERGE (comment)<-[:COMMENTED]-(commenter)
);