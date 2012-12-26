function(doc) {
  if (doc.doc_type == "tweet"){
    var d = new Date(Date.parse(doc.created_at));

    var key = [d.getFullYear(), d.getMonth() + 1, d.getDate(),
               d.getHours(), d.getMinutes(), d.getSeconds(),
               doc.user.time_zone];

    emit(key, doc._id);
  }
}
