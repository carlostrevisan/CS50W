function likepost(id) {
    console.log(id)
    fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: false
        })
    })
        .then(() => load_mailbox('inbox'))
}