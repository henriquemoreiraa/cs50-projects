let currEmail = null
let currEmailView = 'inbox'

document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => { currEmail = null; compose_email() });

  document.querySelector('form').addEventListener('submit', (e) => sendEmail(e))
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  if (currEmail) {
    document.querySelector('#compose-recipients').value = currEmail.sender === document.querySelector('#compose-sender').value ? currEmail.recipients[0] : currEmail.sender;
    document.querySelector('#compose-subject').value = `${currEmail.subject.includes("Re:") ? "" : 'Re:'} ${currEmail.subject}`;
    document.querySelector('#compose-body').value = `On ${currEmail.timestamp} ${currEmail.sender} wrote: ${currEmail.body}`;

    return
  }

  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  currEmailView = mailbox
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      emails.forEach(e => {
        document.querySelector('#emails-view').innerHTML +=
          `
          <button class="email-btn border border-zinc-500 p-2 flex justify-between w-full ${e.read ? 'bg-zinc-300' : 'bg-white'}" value="${e.id}">
            <div class="flex gap-3">
              <p><b>${mailbox === 'sent' ? 'To' : ''} ${e.recipients[0]}</b></p>
              <p>${e.subject}</p>
            </div>
            <p>${e.timestamp}</p>
          </button>
          `
      })
      document.querySelectorAll('.email-btn').forEach((button) => {
        button.addEventListener("click", () => viewEmail(button.value))
      })
    });
}

function viewEmail(id) {
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';

  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      if (!email.read) {
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
            read: true,
          })
        })
      }
      currEmail = email
      document.querySelector('#email-view').innerHTML =
        `
          <div class="relative">
           ${currEmailView !== 'sent' ? `<button class="btn absolute right-0" id="archive-btn" value="${email.archived}">${email.archived ? 'Unarchive' : 'Archive'}</button>` : ""} 
            <div>
              <p><b>From:</b> ${email.sender}</p>
              <p><b>To:</b> ${email.recipients[0]}</p>
              <p><b>Timestamp:</b> ${email.timestamp}</p>
              <p><b>Subject:</b> ${email.subject}</p>
              ${currEmailView !== 'sent' ? `<button id="reply-btn" class="btn">Reply</button>` : ''}
              ${currEmailView === 'sent' ? email.subject.includes("Re:") ? `<button id="reply-btn" class="btn">Reply</button>` : '' : ''}
            </div>
            <hr class="my-5 mb-2" />
            <p>${email.body}</p>
          </div>
        `

      document.querySelector("#archive-btn")?.addEventListener("click", () => archiveEmail(id, document.querySelector("#archive-btn").value))
      document.querySelector("#reply-btn").addEventListener("click", compose_email)
    })
}

function archiveEmail(id, archived) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: archived === 'false',
    })
  }).then(() => load_mailbox('inbox'))
}

function sendEmail(e) {
  e.preventDefault()

  const recipients = document.querySelector('#compose-recipients').value
  const subject = document.querySelector('#compose-subject').value
  const body = document.querySelector('#compose-body').value

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients,
      subject,
      body,
    })
  }).then(() => load_mailbox('sent'))
}