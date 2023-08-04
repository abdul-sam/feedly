// import { BASE_URL, getAjaxRequest } from "./base"

const search = () => {
  let element = document.getElementById("searchInput")
  let feed_cards = document.getElementById("feed--cards")
  let q = element.value;
  let url = `${BASE_URL}/api/feeds?q=${q}`
  getAjaxRequest(url, "GET").then((data) => {
    debugger
    let content = appendSearchFeeds(data)
    feed_cards.innerHTML = content;
  })
}


const appendSearchFeeds = (feeds) => {
  let content = '';
  if (feeds.length > 0){
    feeds.map((feed) => {
      image_url = feed.image_url != '' ? feed.image_url : 'static/images/no-image.png';
      let description = descriptionParser(feed.description)
      content +=  `<div class="col-lg-12 mb-4">
                    <div class="card">
                      <div class="feed--follow-btn mt-3">
                        <span class="p-1 px-2 cursor-pointer" data-id="${feed.id}">
                          <button 
                            class="btn btn-outline-success px-3 fs-12 me-4 py-1 dropdown-toggle"
                            id="dropdown${feed.id}" data-bs-toggle="dropdown" aria-expanded="false"
                            onclick="preventClose(event);"
                          >
                            Follow
                          </button>
                        </span>
                      </div>
                      <div class="card-body">
                        <div class="d-flex">
                          <img
                            src="${image_url}"
                            alt=""
                            class="feed--image"
                            width="90px"
                          />
                          <a href="#" data-id="${feed.id}" class="text-decoration-none text-body ms-4">
                            <h5 class="card__title mt-3">${feed.title}</h5>
                            <p class="card-text text-muted fs-14">
                              ${description}
                            </p>
                          </a>
                        </div>
                      </div>
                    </div>
                  </div>`
    })
  } else {
    content +=  `<div class="text-muted mt-5 text-center">
                  <i class="fa-regular fa-face-sad-tear me-2 fs-44 mb-3"></i>
                  <p> Sorry! there is no feed match with your search</p>
                </div>`
  }

  return content;
}