const urlParams = new URLSearchParams(window.location.search);
const orderBy = urlParams.get('order_by');

document.addEventListener('DOMContentLoaded', async () => {
  document.querySelector('.sort-select').value = orderBy || 'rating'

  document.querySelectorAll('.rate-select').forEach((select) => {
    select.addEventListener("change", (e) => {
      handleRating(Number(e.target.value), Number(e.target.name))
    })
  })

  document.querySelectorAll('.sort-select').forEach((select) => {
    select.addEventListener("change", (e) => {
      window.location = `?order_by=${e.target.value}`
    })
  })
})

const handleRating = async (rating, attemptId) => await fetch(`/rate/${attemptId}`, {
  method: 'PUT',
  body: JSON.stringify({
    rating,
  }),
}).then(() => window.location.reload())
