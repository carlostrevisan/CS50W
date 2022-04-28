document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  document.querySelector('#compose-form').onsubmit = function () {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
      .then(response => response.json())
      .then(result => {
        console.log(result);
      });
    load_mailbox('sent')
    return false;
  };

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  let posts = []

  fetch(`/emails/${mailbox}`, {
    method: 'GET'
  })
    .then(response => response.json())
    .then(data => {
      const posts = data
      const user = document.getElementById('user').innerHTML
      console.log(posts)
      posts.sort(sortById)
      for (let index = 0; index < posts.length; index++) {
        if (posts[index].recipients.includes(user)) {
          const div1 = document.createElement('div')
          div1.className = "card"
          div1.style.marginTop = "5px"
          if (posts[index].read)
            div1.style.backgroundColor = "#D3D3D3"
          document.querySelector('#emails-view').append(div1)
          div1.addEventListener("click", () => { read_email(posts[index].id, mailbox) })
          const div2 = document.createElement('div')
          div2.className = "card-body"
          div1.appendChild(div2)
          const subject = document.createElement('h5')
          subject.className = 'card-title'
          subject.innerHTML = `${posts[index].subject}`
          div2.append(subject)
          const sender = document.createElement('h6')
          sender.className = 'card-subtitle'
          sender.innerHTML = `From: ${posts[index].sender}`
          div2.append(sender)
          const date = document.createElement('p')
          date.innerHTML = posts[index].timestamp
          date.style.textAlign = 'right'
          date.style.marginBottom = "0px"
          div2.append(date)
        }
      }
    });

  return false;
};

function read_email(id, mailbox) {
  console.log('tu apertou no id: ', id)
  const user = document.getElementById('user').innerHTML

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

  fetch(`/emails/${id}`, {
    method: 'GET'
  })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      document.querySelector('#emails-view').innerHTML = ""
      const emailview = document.querySelector('#emails-view');
      const subject = document.createElement('h1')
      subject.innerHTML = data.subject
      emailview.append(subject)
      const sender = document.createElement('h5')
      sender.innerHTML = `From: ${data.sender}`
      emailview.append(sender)
      const date = document.createElement('p')
      date.innerHTML = data.timestamp
      date.style.textAlign = 'right'
      emailview.append(date)
      const body = document.createElement('p')
      body.innerHTML = data.body
      emailview.append(body)
      const answerBnt = document.createElement('button')
      answerBnt.innerHTML = "Reply"
      answerBnt.className = "btn btn-outline-primary"
      answerBnt.style.marginRight = "5px"
      emailview.append(answerBnt)
      answerBnt.addEventListener("click", () => reply_email(data.id))
      if (mailbox !== "sent") {
        const archiveBnt = document.createElement('button')
        archiveBnt.innerHTML = "Archive"
        archiveBnt.className = "btn btn-primary"
        archiveBnt.style.marginRight = "5px"
        emailview.append(archiveBnt)
        archiveBnt.addEventListener('click', () => archive_email(data.id))
      }
      const unreadBnt = document.createElement('button')
      unreadBnt.innerHTML = "Mark as Unread"
      unreadBnt.className = "btn btn-secondary"
      emailview.append(unreadBnt)
      unreadBnt.addEventListener('click', () => markAsUnread(data.id))
    })
}

function markAsUnread(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: false
    })
  })
    .then(() => load_mailbox('inbox'))
}

function archive_email(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true
    })
  })
}

function sortById(a, b) {
  if (a.id > b.id) {
    return -1;
  }
  if (a.id < b.id) {
    return 1;
  }
  return 0;
}

function reply_email(id) {

}