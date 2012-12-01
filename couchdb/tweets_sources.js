function(doc) {
  if (doc.doc_type =="tweet"){
    var d = new Date(Date.parse(doc.created_at));
    
    var key = [d.getFullYear(), d.getMonth() + 1, d.getDate(),
               d.getHours(), d.getMinutes(), d.getSeconds()];
    
    var value = {tweet_id: doc.id,
                 tweet_id_str: doc.id_str,
                 source: doc.source,
                 user_id: doc.user.id,
                 user_id_str: doc.user.id_str};

    emit(key, value);
  }
}
