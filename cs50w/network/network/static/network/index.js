
// let postsData = []
let currentPage;
let nextPage;
let previousPage;

let currentPost;

const url = window.location.pathname;
const userName = url.substring(url.lastIndexOf('/') + 1);
const isUserProfilePage = userName !== 'following'

if (userName && isUserProfilePage) {
  document.addEventListener('DOMContentLoaded', async () => {
    document.querySelector("#user-posts").innerHTML = `${userName}'s Posts`
    await Promise.all([
      getUser(),
      getPosts(1)
    ])
  })

} else {
  document.addEventListener('DOMContentLoaded', async () => {
    await getPosts(1);

    document.querySelector('#new-post-form').addEventListener('submit', (e) => createPost(e))
    document.querySelector('#edit-post-form').addEventListener('submit', (e) => updatePost(e))
  })
}

document.addEventListener('DOMContentLoaded', async () => {
  document.querySelector('#next-page-btn').addEventListener("click", async () => {
    await getPosts(nextPage)
  })

  document.querySelector('#previous-page-btn').addEventListener("click", async () => {
    await getPosts(previousPage)
  })
})

const renderPaginationBtns = () => {
  document.querySelector("#next-page-btn").style.display = nextPage ? 'block' : 'none';
  document.querySelector("#previous-page-btn").style.display = previousPage ? 'block' : 'none';

}

const renderPosts = (posts) => {
  document.querySelector('#posts-view').innerHTML = ''
  posts.forEach(post => {
    const isEditBtnVisible = userName || !post.is_user_owner
    const loggedUser = document.querySelector("#logged-user").value

    document.querySelector('#posts-view').innerHTML +=
      ` 
      <div class="shadow-sm p-3">
        <h3><a href="/profile/${post.user_name}">${post.user_name}</a></h3>
        ${!isEditBtnVisible ? `<button value="${post.id}" class="edit-btn text-blue-600">Edit</button>` : ""}
        <p>${post.content}</p>
        <p>${post.timestamp}</p>${loggedUser !== 'AnonymousUser' ? `        <button value="${post.id}" class="like-btn">${post.has_user_liked ? '💖' : '❤️'}</button>
          ` : '❤️'
      }
         ${post.likes}
      </div>
      `
  })
  document.querySelectorAll('.like-btn').forEach((button) => {
    button.addEventListener("click", () => likePost(posts, button.value))
  })
  document.querySelectorAll('.edit-btn').forEach((button) => {
    button.addEventListener("click", () => onClickEdit(posts, button.value))
  })
}

const onClickEdit = (posts, postId) => {
  const post = posts.find(p => p.id === Number(postId))
  currentPost = post

  document.querySelector('#new-post-form').style.display = 'none'
  document.querySelector('#edit-post-form').style.display = 'flex'
  document.querySelector('#edit-post').value = post.content
}

const likePost = (posts, postId) => {
  const post = posts.find(p => p.id === Number(postId))

  fetch(`/posts?page_id=${post.id}`, {
    method: 'PUT', body: JSON.stringify({
      like: !post.has_user_liked
    })
  }).then(() => {
    getPosts(currentPage)
  })
}

const updatePost = (e) => {
  e.preventDefault()

  const content = document.querySelector('#edit-post').value

  fetch(`/posts?page_id=${currentPost.id}`, {
    method: 'PUT', body: JSON.stringify({
      content,
    })
  }).then(() => {
    getPosts(currentPage)
    currentPost = null;
    document.querySelector('#new-post-form').style.display = 'block'
    document.querySelector('#edit-post-form').style.display = 'none'
  })
}

const createPost = (e) => {
  e.preventDefault()

  const content = document.querySelector('#new-post').value

  fetch(`/posts`, {
    method: 'POST', body: JSON.stringify({
      content,
    })
  }).then(() => {
    getPosts(currentPage)
    document.querySelector('#new-post').value = ''
  })
}

const getPosts = async (page) => await fetch(`/posts?page=${page}${createParams({
  list_by: url === '/' ? undefined : 'list',
  user_name: isUserProfilePage ? userName : undefined
})}`)
  .then((res) => res.json())
  .then(({ posts, next, previous, current }) => {
    nextPage = next;
    previousPage = previous;
    currentPage = current;

    renderPosts(posts)
    renderPaginationBtns()
  })

const followUser = (isUserFollowing) => {
  fetch(`/user/${userName}`, {
    method: 'PUT', body: JSON.stringify({
      follow: !isUserFollowing
    })
  }).then(() => {
    getUser()
  })
}

const getUser = async () => await fetch(`/user/${userName}`)
  .then((res) => res.json())
  .then(({ following, followers, is_user_following }) => {
    const loggedUser = document.querySelector("#logged-user").value
    console.log(typeof loggedUser)
    document.querySelector("#user-profile").innerHTML =
      `
      <h3 id="username">${userName}</h3>
      <p id="user-following">Following ${following}</p>
      <p id="user-followers">Followers ${followers}</p>
      <button style="display: none;" id="follow-btn">${is_user_following ? 'Unfollow' : 'Follow'}</button>
    `
    if (loggedUser !== 'AnonymousUser') {
      document.querySelector("#follow-btn").style.display = loggedUser === userName ? 'none' : 'block'
      document.querySelector("#follow-btn").addEventListener("click", () => followUser(is_user_following))
    }
  })

const createParams = (filters) => filters ? Object.entries(filters).map(([key, value]) => value ? `&${key}=${value}` : '').join("") : ''