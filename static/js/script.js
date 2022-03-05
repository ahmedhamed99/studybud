// // Actions:

// const closeButton = `<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
// <title>remove</title>
// <path d="M27.314 6.019l-1.333-1.333-9.98 9.981-9.981-9.981-1.333 1.333 9.981 9.981-9.981 9.98 1.333 1.333 9.981-9.98 9.98 9.98 1.333-1.333-9.98-9.98 9.98-9.981z"></path>
// </svg>
// `;
// const menuButton = `<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
// <title>ellipsis-horizontal</title>
// <path d="M16 7.843c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 1.98c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// <path d="M16 19.908c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 14.046c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// <path d="M16 31.974c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 26.111c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// </svg>
// `;

// const actionButtons = document.querySelectorAll('.action-button');

// if (actionButtons) {
//   actionButtons.forEach(button => {
//     button.addEventListener('click', () => {
//       const buttonId = button.dataset.id;
//       let popup = document.querySelector(`.popup-${buttonId}`);
//       console.log(popup);
//       if (popup) {
//         button.innerHTML = menuButton;
//         return popup.remove();
//       }

//       const deleteUrl = button.dataset.deleteUrl;
//       const editUrl = button.dataset.editUrl;
//       button.innerHTML = closeButton;

//       popup = document.createElement('div');
//       popup.classList.add('popup');
//       popup.classList.add(`popup-${buttonId}`);
//       popup.innerHTML = `<a href="${editUrl}">Edit</a>
//       <form action="${deleteUrl}" method="delete">
//         <button type="submit">Delete</button>
//       </form>`;
//       button.insertAdjacentElement('afterend', popup);
//     });
//   });
// }


const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}

// Upload Image
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
  photoInput.onchange = () => {
    const [file] = photoInput.files;
    if (file) {
      photoPreview.src = URL.createObjectURL(file);
    }
  };

// Scroll to Bottom
const conversationThread = document.querySelector(".room__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;

let csrftoken = getCookie('csrftoken');

const follow_topic = document.querySelectorAll('#follow-topic');

if (follow_topic) {

  follow_topic.forEach(button => {
    button.addEventListener('click', function (event) {
      topic_id = this.dataset.id;
      if (this.innerHTML === "Follow") {
        fetch(`/follow_topic/${topic_id}`, {
          method: 'PUT',
          body: JSON.stringify({
            'method': 'follow'
          }),
          headers: { "X-CSRFToken": csrftoken },
        })
          .then(res => res.json())
          .then(data => {
                if (data['error']){
                  alert(`${data['error']}`)
                }else if (data['message']){
                  this.innerHTML = 'Following';
                }
          })
          .catch(err => console.log("error:", err));
      } else if (this.innerHTML === 'Following') {
        fetch(`/follow_topic/${topic_id}`, {
          method: "PUT",
          body: JSON.stringify({
            "method": 'unfollow'
          }),
          headers: { "X-CSRFToken": csrftoken },
        })
        .then(res => res.json())
        .then(data => {
                if (data['error']){
                  alert(`${data['error']}`)
                }else if (data['message']){
                  this.innerHTML = 'Follow';
                }
        })
      }
      event.preventDefault();
    });
  });

  const follow_user = document.querySelectorAll('#follow-user');
  

  if (follow_user) {

    follow_user.forEach(button => {
      button.addEventListener('click', function () {
        user_id = this.dataset.id;
        console.log(this.dataset.method)
        if (this.dataset.method === "follow") {
          fetch(`/follow_user/${user_id}`, {
            method: 'PUT',
            body: JSON.stringify({
              'method': 'follow'
            }),
            headers: { "X-CSRFToken": csrftoken },
          })
            .then(res => res.json())
            .then(data => {
                if (data['error']){
                  alert(`${data['error']}`)
                }else if (data['message']){
                  console.log(data);
                  this.innerHTML = 'Following';
                  this.dataset.method = 'unfollow';
                }
            })
            .catch(err => console.log("error:", err));
        } else if (this.dataset.method === 'unfollow') {
          fetch(`/follow_user/${user_id}`, {
            method: "PUT",
            body: JSON.stringify({
              "method": 'unfollow'
            }),
            headers: { "X-CSRFToken": csrftoken },
          })
          .then(res => res.json())
          .then(data => {
                if (data['error']){
                  alert(`${data['error']}`)
                }else if (data['message']){
                  console.log(data);
                  this.innerHTML = 'Follow';
                  this.dataset.method = 'follow';
                }
          })
        }

      });
    });
  }
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}