document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Send an email
  document.querySelector('#compose-form').onsubmit = function(event) {

    // Prevent page from reloading
    event.preventDefault();

    // Save the email
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
        // Print result
        console.log(result);
    });

    // Load sent mailbox
    setTimeout(function(){load_mailbox('sent');}, 100);
  }
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
};

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Populate the mailbox with emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      // Create the divs with emails
      emails.forEach(function(email) {
        const element = document.createElement('div');
        element.className = "email";
        element.innerHTML = `<div class="emails-sender">${email.sender}</div><div class="emails-body">${email.body}</div><div class="emails-timestamp">${email.timestamp}</div>`;
        if (email.read) {
          element.style.backgroundColor = "grey";
        }
        element.addEventListener('click', function() {
            load_email(email);
        });
        document.querySelector('#emails-view').append(element);
      });
  });
};

function load_email(email) {

  // Show the email and hide other views
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Fill the email info
  document.querySelector('#email-sender').innerHTML = `<strong>From: </strong>${email.sender}`;
  document.querySelector('#email-recipients').innerHTML = `<strong>To: </strong>${email.recipients}`;
  document.querySelector('#email-subject').innerHTML = `<strong>Subject: </strong>${email.subject}`;
  document.querySelector('#email-timestamp').innerHTML = `<strong>Timestamp: </strong>${email.timestamp}`;
  document.querySelector('#email-body').innerHTML = `${email.body}`;

  // Create reply variables
  reply_recipients = email.sender;
  if (email.subject.substring(0,4) == "Re: ") {
    reply_subject = email.subject
  }
  else {
    reply_subject = `Re: ${email.subject}`
  }
  reply_body = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`

  // Create reply button
  document.querySelector('#reply').addEventListener('click', () => reply(reply_recipients, reply_subject, reply_body));

  if (document.querySelector('#archive') !== null)
  {
    document.querySelector('#archive').remove();
    document.querySelector('#pre-archive').remove();
  }

  // Create archive/unarchive button
  if (document.querySelector('#user_email').innerHTML === String(email.recipients)) {

    const line = document.createElement('hr');
    line.id = "pre-archive";
    document.querySelector('#email-view').append(line);

    if (email.archived == true) {
      const element = document.createElement('button');
      element.className = "btn btn-sm btn-outline-primary";
      element.innerHTML = "Unarchive";
      element.id = "archive";
      element.addEventListener('click', function() {
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: false
          })
        })
        setTimeout(function(){load_mailbox('inbox');}, 100);
      });
      document.querySelector('#email-view').append(element);
    }
    else {
      const element = document.createElement('button');
      element.className = "btn btn-sm btn-outline-primary";
      element.innerHTML = "Archive";
      element.id = "archive";
      element.addEventListener('click', function() {
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: true
          })
        })
        setTimeout(function(){load_mailbox('inbox');}, 100);
      });
      document.querySelector('#email-view').append(element);
    }
  }

  // Mark email as read
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
};

function reply(recipients, subject, body) {

  // Show compose view and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Fill composition fields
  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;
}