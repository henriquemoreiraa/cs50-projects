let currentPage;
let nextPage;
let previousPage;
let countPage;

document.addEventListener('DOMContentLoaded', async () => {
  await getSheets(1);

  document.querySelector("form").addEventListener("submit", (e) => { e.preventDefault(); getSheets(1) })

  document.querySelector('#next-page-btn').addEventListener("click", async () => {
    await getSheets(nextPage)
  })
  document.querySelector('#last-page-btn').addEventListener("click", async () => {
    await getSheets(countPage)
  })
  document.querySelector('#previous-page-btn').addEventListener("click", async () => {
    await getSheets(previousPage)
  })
  document.querySelector('#first-page-btn').addEventListener("click", async () => {
    await getSheets(1)
  })
})

const renderPosts = (sheets) => {
  document.querySelector('#sheets-view').innerHTML = ''

  if (sheets.length === 0) {
    document.querySelector('#sheets-view').innerHTML = '<p class="text-center w-full">No results</p>'
    return
  }

  sheets.forEach(sheet => {

    document.querySelector('#sheets-view').innerHTML +=
      ` 
      <div class="p-3">
      <a href="/sheet/${sheet.id}">  
        <div class="w-[300px] h-[400px] border bg-white ">
        <img class="object-contain w-full h-full" src="${sheet.img}" alt="sheet">
        </div>
      </a>
      <a href="/sheet/${sheet.id}">  
        <h3 class="text-sm mt-0">${sheet.name}</h3>
      </a>
      </div>
      `
  })
}

const renderPaginationBtns = () => {
  document.querySelector("#current-page-btn").innerHTML = currentPage;
  document.querySelector("#next-page-btn").style.display = nextPage ? 'block' : 'none';
  document.querySelector("#next-page-btn").innerHTML = nextPage;
  document.querySelector("#previous-page-btn").style.display = previousPage ? 'block' : 'none';
  document.querySelector("#previous-page-btn").innerHTML = previousPage;

  document.querySelector("#first-page").style.display = previousPage !== 1 ? currentPage !== 1 ? 'block' : 'none' : 'none';
  document.querySelector("#first-page-btn").innerHTML = 1;

  document.querySelector("#last-page").style.display = nextPage !== countPage ? currentPage !== countPage ? 'block' : 'none' : 'none';
  if (countPage === 0 || !nextPage) {
    document.querySelector("#last-page").style.display = 'none';
  }
  document.querySelector("#last-page-btn").innerHTML = countPage;
}

const getSheets = async (page) => await fetch(`/sheets?page=${page}${createParams({ search: document.querySelector('#search').value })}`)
  .then((res) => res.json())
  .then(({ results, count, next, previous, current }) => {
    nextPage = next;
    previousPage = previous;
    currentPage = current;
    countPage = count;
    console.log(countPage)
    renderPosts(results)
    renderPaginationBtns()
  })

const createParams = (filters) => filters ? Object.entries(filters).map(([key, value]) => value ? `&${key}=${value}` : '').join("") : ''